# built in
import sys
import json
import logging
from datetime import datetime
from os import environ
from traceback import print_exception
import signal

# dependencies
import asyncio
from typing import Optional, Any
import discord
from discord import commands
from discord.ext.commands import Bot, Cog
from dotenv import load_dotenv

_log = logging.getLogger(__name__)

def _flatten_user(user: discord.User) -> dict[str, str]:
    return {
        "id": str(user.id),
        "name": user.name,
        "discriminator": user.discriminator,
        "mention": user.mention,
        "bot": user.bot,
        "display_name": user.display_name or user.name,
        "nick": user.nick or None,
    }

def _cancel_tasks(loop: asyncio.AbstractEventLoop) -> None:
    tasks = {t for t in asyncio.all_tasks(loop=loop) if not t.done()}

    if not tasks:
        return

    _log.info("Cleaning up after {len(tasks):d} tasks.", )
    for task in tasks:
        task.cancel()

    loop.run_until_complete(asyncio.gather(*tasks, return_exceptions = True))
    _log.info("All tasks finished cancelling.")

    for task in tasks:
        if task.cancelled():
            continue
        if task.exception() is not None:
            loop.call_exception_handler({
                "message": "Unhandled exception during shutdown operations.",
                "exception": task.exception(),
                "task": task,
            })

def _cleanup_loop(loop: asyncio.AbstractEventLoop) -> None:
    try:
        _cancel_tasks(loop)
        loop.run_until_complete(loop.shutdown_asyncgens())
    finally:
        _log.info("Closing the event loop.")
        loop.close()

def _default_config() -> dict[str, Any]:
    return {
        "command_prefix": "!", # this is a bridge in lieu of /slash
        "cache_file_name": "config.json", # any name, any JSON file will work
        "maintain_every": 60, # 1 minute (60 seconds) max data loss
        "no_message_color": 0xE74C3C, # red, #0xE74C3C, discord.Color.red(), discord.Color.from_rgb(231, 76, 60), etc.
        "with_message_color": 0x3498DB, # blue, #3498DB, discord.Color.blue(), discord.Color.from_rgb(52, 152, 219), etc.
        "embed_title": "Last message from {name}", # All user {properties} are accessible here
        "deleted_message_response": "{name}'s last message was deleted.", # All user {properties} are accessible here
        "no_message_response": "No message has been seen that was sent by {name}.", # All user {properties} are accessible here
        "mention_response": "Hello, {name}!", # All user {properties} are accessible here
    }

class Cache(Cog):
    _cache: dict[str, int] = {}

    def __init__(self, client, **data):
        self.client = client
        self.bot = client.bot
        self._task = None
        self.fill_message_cache(**data)

    def fill_message_cache(self, **data) -> None:
        self._cache.update(**data)

    async def load_message_cache(self) -> None:
        _log.info("Loading the user message cache...")
        try:
            with open(self.client.config.get("cache_file_name"), "r") as f:
                self.fill_message_cache(**json.load(f))
                _log.info("Successfully loaded the user message cache.")
        except FileNotFoundError:
            _log.info("No cache file found. Creating a new cache file...")
            await self.store_message_cache()

    async def store_message_cache(self) -> None:
        _log.info("Storing the user message cache...")
        with open(self.client.config.get("cache_file_name"), "w") as f:
            json.dump(self._cache, f)
            _log.info("Successfully stored the user message cache.")

    async def cache_sentry(self) -> None:
        await asyncio.sleep(int(self.client.config.get("maintain_every")))
        _log.info("Cache maintenance starting...")
        if not self._task == None:
            _log.info("Parallel sentry task found. awaiting...")
            # ensure no parallel tasks are running
            await self._task

        self._task = asyncio.create_task(self.store_message_cache())

        # awaiting here ensures no parallel scheduling
        await self._task

        # clear the task
        self._task = None

        _log.info("Cache maintenance completed. Rescheduling...")

        # rescheudle sentry
        self.schedule_cache_maintenance()

    def schedule_cache_maintenance(self) -> None:
        _log.info(f"Next cache maintenance in {int(self.client.config.get('maintain_every')) / 60:.2f} minutes...")
        # schedule the task and await its completion
        # it will reschedule itself
        return asyncio.create_task(self.cache_sentry())

    def get_message(self, user_id: int) -> int:
        user_id = str(user_id)

        return self._cache.get(user_id, None)

    def has_message(self, user_id: int) -> bool:
        user_id = str(user_id)

        return user_id in self._cache

    def add_message(self, user_id: int, channel_id: int, message_id: int) -> None:
        user_id = str(user_id)

        self._cache[user_id] = (channel_id, message_id)

    def remove_message(self, user_id: int) -> None:
        user_id = str(user_id)

        self._cache.pop(user_id, None)

class Responses(Cog):
    def __init__(self, client):
        self.client = client
        self.bot = client.bot

    def generate_user_summary(self, user: discord.User) -> str:
        return f"**User ID:** `{user.id}`\n**User Joined:** <t:{int(datetime.timestamp(user.joined_at))}:f>, <t:{int(datetime.timestamp(user.joined_at))}:R>"

    def generate_message_summary(self, user: discord.User, message: discord.Message) -> str:
        return f"**Channel:** <#{message.channel.id}> (ID: `{message.channel.id}`)\n**Message ID:** `{message.id}`\n**Message Created:** <t:{int(datetime.timestamp(message.created_at))}:f>, <t:{int(datetime.timestamp(message.created_at))}:R>\n**Message Content:**\n```\n{message.content}\n```"

    def generate_deleted_message_summary(self, user: discord.User, channel_id: int, message_id: int) -> None:
        return f"**Channel:** <#{channel_id}> (ID: `{channel_id}`\n**Message ID:** `{message_id}`\n**Message Content:**\n```\n{self.client.config.get('deleted_message_response').format(**_flatten_user(user)) or 'Message was deleted.'}\n```"

    def generate_no_message_summary(self, user: discord.User) -> None:
        return f"```\n{self.client.config.get('no_message_response').format(**_flatten_user(user)) or 'No message found.'}\n```"

    def generate_user_deleted_message_summary(self, user: discord.User, channel_id: int, message_id: int) -> str:
        return f"{self.generate_user_summary(user)}\n{self.generate_deleted_message_summary(user, channel_id, message_id)}"

    def generate_no_user_message_summary(self, user: discord.User) -> str:
        return f"{self.generate_user_summary(user)}\n{self.generate_no_message_summary(user)}"

    def generate_user_message_summary(self, user: discord.User, message: discord.Message) -> str:
        return f"{self.generate_user_summary(user)}\n{self.generate_message_summary(user, message)}"

    def create_no_message_embed(self, user: discord.User) -> discord.Embed:
        return discord.Embed(
            title = self.client.config.get("embed_title").format(**_flatten_user(user)),
            description = self.generate_no_user_message_summary(user),
            color = discord.Color(self.client.config.get("no_message_color")),
        )

    def create_deleted_message_embed(self, user: discord.User, channel_id: int, message_id: int) -> discord.Embed:
        return discord.Embed(
            title = self.client.config.get("embed_title").format(**_flatten_user(user)),
            description = self.generate_user_deleted_message_summary(user, channel_id, message_id),
            color = discord.Color(self.client.config.get("no_message_color")),
        )

    def create_message_embed(self, user: discord.User, message: discord.Message) -> discord.Embed:
        return discord.Embed(
            title = self.client.config.get("embed_title").format(**_flatten_user(user)),
            description = self.generate_user_message_summary(user, message),
            color = discord.Color(self.client.config.get("with_message_color")),
        )

    async def create_user_message_embed(self, user: discord.User) -> discord.Embed:
        cache_cog = self.bot.get_cog("Cache")
        flag = 0

        # get the last message from the cache
        res: tuple[int, int] = cache_cog.get_message(str(user.id))

        if not res == None:
            message = self.bot.get_message(res[1])

            if not message:
                # get the channel from the channel ID
                channel = self.bot.get_channel(res[0])
                # get the message from the message ID
                try:
                    message = await channel.fetch_message(res[1])
                except (
                    discord.NotFound,
                    discord.Forbidden,
                    discord.HTTPException,
                ):
                    pass

            if message == None:
                flag = -1
            else:
                flag = 1

        # if the last message the user sent was deleted
        if flag == -1:
            return self.create_deleted_message_embed(user, res[0], res[1])
        # if the user has not sent a message that the bot has seen
        elif flag == 0:
            return self.create_no_message_embed(user)
        # if the user has sent a message that the bot has seen
        elif flag == 1:
            return self.create_message_embed(message.author, message)

class Commands(Cog):
    def __init__(self, client):
        self.client = client
        self.bot = client.bot

    @commands.slash_command(
        name = "last",
        aliases = ["l"],
        description = "Get the last message from a user",
        usage = "last [user]",
        guild_ids = [474389512684961813]
    )
    async def last(self, ctx, *, user: discord.Option(discord.User, description = "The user whose message to retrieve.", required = False)) -> None:
        response_cog = self.bot.get_cog("Responses")

        if user == None:
            user = ctx.author

        # get the last message from the cache
        embed = await response_cog.create_user_message_embed(user)

        # send the message
        await ctx.respond(embed = embed)

class Listeners(Cog):
    def __init__(self, client):
        self.client = client
        self.bot = client.bot

    @Cog.listener()
    async def on_member_leave(self, member: discord.Member) -> None:
        cache_cog = self.bot.get_cog("Cache")
        user_id = str(member.id)

        if cache_cog.has_message(user_id):
            _log.info(f"Removing user ID ' {user_id} ' from cache")
            cache_cog.remove_message(user_id)

    @Cog.listener()
    async def on_ready(self) -> None:
        cache_cog = self.bot.get_cog("Cache")
        _log.info("Bot successfully connected to the Discord Gateway.")
        await cache_cog.load_message_cache()

        # schedule the cache maintenance task
        # this starts the initial task cycle
        self.bot._cache_task = cache_cog.schedule_cache_maintenance()

        _log.info("Bot is ready.")

    @Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        cache_cog = self.bot.get_cog("Cache")
        # ignore messages from bot users
        if message.author.bot == True:
            return

        # add the message to the cache under the user's ID
        cache_cog.add_message(message.author.id, message.channel.id, message.id)

        if message.content.startswith((f"<@{self.bot.user.id}> ", f"<@!{self.bot.user.id}> ")):
            # when a user mentions the bot, respond with a hello
            await message.reply(content = self.client.config.get("mention_response").format(**_flatten_user(message.author)))

class DiscordClient:
    def __init__(self, options: dict[str, Any], cogs: list[Cog]) -> None:
        self._set_config(options)
        self._cogs = cogs

        self.bot = Bot(**options)
        # overwrite to prevent attempt to call a command
        # when the bot is mentioned
        self.bot.on_mention = self._on_mention
        self._cache_task = None

    def _on_mention(self, *args, **kwargs) -> None:
        pass

    def _set_config(self, options) -> None:
        default_config = _default_config()
        self.config = {
            "command_prefix": options.pop("command_prefix", default_config.get("command_prefix")),
            "cache_file_name": options.pop("cache_file_name", default_config.get("cache_file_name")),
            "maintain_every": int(options.pop("maintain_every", default_config.get("cache_file_name"))),
            "no_message_color": int(options.pop("no_message_color", default_config.get("cache_file_name"))),
            "with_message_color": int(options.pop("with_message_color", default_config.get("cache_file_name"))),
            "embed_title": options.pop("embed_title", default_config.get("cache_file_name")),
            "deleted_message_response": options.pop("deleted_message_response", default_config.get("cache_file_name")),
            "no_message_response": options.pop("no_message_response", default_config.get("cache_file_name")),
            "mention_response": options.pop("mention_response", default_config.get("cache_file_name")),
        }

    def register_cogs(self) -> None:
        for cog in self._cogs:
            self.bot.add_cog(cog(self))

    async def sentry(self, token: str, *, reconnect: Optional[bool] = True):
        try:
            self.register_cogs()
            await self.bot.start(token, reconnect = reconnect)
        finally:
            if not self.bot.is_closed():
                await self.bot.close()

    def schedule_sentry(self, token: str, *, reconnect: Optional[bool] = False):
        return asyncio.ensure_future(self.sentry(token, reconnect = reconnect), loop = self.bot.loop)

    def run(self, token: str, *, reconnect: Optional[bool] = True) -> None:
        try:
            self.bot.loop.add_signal_handler(signal.SIGINT, self.bot.loop.stop)
            self.bot.loop.add_signal_handler(signal.SIGTERM, self.bot.loop.stop)
        except (NotImplementedError, RuntimeError):
            pass

        def stop_loop_on_completion(future: asyncio.Future):
            self.bot.loop.stop()

        future = self.schedule_sentry(token, reconnect = reconnect)
        future.add_done_callback(stop_loop_on_completion)

        try:
            self.bot.loop.run_forever()
        except KeyboardInterrupt:
            _log.info("Received signal to terminate.")
        finally:
            future.remove_done_callback(stop_loop_on_completion)
            _log.info("Cleaning up tasks...")
            _cleanup_loop(loop)

        if not future.cancelled():
            try:
                return future.result()
            except KeyboardInterrupt:
                pass

def run() -> None:
    # create new event loop
    loop = asyncio.new_event_loop()

    # load the virtual environment where the token is stored
    # NOTE: this is not the same virtual environment used by
    # the python interpreter, this is only within the script file
    load_dotenv()

    # default config for fallback in case
    # the config file is not found

    # load the local config file
    try:
        _log.info("Loading config file...")
        with open("config.json", "r") as f:
            config = json.load(f)
    except FileNotFoundError:
        _log.error("Config file not found. Default config file was created and stored on the local disk.")
        with open("config.json", "w") as f:
            config = _default_config()
            json.dump(config, f)

    # configure logging
    logging.basicConfig(
        stream = sys.stdout,
        level = logging.INFO, 
        format= '%(asctime)s:%(levelname)s:%(name)s: %(message)s',
        datefmt='%H:%M:%S',
    )

    # create the bot
    client = DiscordClient(
        options = {
            **config,
            "loop": loop,
            "intents": discord.Intents.all(),
        },
        cogs = [
            Cache,
            Commands,
            Responses,
            Listeners,
        ]
    )

    # run the bot
    client.run(token = environ.get("DISCORD_TOKEN"))

if __name__ == "__main__":
    run()

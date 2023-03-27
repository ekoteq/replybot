# Triggers
## `@Mention`
The bot will reply with a custom message when mentioned. The message will be the same for all users
and will be configurable in the config file.

The custom response message may be updated at any time. However, the bot client must be restarted
for the changes to take effect.

### Parameters
* `message` - Any message received that starts with the bot's mention: `<@botid>`

### Output
* `text` - A string response based on the `mention_response` defined in `config.json`

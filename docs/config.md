# Configuration Seetup
The config file hosts all major settings that the bot uses.

The bot will not run without a config file, but a default file will be created if one does not exist.

##Properties
### cache_file_name
The name of the file that the bot will use to store the cache. The file will be
created in the same directory as the bot's executable.

### maintain_every
The number of seconds between cache maintenance. Cache maintenance is the process of
saving the cache to the disk, along with any updates that have happened to the cache
since the last maintenance cycle.

### no_message_color
The color of the embed that is sent when a user has not sent a message in the server.

### with_message_color
The color of the embed that is sent when a user has sent a message in the server.

### embed_title
The title of the embed that is sent when a user has sent a message in the server.

### deleted_message_response
The message that is sent when a user has sent a message in the server, but that message
has since been deleted.

### no_message_response
The message that is sent when a user has not sent a message in the server.

### mention_response
The message that is sent when the bot is mentioned.
  
## Default Configuration
* cache_file_name: "cache.json",
* maintain_every: 60,
* no_message_color: 15158332,
* with_message_color: 3447003,
* embed_title: "Last message from {name}",
* deleted_message_response: "{name}'s last message was deleted.",
* no_message_response: "No message has been seen that was sent by {name}.",
* mention_response: "Hello, {name}!"

Response messages have access to the user object and can make use of all attributes a discord
user owns. All attributes must be {wrapped} in order to be properly formatted.

If an attribute exists and it is not listed here, it is not recommended or incompatible for
use with response messages.

## User Attributes
* id: The user's ID.
* name: The user's name.
* discriminator: The user's discriminator.
* bot: True or False. Whether the user is a bot.
* display_name: The user's display name. This is either their server nickname, or
username if none exists.
* mention: The user's mention.
* nick: The user's nickname.

For those familiar with python and methods for string values, all methods implemented
by string objects may be called in response messages. ex: {string.lower()} for
lowercase operations, or {string.split(x)} for split operations. f-string tags, such
as !r, !d, !s, and !a, are also supported. ex: {string!r} for repr or {string!d} for
comma-separated numbers.
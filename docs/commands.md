# Commands
## `/last`
The `/last` command will reply with summary information about the last message a user has sent.
Summary information will include the contents of the message if the message exists and has not
been deleted by the user or other server members.

### Parameters
* `user` - The user to get the last message for. This can be a mention, ID, or name. If no user is
specified, the command will default to the user who sent the command.

### Output
* `rich embed` - An embed detailing the user's last message, no message found, or last message deleted.

Embed parameters, such as the title, color, and response values are modifyable by changing their values
in the `config.json` file.

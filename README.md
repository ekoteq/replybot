ReplyBot v1.0.0

# Info
This is a simple discord bot that will store the last message ID sent by each user
in all known discord guilds, as well as reply with a custom response message when mentioned.

## Requirements
* Python 3.11 or higher

## Dependencies
* pycord 2.4.1 or higher
* asyncio 3.4.3 or higher
* python-dotenv 1.0.0 or higher

## Optional Dependencies
* virtualenv 20.21.0 or higher

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

# Quick Setup
This quick setup guide assumes you are using a system with a graphical interface and not a headless
unit that interfaces via the command-line only. This bot may run on either system, but the windowless
mode is not available for headless or command-line environments.

1. Install Python 3.11 if you have not already done so and restart.

2. Download a copy of this repository and save it somewhere.

3. Modify the .env and config.json files with relevant secrets and settings.

4. Right-click either the `start.pyw` or `core.py` files and open it with Python.

5. Open a command prompt and run the following commands:
	1. `cd <path to bot folder>`

	2. OPTIONAL:
		1. `python -m pip install virtualenv`

		2. `virtualenv --python \path\to\python venv`

		3. `venv\Scripts\activate.bat`

	2. `python -m pip install -r requirements.txt`

	3. Update the .env file with relevant secrets

	4. Update the config.json file with relevant settings

	5. Right click desired script and open with Python.

# Installation
1. Obtain a copy of Python v3.11 or higher and install it on the same system where the
	scripts will be executed. If prompted, add python to the path variables. Once installed,
	restart your system.
	- Official download link: https://www.python.org/downloads/release/python-3110/

2. After rebooting, download a copy of this repository and save it in the same location from which it
	will be run or executed.
	- You can download a copy of this repository by clicking the green "Code" button and selecting "Download ZIP".

3. Open a command prompt window.
	- Windows: Press the Windows key and type "cmd" and press enter.
	- Linux: Press the Super key and type "terminal" and press enter.
	- Mac: Press the Command key and type "terminal" and press enter.

4. Change directories into the folder where the `core.py` file is located.
	- The command to change directories is `cd <path>` ex: `cd ./replybot`.

5. If you plan to use a virtual environment, you will need to install additional dependencies
not covered by the standard requirements install.

	1. Run the command `python -m pip install virtualenv` to create a virtual environment. After install, restart
		your system to ensure changes have taken effect.
		- If you receive any errors, try opening the command prompt as an administrator by right-clicking
		the command prompt icon and selecting "Open as administrator" before running commands.

	2. Run the command `virtualenv --python \path\to\python venv` to create a virtual environment
		within your bot folder.
		- The path where your Python exe file is located will dependent on your operating system and settings.
		A typical windows path looks like: `C:\Users\username\AppData\Local\Programs\Python\Python311\python.exe`
		and a typical linux path looks like: `/usr/bin/python3.11`

5. Install the required dependencies with the command `python -m pip install -r requirements.txt`.
	- If you are using a virtual environment, you MUST activate it first.
	- The command to activate a virtual environment is `venv\Scripts\activate.bat`.
	- If you are using a linux system, the command to activate a virtual environment is `source venv/bin/activate`.
	- If you are using a linux system, you may need to run the command `chmod +x venv/bin/activate` to
	allow the script to be executed.

# Discord Application Setup
1. Navigate to https://discord.com/developers/applications in your web browser.
	- If you are not signed in, you will need to sign in to continue.

2. Click the "New Application" button.

3. Give your application a name, read through and agree (or disagree) to the terms, and click "Create".

4. Click the "Bot" tab on the left side of the screen.

5. Click the "Add Bot" button.

6. Review the bot's information and click the "Copy" button to copy the bot's token.
	- This token will be used to connect to the API and gateway.
		- This token will not be shown again, so be sure to save it somewhere safe.

7. Open the .env file in the bot's folder (this can be opened with notepad like a text file) and save the
bot's secret token beside the 'DISCORD_TOKEN' entry.
	- The .env file should look something like this:
		```
		DISCORD_TOKEN=your_token_here
		```
7. Click the "URL Generator" on the left side of the screen.

8. Select the "bot" scope.

9. Review the permissions and select the ones you want to grant the bot.
	- This specific bot requires the following permissions:
		* Send Messages
		* Embed Links
		* Read Message History
		* Read Messages/View Channels

10. The generated URL may be used to invite your new bot user to any server.
	- Those interested in inviting your bot to their server will need to have
	the "Manage Server" permission on the server they wish to invite the bot to.

## Token Reset
1. Click the "Oauth2" tab on the left side of the screen.

2. Click the "Reset Secret" button to generate your bot's secret token, used to connect to the API and gateway.

3. Copy the token and paste it into the `.env` file in the `DISCORD_TOKEN` field. You will not have access to this
token via the website again, so be sure to save it before you leave the page.

# Configuration Seetup
The config file hosts all major settings that the bot uses.

The bot will not run without a config file, but a default file will be created if one does not exist.

## Properties
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

# Bot Setup
1. Navigate to the folder where you saved the bot files.

2. Right-click either the `start.pyw` or `core.py` files and open it with Python.
	- If you are using a linux system, you may need to run the command `chmod +x start.pyw` to
	allow the script to be executed.
	- the `core.py` file contains all of the logic necessary for the bot to run. Running this file
	will open a command prompt window and display debug output. Closing this window will terminate
	the bot process immediately. Alternatively, typing Ctrl+C on your keyboard will safely terminate
	the bot client and end all tasks before exiting.
	- the `start.pyw` file is a wrapper that will run the `core.py` file in the background,
	allowing you to host the bot without an open command prompt window. Running this file
	will not open any windows and will not display any output. This version cannot be terminated
	without shutting down the host system.
	- Running either file via command line `python -m start` or `python -m core` will display
	debug output in the command prompt window.

2. The bot process will terminate when your system shuts down. In the event you need to restart the bot,
	simply restart your system and repeat step 6.

3. If you prefer to run the bot with a console window, which is useful when you are debugging,
	simply run the `core.py` file instead, or run the `start.pyw` or `core.py` files from the command line
	using the command `python -m start` or `python -m core`. Both of these options will perform the same way,
	allowing you to see the output of the bot in the console window, including informational and error messages.

Notes:
* Shutting your system down will terminate the running script. You will need to restart the
	script once your system has booted back up.

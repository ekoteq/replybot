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

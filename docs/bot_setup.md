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
	simply restart your system and repeat step 2.

3. If you prefer to run the bot with a console window, which is useful when you are debugging,
	simply run the `core.py` file instead, or run the `start.pyw` or `core.py` files from the command line
	using the command `python -m start` or `python -m core`. Both of these options will perform the same way,
	allowing you to see the output of the bot in the console window, including informational and error messages.

Notes:
* Shutting your system down will terminate the running script. You will need to restart the
	script once your system has booted back up.

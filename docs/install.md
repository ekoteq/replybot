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

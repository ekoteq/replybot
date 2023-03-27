# Quick Setup
This quick setup guide assumes you are using a system with a graphical interface and not a headless
unit that interfaces via the command-line only. This bot may run on either system, but the windowless
mode is not available for headless or command-line environments.

1. Install Python 3.11 if you have not already done so and restart.

2. Download a copy of this repository and save it somewhere.

3. Open a command prompt and run the following commands:
	1. `cd <path to bot folder>`

	2. OPTIONAL:
		1. `python -m pip install virtualenv`

		2. `virtualenv --python \path\to\python venv`

		3. `venv\Scripts\activate.bat`

	3. `python -m pip install -r requirements.txt`
	
4. Modify the .env and config.json files with relevant secrets and settings.

5. Right-click either the `start.pyw` or `core.py` files and open it with Python.

import ansi
import os

# Development Information
VERSION_INFO = f"{ansi.BLUE}{ansi.BOLD}v1.0.0 - Created by {ansi.ansi_link('https://github.com/narlock', 'narlock')}"

# Command Information
MENU_CONTROLS = f"""
1. Start pomo with previous setting.
2. Start pomo with saved setting.   
3. Start new pomo with new setting. 
4. Enter settings.                  
CTRL + C: Quit Pomo                 
"""
HELP_CMD = "-help"
HELP = f"""
Usage: pomo [args]\n
Where args include:\n
\t(no args)         Start pomo at main menu.
\t-p                Start pomo with previous setting.
\t-n                Enter new pomo creation.
\t-s                Enter settings.
\t<int>             Start single session pomo for <int> minutes.
\t<pomo_name>       Start pomo by pomo name.
\t-ls               View saved pomos.
\nView demonstration on {ansi.ansi_link('https://github.com/narlock/pomo', 'GitHub')}.
"""
POMO_CMD = "-p"
POMO_CREATE_CMD = "-n"
SETTINGS_CMD = "-s"
LIST_CMD = "-ls"

# Key binds
EXIT_CMD = "\x03"
KEY_1 = "1"
KEY_2 = "2"
KEY_3 = "3"
KEY_4 = "4"
KEY_5 = "5"
KEY_6 = "6"
KEY_7 = "7"
KEY_8 = "8"
KEY_9 = "9"
KEY_0 = "0"

# Storage information
STORAGE_DIR = os.path.expanduser("~/Documents/narlock/pomo")


CHOOSE_SELECTION = f"\n{ansi.YELLOW}Choose selection...{ansi.RESET} "
INVALID_SELECTION = f"\n{ansi.RED}Invalid option...{ansi.RESET} "
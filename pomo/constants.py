import ansi
import os
import re

def get_version_info(subtext_color_str: str = 'BLUE'):
    color = ansi.str_to_color(subtext_color_str)
    return f"{color}{ansi.BOLD}v1.0.0 - Created by {ansi.ansi_link('https://github.com/narlock', 'narlock')}" 

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

# Selection
CHOOSE_SELECTION = f"\n{ansi.YELLOW}Choose selection...{ansi.RESET} "
INVALID_SELECTION = f"\n{ansi.RED}Invalid option...{ansi.RESET} "

# Source
MAIN_MENU_SOURCE = 0
COMMAND_LINE_SOURCE = 1

# End options
MAIN_MENU_END_OPTION = 0
CONTINUE_TO_BREAK_END_OPTION = 1
CONTINUE_TO_NEXT_SESSION_END_OPTION = 2
TERMINATE_END_OPTION = 3

# Helper functions
CURRENT_SESSION_PLACEHOLDER = 'current_session'
TOTAL_SESSIONS_PLACEHOLDER = 'total_sessions'

def replace_placeholder(message: str, placeholder: str, replacement: str):
    pattern = r'\$\{' + re.escape(placeholder) + r'\}'
    return re.sub(pattern, replacement, message)

# Error messages
def POMO_NOT_FOUND(pomo_name: str):
    return f"{ansi.RED}Pomo `{pomo_name}` was not found Use `pomo -ls` to view pomos."
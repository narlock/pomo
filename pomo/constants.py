import ansi
import os
import re

def get_version_info(subtext_color_str: str = 'BLUE'):
    color = ansi.str_to_color(subtext_color_str)
    return f"{color}{ansi.BOLD}v1.0.0-beta.1 - Created by {ansi.ansi_link('https://github.com/narlock', 'narlock')}" 

# Command Information
MENU_CONTROLS = f"""
1. Start pomo with previous setting.
2. Start pomo with saved setting.   
3. Create new pomo.                 
4. Enter settings.                  
CTRL + C: Quit Pomo                 
"""
HELP_CMD = "-help"
HELP = f"""
Usage: pomo [args]\n
Where args include:\n
\t(no args)         Start pomo at main menu.
\t-p                Start pomo with previous setting.
\t<pomo_name>       Start pomo by pomo name.
\t<int>             Start single session pomo for <int> minutes.
\t-n                Enter new pomo creation.
\t-e <pomo_name>    Edit an existing pomo.
\t-d <pomo_name>    Delete an existing pomo.
\t-s                Enter settings.
\t-ls               View saved pomos.
\nView demonstration on {ansi.ansi_link('https://github.com/narlock/pomo', 'GitHub')}.
"""
POMO_CMD = "-p"
POMO_CREATE_CMD = "-n"
POMO_EDIT_CMD = "-e"
POMO_DELETE_CMD = "-d"
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
KEY_UP = "\x1b[A"
KEY_DOWN = "\x1b[B"
KEY_LEFT = "\x1b[D"
KEY_RIGHT = "\x1b[C"
KEY_ENTER = ('\r', '\n')
KEY_BACK = ('\x7f', '\x08')
EXIT_CMD = "\x03"  # Ctrl+C
KEY_DELETE = ("d", "D")
KEY_EDIT = ("e", "E")

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

# Pomo options
pomo_options = ['name', 'focusTime', 'shortBreak', 'shortBreakTime', 'sessionCount',
                'longBreak', 'longBreakTime', 'longBreakAfterSessions', 'autoStartNextSession',
                'autoStartBreak', 'playAlarmSound', 'alarmSound', 'timerEndFlash', 'sessionMessage',
                'breakMessage', 'longBreakMessage', 'borderColor', 'timeColor', 'subtextColor']

pomo_type_options = ['str', 'int', 'bool', 'int', 'int',
                     'bool', 'int', 'int-list', 'bool', 'bool',
                     'bool', 'str', 'bool', 'str', 'str', 'str',
                     'str', 'str', 'str']

# Main Menu Options
main_menu_options = ['title', 'borderColor', 'timeColor', 'subtextColor']
main_menu_type_options = ['str', 'str', 'str', 'str']

def get_pomo_option(index, pomo):
    return pomo[pomo_options[index]]
    
def get_pomo_key(index):
    return pomo_options[index]

POMO_STR_REGEX = r'^[A-Za-z0-9\s\-\_\.\$\{\}\!\@\#\%\^\&\*\(\)]+$'
POMO_INT_REGEX = r'^\d+$'
POMO_ALPHA_REGEX = r'^[A-Za-z]+$'

def get_comma_sep_string(list_of_int):
    return ', '.join(str(i) for i in list_of_int)

def parse_int_list(s):
    return [int(x.strip()) for x in s.split(',') if x.strip().isdigit()]

# Helper functions
CURRENT_SESSION_PLACEHOLDER = 'current_session'
TOTAL_SESSIONS_PLACEHOLDER = 'total_sessions'

def replace_placeholder(message: str, placeholder: str, replacement: str):
    pattern = r'\$\{' + re.escape(placeholder) + r'\}'
    return re.sub(pattern, replacement, message)

# Error messages
def POMO_NOT_FOUND(pomo_name: str):
    return f"{ansi.RED}Pomo `{pomo_name}` was not found Use `pomo -ls` to view pomos."
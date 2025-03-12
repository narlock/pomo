"""
Pomo - main.py
author: narlock

This is the main file for the Pomo application.
"""

import ansi
import countdown_timer
import sys
import os
import pomo_key

# Development Information
VERSION_INFO = f"{ansi.BLUE}{ansi.BOLD}v1.0.0 - Created by {ansi.ansi_link('https://github.com/narlock', 'narlock')}"

# Command Information
MENU_CONTROLS = f"""
1. Start pomo with previous setting.
2. Start new pomo with new setting. 
3. Enter settings.                  
CTRL + C: Quit Pomo                 
"""
HELP_CMD = "-help"
EXIT_CMD = "\x03"

# Storage information
STORAGE_DIR = os.path.expanduser("~/Documents/narlock/pomo")

# Other
POMO_ANSI = ["", "", "", "", ""]
for char in 'POMO':
    for i in range(5):
        POMO_ANSI[i] += ansi.ascii_letters[char][i] + "  "

def show_help():
    pass

def show_main_menu():
    os.system('clear')
    countdown_timer.draw_border(POMO_ANSI, VERSION_INFO)
    print(f"{ansi.RESET}{ansi.center_text(MENU_CONTROLS)}")
    print(f"\n{ansi.YELLOW}Choose selection...{ansi.RESET} ")
    key = pomo_key.get_keypress()

def main():
    args = sys.argv[1:]

    if not args:
        show_main_menu()
    elif args[0] == HELP_CMD:
        show_help()
    else:
        show_main_menu()

if __name__ == '__main__':
    main()
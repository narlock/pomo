"""
Pomo - main.py
author: narlock

This is the main file for the Pomo application.
"""

import ansi
import constants
import countdown_timer
import sys
import os
import pomo_key
import settings

# Other
POMO_ANSI = ["", "", "", "", ""]
for char in 'POMO':
    for i in range(5):
        POMO_ANSI[i] += ansi.ascii_letters[char][i] + "  "

def show_help():
    pass

def show_main_menu():
    user_settings = settings.load_settings()

    os.system('clear')
    countdown_timer.draw_border(POMO_ANSI, constants.VERSION_INFO)
    print(f"{ansi.RESET}{ansi.center_text(constants.MENU_CONTROLS)}")
    print(f"\n{ansi.YELLOW}Choose selection...{ansi.RESET} ")
    
    # Get user key press
    key = pomo_key.get_keypress()
    if key == constants.EXIT_CMD:
        # Exit the application
        print(f"{ansi.RED}Exiting Pomo...{ansi.RESET}")
        os.system('clear')
        sys.exit(0)
    elif key == constants.KEY_1:
        # Load and start previous pomodoro
        print(f"{ansi.GREEN}Starting previous pomodoro...{ansi.RESET}")
        os.system('clear')

        # TODO make this load from the settings
        countdown_timer.previous_pomodoro(user_settings)
        pass

def main():
    args = sys.argv[1:]

    if not args:
        show_main_menu()
    elif args[0] == constants.HELP_CMD:
        show_help()
    else:
        show_main_menu()

if __name__ == '__main__':
    main()
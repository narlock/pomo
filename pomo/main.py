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

user_settings = None

# Other
POMO_ANSI = ["", "", "", "", ""]
for char in 'POMO':
    for i in range(5):
        POMO_ANSI[i] += ansi.ascii_letters[char][i] + "  "

def show_help():
    print(constants.HELP)

def show_main_menu(selection=constants.CHOOSE_SELECTION):
    os.system('clear')
    countdown_timer.draw_border(POMO_ANSI, constants.VERSION_INFO)
    print(f"{ansi.RESET}{ansi.center_text(constants.MENU_CONTROLS)}")
    print(selection)
    
    # Get user key press
    key = pomo_key.get_keypress()
    if key == constants.EXIT_CMD:
        # Exit the application
        os.system('clear')
        print(f"{ansi.RED}Exiting Pomo...{ansi.RESET}")
        sys.exit(0)
    elif key == constants.KEY_1:
        # Load and start previous pomodoro
        print(f"{ansi.GREEN}Starting previous pomodoro...{ansi.RESET}")
        os.system('clear')

        # TODO make this load from the settings
        countdown_timer.previous_pomodoro(user_settings)
        pass
    else:
        show_main_menu(constants.INVALID_SELECTION)

def main():
    args = sys.argv[1:]

    # Load user settings
    global user_settings
    user_settings = settings.load_settings()

    if not args:
        show_main_menu()
    elif args[0] == constants.HELP_CMD:
        show_help()
    elif args[0] == constants.POMO_CREATE_CMD:
        # Enter Creation Menu
        print('Entering creation menu')
        pass
    elif args[0] == constants.SETTINGS_CMD:
        # Enter Settings Menu
        print('Entering settings menu')
        pass
    elif len(args) == 1 and args[0] == constants.POMO_CMD:
        # Start Pomo with previous setting.
        print('Entering pomo with previous setting')
        pass
    elif len(args) == 2 and args[0] == constants.POMO_CMD:
        # Start pomo with saved setting.
        print(f'Entering pomo with saved setting {args[1]}')
        pass
    elif len(args) == 1 and int(args[0]):
        # Start a pomodoro where args[0] is amount of time in minutes.
        minutes = int(args[0])
        print(f'Starting countdown timer with {minutes} minutes')
        countdown_timer.countdown_timer(minutes * 60)
    else:
        show_main_menu()

if __name__ == '__main__':
    main()
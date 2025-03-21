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
import re

user_settings = None

# Other
POMO_ANSI = ["", "", "", "", ""]
for char in 'POMO':
    for i in range(5):
        POMO_ANSI[i] += ansi.ascii_letters[char][i] + "  "

def show_help():
    print(constants.HELP)

def show_main_menu(selection: str = constants.CHOOSE_SELECTION, message: str = constants.get_version_info()):
    os.system('clear')
    countdown_timer.draw_countdown_timer(POMO_ANSI, message)
    print(f"{ansi.RESET}{ansi.center_text(constants.MENU_CONTROLS)}")
    print(selection)
    
    # Get user key press
    key = pomo_key.get_keypress()
    if key == constants.EXIT_CMD:
        # Exit the application
        os.system('clear')
        print(f"{ansi.GREEN}Exiting Pomo...{ansi.RESET}")
        sys.exit(0)
    elif key == constants.KEY_1:
        # Load and start previous pomodoro
        print(f"{ansi.GREEN}Starting previous pomodoro...{ansi.RESET}")
        os.system('clear')

        previous_pomo = user_settings['previousPomoName']
        countdown_timer.pomodoro_timer(name = previous_pomo, source = constants.MAIN_MENU_SOURCE)
    elif key == constants.KEY_2:
        # Display a list of saved settings, then start pomo
        show_saved_pomos()
    elif key == constants.KEY_3:
        show_pomo_create_menu()
    elif key == constants.KEY_5:
        # Debug
        message = user_settings.get('pomos')[0].get('sessionMessage')
        message = constants.replace_placeholder(message, constants.CURRENT_SESSION_PLACEHOLDER, str(1))
        print(message)
    else:
        show_main_menu(constants.INVALID_SELECTION)

def show_saved_pomos():
    selected_index = 0

    while True:
        os.system('clear')
        print(f"{ansi.ORANGE}{ansi.BOLD}Saved Pomos:{ansi.RESET}\n")
        for index, pomo in enumerate(user_settings['pomos']):
            if index == selected_index:
                print(f"{ansi.BRIGHT_GREEN}{ansi.BOLD}→ [{index}] {ansi.RESET}{get_pomo_info(pomo)}{ansi.RESET}")
            else:
                print(f"{ansi.GREEN}[{index}] {ansi.RESET}{get_pomo_info(pomo)}")
        print()

        key = pomo_key.get_keypress()

        if key == constants.KEY_UP:
            selected_index = (selected_index - 1) % len(user_settings['pomos'])
        elif key == constants.KEY_DOWN:
            selected_index = (selected_index + 1) % len(user_settings['pomos'])
        elif key == constants.KEY_DELETE:
            confirm = input(f"{ansi.YELLOW}{ansi.BOLD}Delete pomo \"{user_settings['pomos'][selected_index]['name']}\"? (y/N) ")
            if confirm == 'y' or confirm == 'Y':
                # Delete the pomo from the list
                del user_settings['pomos'][selected_index]
                settings.update_settings(user_settings)
                pass
        elif key in constants.KEY_ENTER:
            pomo_name = user_settings['pomos'][selected_index]['name']
            countdown_timer.pomodoro_timer(pomo_name)
            return
        elif key == constants.EXIT_CMD:
            os.system('clear')
            show_main_menu()
            return
        
def show_pomo_create_menu(pomo = None):
    selected_index = 0
    if pomo is None:
        pomo = settings.DEFAULT_POMO

    while True:
        os.system('clear')
        print(f"{ansi.ORANGE}{ansi.BOLD}Pomo Creation Interface:{ansi.RESET}\n")
        for index, option in enumerate(constants.pomo_options):
            if index == selected_index:
                print(f"{ansi.BRIGHT_GREEN}{ansi.BOLD}→ {option}: {ansi.RESET}{constants.get_pomo_option(index, pomo)}")
            else:
                print(f"{ansi.GREEN}{option}: {ansi.RESET}{constants.get_pomo_option(index, pomo)}")
        
        # Set option edit interface
        option_type = constants.pomo_type_options[selected_index]
        if option_type is not 'list':
            print(f"\n{ansi.YELLOW}Input ({option_type}):{ansi.RESET} {constants.get_pomo_option(selected_index, pomo)}", end="")
        else:
            list_content = ''
            for list_int in constants.get_pomo_option(selected_index, pomo):
                list_content += list_int + ","
            print(f"\n{ansi.YELLOW}Input ({option_type}):{ansi.RESET} {list_content}", end="")

        key = pomo_key.get_keypress()

        if key == constants.EXIT_CMD:
            show_main_menu()
            return
        elif key == constants.KEY_UP:
            selected_index = (selected_index - 1) % len(constants.pomo_options)
        elif key == constants.KEY_DOWN:
            selected_index = (selected_index + 1) % len(constants.pomo_options)
        elif key == constants.KEY_ENTER:
            # Save the pomo, ensure one with the same name does not exist
            pass

        # Determine key behavior based on option type
        if option_type == 'str':
            key_name = constants.pomo_options[selected_index]

            # Create string edit interface
            option_string = constants.get_pomo_option(selected_index, pomo)
            if key in constants.KEY_BACK:
                # Delete character from string if possible
                option_string = option_string[:-1]
                pomo[key_name] = option_string

        elif option_type == 'int':
            # Create int edit interface
            pass
        elif option_type == 'bool':
            # Create bool edit interface
            pass
        elif option_type == 'list':
            pass

def get_pomo_info(pomo):
    return f"{pomo['name']} — {pomo['sessionCount']} sessions, {int(int(pomo['focusTime']) / 60)}/{int(int(pomo['shortBreakTime']) / 60)}, long: {pomo['longBreakAfterSessions']}"

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
    elif args[0] == constants.LIST_CMD:
        # List the available pomos
        print(f"{ansi.GREEN}Pomos:{ansi.RESET} {settings.get_list_of_pomo_names(user_settings)}")
    elif len(args) == 1 and args[0] == constants.POMO_CMD:
        # Start Pomo with previous setting.
        countdown_timer.pomodoro_timer(user_settings.get('previousPomoName'), constants.COMMAND_LINE_SOURCE)
    elif len(args) == 2 and args[0] == constants.POMO_CMD:
        # Start pomo with saved setting.
        countdown_timer.pomodoro_timer(args[1], constants.COMMAND_LINE_SOURCE)
    elif len(args) == 1 and int(args[0]):
        # Start a pomodoro where args[0] is amount of time in minutes.
        minutes = int(args[0])
        print(f'Starting countdown timer with {minutes} minutes')
        countdown_timer.pomodoro_timer_global(minutes * 60)
    else:
        show_main_menu()

if __name__ == '__main__':
    main()
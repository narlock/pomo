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

user_settings = None # Global Settings
POMO_ANSI = None # Title Screen ANSI text

def show_help():
    """
    Prints out the options of the pomo command line
    application to the screen.
    """
    print(constants.HELP)

def show_main_menu(selection: str = constants.CHOOSE_SELECTION, message: str = constants.get_version_info()):
    """
    Displays the main menu of the pomo command line
    interface application to the screen.

    Uses the pomo_key.get_keypress function to get input
    from the user to determine the path to go in the
    application.
    """
    global user_settings
    user_settings = settings.load_settings()
    load_title()
    if message == constants.get_version_info():
        message = f"{constants.get_version_info(user_settings['mainMenu']['subtextColor'])}"

    os.system('clear')
    countdown_timer.draw_countdown_timer(POMO_ANSI, message, ansi.str_to_color(user_settings['mainMenu']['borderColor']), ansi.str_to_color(user_settings['mainMenu']['timeColor']))
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
    elif key == constants.KEY_4:
        show_settings(user_settings)
    elif key == constants.KEY_5:
        # Debug
        message = user_settings.get('pomos')[0].get('sessionMessage')
        message = constants.replace_placeholder(message, constants.CURRENT_SESSION_PLACEHOLDER, str(1))
        print(message)
    else:
        show_main_menu(constants.INVALID_SELECTION)

def show_saved_pomos():
    """
    Displays an interface that shows the pomos that are saved
    in the settings.json file in Documents/narlock/pomo/settings.json

    Users can...
        start a pomo session by pressing ENTER on their selected pomo.
        edit an existing pomo by pressing 'e' on their selected pomo.
        delete an existing pomo by pressing 'd' on their selected pomo.
    """
    selected_index = 0

    while True:
        os.system('clear')
        if len(user_settings['pomos']) > 1:
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
            elif key in constants.KEY_DELETE:
                confirm = input(f"{ansi.YELLOW}{ansi.BOLD}Delete pomo \"{user_settings['pomos'][selected_index]['name']}\"? (y/N) ")
                if confirm == 'y' or confirm == 'Y':
                    # Delete the pomo from the list
                    del user_settings['pomos'][selected_index]
                    settings.update_settings(user_settings)
                    selected_index = 0
            elif key in constants.KEY_EDIT:
                # Open creation interface with existing pomo
                pomo = user_settings['pomos'][selected_index]
                show_pomo_create_menu(pomo=pomo)
            elif key in constants.KEY_ENTER:
                pomo_name = user_settings['pomos'][selected_index]['name']
                countdown_timer.pomodoro_timer(user_settings=user_settings, name=pomo_name)
                return
            elif key == constants.EXIT_CMD:
                os.system('clear')
                show_main_menu()
                return
        else:
            print(f"{ansi.RED}{ansi.BOLD}No Saved Pomos.{ansi.RESET}\n")
            key = pomo_key.get_keypress()
            show_main_menu()
        
def show_pomo_create_menu(pomo = None, source = constants.MAIN_MENU_SOURCE):
    """
    Displays the inferface for creating or updating a pomo item.
    If pomo parameter is None, then we are creating a new pomo. Otherwise,
    we are updating an existing pomo item.
    """
    input_text = f"{ansi.YELLOW}Input (str):"
    selected_index = 0
    if pomo is None:
        header_message = f"{ansi.ORANGE}{ansi.BOLD}Pomo Creation Interface:{ansi.RESET}\n"
        existing_pomo = False
        pomo_index = -1
        pomo = settings.DEFAULT_POMO
        pomo['name'] = ''
    else:
        header_message = f"{ansi.ORANGE}{ansi.BOLD}Pomo Update Interface:{ansi.RESET}\n"
        existing_pomo = True
        pomo_index = settings.get_pomo_index_by_name(name=pomo['name'])

    while True:
        os.system('clear')
        print(header_message)
        for index, option in enumerate(constants.pomo_options):
            if index == selected_index:
                print(f"{ansi.BRIGHT_GREEN}{ansi.BOLD}→ {option}: {ansi.RESET}{constants.get_pomo_option(index, pomo)}")
            else:
                print(f"{ansi.GREEN}{option}: {ansi.RESET}{constants.get_pomo_option(index, pomo)}")
        
        # Set option edit interface
        option_type = constants.pomo_type_options[selected_index]
        if option_type != 'list':
            print(f"\n{input_text}{ansi.RESET} {constants.get_pomo_option(selected_index, pomo)}", end="")
        else:
            list_content = constants.get_comma_sep_string(constants.get_pomo_option(selected_index, pomo))
            print(f"\n{input_text}{ansi.RESET} {list_content}", end="")

        key = pomo_key.get_keypress()

        if key == constants.EXIT_CMD:
            show_main_menu()
            return
        elif key == constants.KEY_UP:
            input_text = f"{ansi.YELLOW}Input ({option_type}):"
            selected_index = (selected_index - 1) % len(constants.pomo_options)
            continue
        elif key == constants.KEY_DOWN:
            input_text = f"{ansi.YELLOW}Input ({option_type}):"
            selected_index = (selected_index + 1) % len(constants.pomo_options)
            continue
        elif key in constants.KEY_ENTER:
            # Validation
            if ''.join(pomo['name'].split()) == '':
                input_text = f"{ansi.RED}Name cannot be empty...{ansi.RESET}"
                continue
            elif pomo['name'] in [p['name'] for i, p in enumerate(user_settings['pomos']) if i != pomo_index]:
                input_text = f"{ansi.RED}Pomo with name \"{pomo['name']}\" already exists... Try a different name...{ansi.RESET}"
                continue
            elif pomo['borderColor'] not in ansi.VALID_COLORS:
                input_text = f"{ansi.RED}Invalid borderColor...{ansi.RESET}"
                continue
            elif pomo['timeColor'] not in ansi.VALID_COLORS:
                input_text = f"{ansi.RED}Invalid timeColor...{ansi.RESET}"
                continue
            elif pomo['subtextColor'] not in ansi.VALID_COLORS:
                input_text = f"{ansi.RED}Invalid subtextColor...{ansi.RESET}"
                continue
            elif pomo['alarmSound'] != 'Default':
                input_text = f"{ansi.RED}\"Default\" is the only supported alarmSound...{ansi.RESET}"
                continue

            os.system('clear')
            # Save and start
            if not existing_pomo:
                user_settings['pomos'].append(pomo)
                message = f"{ansi.GREEN}{ansi.BOLD}The pomo \"{pomo['name']}\" was created!{ansi.RESET}"
            else:
                message = f"{ansi.GREEN}{ansi.BOLD}The pomo \"{pomo['name']}\" was updated!{ansi.RESET}"

            settings.update_settings(user_settings)
            if source == constants.MAIN_MENU_SOURCE:
                show_main_menu(message=message)
                return
            else:
                return

        key_name = constants.pomo_options[selected_index]
        input_text = f"{ansi.YELLOW}Input ({option_type}):"

        # Determine key behavior based on option type
        if option_type == 'str':
            # Create string edit interface
            option_string = constants.get_pomo_option(selected_index, pomo)
            if key in constants.KEY_BACK:
                # Delete character from string if possible
                option_string = option_string[:-1]
                pomo[key_name] = option_string
            elif re.fullmatch(constants.POMO_STR_REGEX, key):
                # Add character from string
                option_string += key
                pomo[key_name] = option_string
        elif option_type == 'int':
            # Create int edit interface
            option_string = str(constants.get_pomo_option(selected_index, pomo))
            if key in constants.KEY_BACK:
                # Delete character from string if possible
                option_string = option_string[:-1]
                pomo[key_name] = option_string
            elif re.fullmatch(constants.POMO_INT_REGEX, key):
                # Add character from string
                option_string += key
                pomo[key_name] = int(option_string)
        elif option_type == 'bool':
            option_bool = constants.get_pomo_option(selected_index, pomo)
            # Create bool edit interface
            if key == constants.KEY_LEFT or key == constants.KEY_RIGHT:
                pomo[key_name] = not option_bool
        elif option_type == 'int-list':
            # Allow for integers that are command separated
            option_string = constants.get_comma_sep_string(constants.get_pomo_option(selected_index, pomo))

            if key in constants.KEY_BACK:
                # handle back
                option_string = option_string[:-1]
                pomo[key_name] = constants.parse_int_list(option_string)
            elif key == ',':
                option_string += f", 0"
                pomo[key_name] = constants.parse_int_list(option_string)
            elif re.fullmatch(constants.POMO_INT_REGEX, key):
                # Add character from string
                option_string += key
                pomo[key_name] = constants.parse_int_list(option_string)
            
        print(pomo)

def get_pomo_info(pomo):
    """
    Retrieves a formatted information string for a pomo
    """
    return f"{pomo['name']} — {pomo['sessionCount']} sessions, {int(int(pomo['focusTime']) / 60)}/{int(int(pomo['shortBreakTime']) / 60)}, long: {pomo['longBreakAfterSessions']}"

def show_settings(user_settings, source = constants.MAIN_MENU_SOURCE):
    """
    Displays the interface for settings. This is a navigation screen
    that allows the user to select what settings they want to change.
    """
    selected_index = 0
    settings_size = 2 # Main menu and fast countdown are the only settings as of now

    while True:
        os.system('clear')
        print(f"{ansi.ORANGE}{ansi.BOLD}Settings:{ansi.RESET}\n")

        # Show main menu settings option
        if selected_index == 0:
            # Main menu setting is selected
            print(f"{ansi.BRIGHT_GREEN}{ansi.BOLD}→ Main Menu Settings{ansi.RESET}")
        else:
            # Main menu setting is NOT selected
            print(f"{ansi.GREEN}Main Menu Settings{ansi.RESET}")

        # Show fast countdown settings option
        if selected_index == 1:
            # Fast countdown setting is selected
            print(f"{ansi.BRIGHT_GREEN}{ansi.BOLD}→ Fast Countdown Settings{ansi.RESET}")
        else:
            # Fast countdown setting is NOT selected
            print(f"{ansi.GREEN}Fast Countdown Settings{ansi.RESET}")

        print()
        key = pomo_key.get_keypress()
        
        if key == constants.EXIT_CMD:
            if source == constants.MAIN_MENU_SOURCE:
                show_main_menu()
            else:
                os.system('clear')
                print(f"{ansi.GREEN}Exiting Pomo...{ansi.RESET}")
            return
        if key == constants.KEY_UP:
            selected_index = (selected_index - 1) % settings_size
        if key == constants.KEY_DOWN:
            selected_index = (selected_index + 1) % settings_size
        if key in constants.KEY_ENTER:
            if selected_index == 1:
                show_countdown_edit_settings(user_settings)
                return
            else:
                show_main_menu_edit_settings(user_settings, source)
                return

def show_main_menu_edit_settings(user_settings, source = constants.MAIN_MENU_SOURCE):
    """
    Displays the interface for editing the main menu settings
    """
    input_text = f"{ansi.YELLOW}Input (str):"
    selected_index = 0
    main_menu_settings_size = len(user_settings['mainMenu'])

    while True:
        os.system('clear')
        print(f"{ansi.ORANGE}{ansi.BOLD}Main Menu Settings:{ansi.RESET}\n")

        # Show the menu options
        for index, option in enumerate(user_settings['mainMenu']):
            if index == selected_index:
                print(f"{ansi.BRIGHT_GREEN}{ansi.BOLD}→ {option}: {ansi.RESET}{user_settings['mainMenu'][option]}")
            else:
                print(f"{ansi.GREEN}{option}: {ansi.RESET}{user_settings['mainMenu'][option]}")

        # Display Input
        print(f"\n{input_text} {ansi.RESET}{user_settings['mainMenu'][constants.main_menu_options[selected_index]]}", end='')
        option_type = constants.main_menu_type_options[selected_index]
        key = pomo_key.get_keypress()

        if key == constants.EXIT_CMD:
            if source == constants.MAIN_MENU_SOURCE:
                show_settings(user_settings)
            else:
                os.system('clear')
                print(f"{ansi.GREEN}Exiting Pomo...{ansi.RESET}")
            return
        elif key == constants.KEY_UP:
            selected_index = (selected_index - 1) % main_menu_settings_size
        elif key == constants.KEY_DOWN:
            selected_index = (selected_index + 1) % main_menu_settings_size
        elif key in constants.KEY_ENTER:
            # Save settings and return to show_settings

            # Validation
            if ''.join(user_settings['mainMenu']['title'].split()) == '':
                input_text = f"{ansi.RED}Title cannot be empty...{ansi.RESET}"
                continue
            if len(user_settings['mainMenu']['title']) > 6:
                input_text = f"{ansi.RED}Title cannot be larger than 6 characters...{ansi.RESET}"
                continue
            elif user_settings['mainMenu']['borderColor'] not in ansi.VALID_COLORS:
                input_text = f"{ansi.RED}Invalid borderColor...{ansi.RESET}"
                continue
            elif user_settings['mainMenu']['timeColor'] not in ansi.VALID_COLORS:
                input_text = f"{ansi.RED}Invalid timeColor...{ansi.RESET}"
                continue
            elif user_settings['mainMenu']['subtextColor'] not in ansi.VALID_COLORS:
                input_text = f"{ansi.RED}Invalid subtextColor...{ansi.RESET}"
                continue

            settings.update_settings(user_settings)
            show_settings(user_settings, source)
            return
        
        input_text = f"{ansi.YELLOW}Input ({option_type}):"
        key_name = constants.main_menu_options[selected_index]

        if option_type == 'str':
            # Create string edit interface
            option_string = user_settings['mainMenu'][key_name]
            if key in constants.KEY_BACK:
                # Delete character from string if possible
                option_string = option_string[:-1]
                user_settings['mainMenu'][key_name] = option_string
            elif re.fullmatch(constants.POMO_ALPHA_REGEX, key):
                # Add character from string
                option_string += key.upper()
                user_settings['mainMenu'][key_name] = option_string

def show_countdown_edit_settings(user_settings, source = constants.MAIN_MENU_SOURCE):
    """
    Displays the interface for editing the fast countdown settings
    """
    input_text = f"{ansi.YELLOW}Input (str):"
    selected_index = 0
    countdown_settings_size = len(user_settings['countdown'])

    while True:
        os.system('clear')
        print(f"{ansi.ORANGE}{ansi.BOLD}Fast Countdown Menu Settings:{ansi.RESET}\n")

        # Show the menu options
        for index, option in enumerate(user_settings['countdown']):
            if index == selected_index:
                print(f"{ansi.BRIGHT_GREEN}{ansi.BOLD}→ {option}: {ansi.RESET}{user_settings['countdown'][option]}")
            else:
                print(f"{ansi.GREEN}{option}: {ansi.RESET}{user_settings['countdown'][option]}")

        # Display Input
        print(f"\n{input_text} {ansi.RESET}{user_settings['countdown'][constants.countdown_options[selected_index]]}", end='')
        option_type = constants.countdown_type_options[selected_index]
        key = pomo_key.get_keypress()

        if key == constants.EXIT_CMD:
            if source == constants.MAIN_MENU_SOURCE:
                show_settings(source)
            else:
                os.system('clear')
                print(f"{ansi.GREEN}Exiting Pomo...{ansi.RESET}")
            return
        elif key == constants.KEY_UP:
            selected_index = (selected_index - 1) % countdown_settings_size
        elif key == constants.KEY_DOWN:
            selected_index = (selected_index + 1) % countdown_settings_size
        elif key in constants.KEY_ENTER:
            # Validation
            if user_settings['countdown']['alarmSound'] != 'Default':
                input_text = f"{ansi.RED}\"Default\" is the only supported alarmSound...{ansi.RESET}"
                continue
            elif user_settings['countdown']['borderColor'] not in ansi.VALID_COLORS:
                input_text = f"{ansi.RED}Invalid borderColor...{ansi.RESET}"
                continue
            elif user_settings['countdown']['timeColor'] not in ansi.VALID_COLORS:
                input_text = f"{ansi.RED}Invalid timeColor...{ansi.RESET}"
                continue
            elif user_settings['countdown']['subtextColor'] not in ansi.VALID_COLORS:
                input_text = f"{ansi.RED}Invalid subtextColor...{ansi.RESET}"
                continue

            settings.update_settings(user_settings)
            show_settings(user_settings, source)
            return
        
        input_text = f"{ansi.YELLOW}Input ({option_type}):"
        key_name = constants.countdown_options[selected_index]

        if option_type == 'str':
            # Create string edit interface
            option_string = user_settings['countdown'][key_name]
            if key in constants.KEY_BACK:
                # Delete character from string if possible
                option_string = option_string[:-1]
                user_settings['countdown'][key_name] = option_string
            elif re.fullmatch(constants.POMO_STR_REGEX, key):
                # Add character from string
                option_string += key
                user_settings['countdown'][key_name] = option_string
        elif option_type == 'bool':
            option_bool = user_settings['countdown'][key_name]
            # Create bool edit interface
            if key == constants.KEY_LEFT or key == constants.KEY_RIGHT:
                user_settings['countdown'][key_name] = not option_bool

def main():
    args = sys.argv[1:]

    # Load user settings
    global user_settings
    user_settings = settings.load_settings()
    load_title()

    if not args:
        show_main_menu()
    elif args[0] == constants.HELP_CMD:
        show_help()
    elif args[0] == constants.POMO_CREATE_CMD:
        # Enter Creation Menu
        show_pomo_create_menu(source=constants.COMMAND_LINE_SOURCE)
    elif args[0] == constants.SETTINGS_CMD:
        # Enter Settings Menu
        show_settings(user_settings, constants.COMMAND_LINE_SOURCE)
    elif args[0] == constants.LIST_CMD:
        # List the available pomos
        print(f"{ansi.GREEN}Pomos:{ansi.RESET} {settings.get_list_of_pomo_names(user_settings)}")
    elif len(args) == 1 and args[0] == constants.POMO_CMD:
        # Start Pomo with previous setting.
        countdown_timer.pomodoro_timer(user_settings.get('previousPomoName'), constants.COMMAND_LINE_SOURCE)
    elif len(args) == 2 and args[0] == constants.POMO_CMD:
        # Start pomo with saved setting.
        countdown_timer.pomodoro_timer(args[1], constants.COMMAND_LINE_SOURCE)
    elif len(args) == 2 and args[0] == constants.POMO_EDIT_CMD:
        # Enter edit mode with existing pomo where args[1] is pomo
        pomo_index = settings.get_pomo_index_by_name(name=args[1])

        # Ensure the pomo is not none
        if pomo_index == -1:
            print(constants.POMO_NOT_FOUND(args[1])) 
            return
        
        pomo = user_settings['pomos'][pomo_index] # Reference user_settings pomo
        show_pomo_create_menu(pomo=pomo, source=constants.COMMAND_LINE_SOURCE)
    elif len(args) == 2 and args[0] == constants.POMO_DELETE_CMD:
        # Delete the pomo with the name in args[1]
        pomo_index = settings.get_pomo_index_by_name(name=args[1])
        
        # Ensure the pomo is not none
        if pomo_index == -1:
            print(constants.POMO_NOT_FOUND(args[1])) 
            return
        
        confirm = input(f"{ansi.YELLOW}{ansi.BOLD}Delete pomo \"{user_settings['pomos'][pomo_index]['name']}\"? (y/N) ")
        if confirm == 'y' or confirm == 'Y':
            del user_settings['pomos'][pomo_index]
            settings.update_settings(user_settings)
            print(f"{ansi.GREEN}Pomo {args[1]} was deleted...")
            return
        else:
            print(f"{ansi.YELLOW}Canceled deletion...")
            return
    elif len(args) == 1 and int(args[0]):
        # Start a pomodoro where args[0] is amount of time in minutes.
        minutes = int(args[0])
        print(f'Starting countdown timer with {minutes} minutes')
        countdown_timer.pomodoro_timer_global(minutes * 60)
    else:
        show_main_menu()

def load_title():
    global POMO_ANSI
    ascii_height = len(ansi.ascii_letters['P'])  # Assuming all letters have the same height
    POMO_ANSI = [""] * ascii_height

    for char in user_settings['mainMenu']['title']:
        for i in range(ascii_height):
            POMO_ANSI[i] += ansi.ascii_letters[char][i] + "  "

if __name__ == '__main__':
    main()
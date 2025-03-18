import main
import ansi
import time
import os
import sys
import threading
import subprocess
import signal
import settings
import constants
import multiprocessing
import sfx.play_audio

WAV_FILE = "DEFAULT_ALARM.wav"

stop_event = threading.Event()  # Shared stop event for graceful shutdown
sound_process = None  # To track sound subprocess

pomo = None
pomo_source = constants.COMMAND_LINE_SOURCE
sessions = 0
current_session = 0
isBreak = False

def draw_border(content, message: str = None, border_color = ansi.RED, text_color = ansi.YELLOW):
    """Draws a box border around the ASCII time display, centered both horizontally and vertically."""
    width = len(content[0]) + 3  # Box width
    height = len(content) + 4  # Box height (including top & bottom padding)
    
    term_width, term_height = ansi.get_terminal_size()

    # Calculate left padding for centering horizontally
    left_padding = max((term_width - width) // 2, 0)
    padding_x = " " * left_padding

    # Calculate top padding for centering vertically, leaving room for the acknowledgment message
    top_padding = max((term_height - height - 3) // 2, 0)  # Subtract space for the message
    print("\n" * top_padding, end="")  # Add vertical padding

    # Draw border
    border_top = padding_x + "┌" + "─" * width + "┐"
    border_bottom = padding_x + "└" + "─" * width + "┘"

    print(ansi.RESET + border_color + border_top + ansi.RESET)
    print(padding_x + border_color + f"│{' ' * width}│" + ansi.RESET)  # Top padding
    for line in content:
        print(padding_x + border_color + f"│  {text_color}{line}{border_color} │" + ansi.RESET)  # Keep clock ANSI colors
    print(padding_x + border_color + f"│{' ' * width}│" + ansi.RESET)  # Bottom padding
    print(border_color + border_bottom + ansi.RESET)

    # Display the message centered below the timer
    if message:
        if pomo:
            # Format message to include current session if ${current_session} is present.
            message = constants.replace_placeholder(message, constants.CURRENT_SESSION_PLACEHOLDER, str(current_session + 1))
            # Format message to include total session if ${total_sessions} is present.
            message = constants.replace_placeholder(message, constants.TOTAL_SESSIONS_PLACEHOLDER, str(pomo.get('sessionCount', 1)))
            print("\n" + f"{ansi.str_to_color(pomo.get('color')['subtext'])}{ansi.BOLD}{ansi.center_text(message)}")
        else:
            print("\n" + f"{ansi.BOLD}{ansi.center_text(message)}")

def generate_ascii_time(minutes, seconds):
    """Generates the ASCII representation of the time (MM:SS)."""
    time_str = f"{minutes:02}:{seconds:02}"
    ascii_lines = ["", "", "", "", ""]

    for char in time_str:
        for i in range(5):
            ascii_lines[i] += ansi.ascii_numbers[char][i] + "  "  # Obtain each line of ASCII art

    return ascii_lines

def handle_resize(signum, frame):
    """Handles terminal resize events (SIGWINCH)."""
    os.system("clear" if os.name == "posix" else "cls")  # Clear screen
    draw_border(generate_ascii_time(0, 0), "Focusing...")  # Redraw the timer after resize

# TODO move this so that it only resizes here when timer is active.
# Register SIGWINCH signal handler (Unix only)
# signal.signal(signal.SIGWINCH, handle_resize)

def handle_exit(signum, frame):
    """Handles exit signals (SIGINT, SIGHUP, SIGTERM) and ensures proper cleanup."""
    print("\nReceived exit signal, cleaning up...")

    # Stop flashing alert
    stop_event.set()

    # Terminate sound process if running
    global sound_process
    if sound_process and sound_process.poll() is None:
        os.kill(sound_process.pid, signal.SIGTERM)

    # Clear screen before exiting (optional)
    os.system("clear" if os.name == "posix" else "cls")

    # TODO track the amount of time in either focus or break time and ensure we track that time and session.
    # If we only focused and did not do the break, the breakTime will be 0 for the session.

    print(f"{ansi.GREEN}Exited pomo...\nFocus/Break time saved to disk.")
    # TODO modify this so that we only close if the context was opened directly from the CLI
    # If the context was opened using the main menu, instead of exiting, we will call main.show_main_menu
    sys.exit(0)  # Ensure a clean exit

# Register signal handlers
signal.signal(signal.SIGINT, handle_exit)   # Handle Ctrl+C
signal.signal(signal.SIGHUP, handle_exit)   # Handle terminal close (Unix)
signal.signal(signal.SIGTERM, handle_exit)  # Handle kill command

def flashing_alert():
    """Flashes the screen repeatedly showing 00:00 until the user presses Enter."""
    message = "Press ENTER to acknowledge..."
    
    if pomo and isBreak:
        message = "Break is over!"
    elif pomo and not isBreak:
        message = "Session is over!"

    def flash():
        while not stop_event.is_set():
            if not pomo:
                for color in [ansi.RED, ansi.WHITE]:  # Alternate between red and white
                    if stop_event.is_set():
                        return  # Stop flashing immediately if flag is set
                    os.system('clear')
                    draw_border(generate_ascii_time(0, 0), f"{ansi.BLUE}{message}", border_color=color)
                    time.sleep(0.5)  # Adjust flash speed
            else:
               for color in [ansi.str_to_color(pomo['color']['border']), ansi.WHITE]:  # Alternate between red and white
                    if stop_event.is_set():
                        return  # Stop flashing immediately if flag is set
                    os.system('clear')
                    draw_border(generate_ascii_time(0, 0), f"{ansi.str_to_color(pomo['color']['subtext'])}{message}", border_color=color, text_color=ansi.str_to_color(pomo['color']['time']))
                    time.sleep(0.5)  # Adjust flash speed 

    flash_thread = threading.Thread(target=flash, daemon=True)
    flash_thread.start()

def countdown_end(option: int = constants.MAIN_MENU_END_OPTION):
    """Plays an alarm with both flashing and sound, stopping when user presses ENTER."""
    global isBreak
    global current_session
    global isBreak

    stop_event.clear()

    # Start flashing and playing sound in parallel
    flashing_alert()
    sound_process = multiprocessing.Process(sfx.play_audio.play_sound(), daemon=True)
    sound_process.start()

    # Wait for user input and stop everything
    input()
    stop_event.set()
    sfx.play_audio.kill_processes()
    os.kill(sound_process.pid, signal.SIGTERM)

    if option == constants.MAIN_MENU_END_OPTION:
        main.show_main_menu(message = "Timer ended!")
    elif pomo and option == constants.CONTINUE_TO_BREAK_END_OPTION:
        # continue to next break       
        isBreak = True

        # TODO if the current session is the final session, end the pomo.

        # TODO determine that if the current_session is a long break, use long break for next countdown timer call
        countdown_timer(pomo.get('shortBreakTime'), pomo.get('breakMessage'), constants.CONTINUE_TO_NEXT_SESSION_END_OPTION)

    elif pomo and option == constants.CONTINUE_TO_NEXT_SESSION_END_OPTION:
        # continue to next focus session
        isBreak = False
        current_session = current_session + 1

        if current_session == sessions:
            # End the pomo
            if pomo_source and pomo_source == constants.MAIN_MENU_SOURCE:
                # TODO add more verbose pomo complete message... including total focus time?
                main.show_main_menu(constants.CHOOSE_SELECTION, f'{ansi.GREEN}{ansi.BOLD}Pomo Completed!')
            else:
                os.system('clear')
                print(f"{ansi.GREEN}Pomo Completed!")
        else:
            countdown_timer(pomo.get('focusTime'), pomo.get('sessionMessage'), constants.CONTINUE_TO_BREAK_END_OPTION)
    else:
        print(f"{ansi.RESET}\nTimer acknowledged. Exiting...\n")

def countdown_timer(total_seconds: int, message: str = "Focusing...", end_option: int = 3):
    """
    Runs a countdown timer for the specified duration.

    Args:
        total_seconds (int): The total duration of the countdown in seconds.
        message (str, optional): A custom message to display during the countdown.
                                 Defaults to "Focusing...".
        end_option (int, optional): Determine what happens after `countdown_end` function
                            is called.
                    - `0` -> Displays the main menu after the countdown timer is complete.
                    - `1` -> Continues to the break after the session is complete.
                    - `2` -> Continues to the next session after a break is complete.
                    - `3` -> Exits the program after the countdown timer is complete.

    Functionality:
        - Iterates from `total_seconds` down to 0, updating the display every second.
        - Clears the screen before updating the countdown display.
        - Uses `generate_ascii_time(minutes, seconds)` to format the time.
        - Calls `draw_border()` to render the countdown with the provided message.
        - After the countdown reaches zero, clears the screen and calls `countdown_end(3)`,
          which presumably handles the timer completion visuals or alerts.
    """
    for remaining in range(total_seconds, -1, -1):
        minutes = remaining // 60
        seconds = remaining % 60
        os.system("clear" if os.name == "posix" else "cls")  # Clear screen
        if not pomo:
            draw_border(generate_ascii_time(minutes, seconds), message)
        else:
            draw_border(generate_ascii_time(minutes, seconds), message, ansi.str_to_color(pomo['color']['border']), ansi.str_to_color(pomo['color']['time']))
        time.sleep(1)

    os.system("clear" if os.name == "posix" else "cls")  # Clear screen before flashing
    countdown_end(end_option)

def pomodoro_timer(name: str, source: int = constants.MAIN_MENU_SOURCE):
    """
    Runs a Pomodoro timer based on the provided name.

    Args:
        name (str): The name of the Pomodoro session to start.
        source (int, optional): Indicates where this function was called from.
            - `0` (default) -> Called from the Main Menu.
                - Redirects errors back to the main menu.
            - `1` -> Called directly from the CLI.
                - Prints errors to the CLI and stops the program.

    Functionality:
        - Reads the list of Pomodoros from the settings file located at:
          `$HOME/Documents/narlock/pomo/settings.json`.
        - If the specified Pomodoro name is not found in the "pomos" list,
          an error message is returned.
        - If found, initializes the global variables:
            - `sessions`
            - `current_session`
            - `isBreak`
        - Calls `countdown_timer()` to begin the first Pomodoro session.
        - After all work sessions are complete, checks if a break is required.
          If so, sets `isBreak` to `True` and calls `countdown_timer()` to start the break.
    """
    global pomo
    global pomo_source
    pomo = settings.get_pomo(name = name)
    pomo_source = source

    # Check if the pomo is not found
    if pomo is None:
        handle_pomo_not_found(name, pomo_source)
        return

    # Initialize pomodoro settings
    global sessions
    global current_session
    global isBreak

    sessions = pomo.get('sessionCount', 1)
    current_session = 0
    isBreak = False
    
    # Begin pomodoro
    countdown_timer(pomo.get('focusTime'), pomo.get('sessionMessage'), constants.CONTINUE_TO_BREAK_END_OPTION)

def handle_pomo_not_found(name: str, source: int):
    """
    Handles how the program will operate after a pomo has been requested that 
    does not exist in the current settings.

    """
    if source == 0:
        # Redirect to main menu
        main.show_main_menu(message = constants.POMO_NOT_FOUND(name))
    else:
        # Terminate the program
       print(constants.POMO_NOT_FOUND(name)) 
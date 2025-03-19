import main
import ansi
import time
import os
import sys
import signal
import settings
import constants
import multiprocessing
import subprocess
import termios

# Active Pomo Information
pomo = None
pomo_source = constants.COMMAND_LINE_SOURCE
sessions = 0
current_session = 0
isBreak = False

def generate_ascii_time(minutes, seconds):
    """
    Generates the ASCII representation of the time (MM:SS).
    Used for providing the `content` to the draw_border method.

    The content of the ascii_lines are created based on the ascii
    representations in the ansi.py file. It will read in the horizontal
    lines from each of the numbers and append them together so that
    when we print them to the console, we will be printing line by line.
    """
    time_str = f"{minutes:02}:{seconds:02}"
    ascii_lines = ["", "", "", "", ""]

    for char in time_str:
        for i in range(5):
            ascii_lines[i] += ansi.ascii_numbers[char][i] + "  "  # Obtain each line of ASCII art

    return ascii_lines

def draw_countdown_timer(ascii_lines, message: str = None, border_color = ansi.RED, text_color = ansi.YELLOW):
    """
    Draws a box border around the ASCII time display, centered both horizontally and vertically.
    draw_border is called every second that the countdown timer runs. It scales if there are any
    resizing that occurs.
    """
    width = len(ascii_lines[0]) + 3  # Box width
    height = len(ascii_lines) + 4  # Box height (including top & bottom padding)
    
    term_width, term_height = ansi.get_terminal_size() # Retrieves the terminal size to ensure print is in middle

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
    for line in ascii_lines:
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

def draw_countdown_timer_end():
    """
    Draws a flashing countdown timer (if in pomo)
    Indicates to the user that the timer is ended.
    """
    global isBreak
    message = "Break Over!" if isBreak else "Session Over!"

    flash_color = 0

    while True:
        os.system("clear" if os.name == "posix" else "cls")  # Clear screen
        
        # Change flash color
        if flash_color == 0:
            draw_countdown_timer(generate_ascii_time(0, 0), message, ansi.WHITE, ansi.str_to_color(pomo['color']['time']))
            flash_color = 1
        else:
            draw_countdown_timer(generate_ascii_time(0, 0), message, ansi.str_to_color(pomo['color']['border']), ansi.str_to_color(pomo['color']['time']))
            flash_color = 0

        # Repeat every second
        time.sleep(1)

def play_audio_end(file: str = "DEFAULT_ALARM.wav"):
    """
    Plays the audio after the countdown timer ends.
    """
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    audio_file = os.path.join(script_dir, "sfx", "DEFAULT_ALARM.wav")

    # Continuously loop audio track
    try:
        while True:
            if sys.platform == 'darwin':  # macOS
                audio_process = subprocess.Popen(["afplay", audio_file], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            else:  # Linux
                audio_process = subprocess.Popen(["aplay", audio_file], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            # Ensures the audio finishes before replaying
            audio_process.wait()
    except KeyboardInterrupt:
        pass # Allows for graceful termination
    finally:
        try:
            audio_process.terminate()
        except:
            pass # Process may already be dead

# track child processes: flashing screen, playing audio, etc.
child_processes = []

def handle_exit(signum, frame):
    """
    Handles exit signals (SIGINT, SIGHUP, SIGTERM) and ensures proper cleanup.
    """
    print("\nReceived exit signal, cleaning up...")

    if multiprocessing.current_process().name == "MainProcess":
        for process in child_processes:
            if process.is_alive():
                print(f"Terminating child process: {process.pid}")
                process.terminate()
                process.join()

    # Clear screen before exiting (optional)
    os.system("clear" if os.name == "posix" else "cls")

    # TODO track the amount of time in either focus or break time and ensure we track that time and session.
    # If we only focused and did not do the break, the breakTime will be 0 for the session.

    print(f"{ansi.GREEN}Exited pomo...\nFocus/Break time saved to disk.")
    # TODO modify this so that we only close if the context was opened directly from the CLI
    # If the context was opened using the main menu, instead of exiting, we will call main.show_main_menu
    sys.exit(0)  # Ensure a clean exit

# Register signal handlers to handle_exit function
signal.signal(signal.SIGINT, handle_exit)   # Handle Ctrl+C
signal.signal(signal.SIGHUP, handle_exit)   # Handle terminal close (Unix)
signal.signal(signal.SIGTERM, handle_exit)  # Handle kill command

def countdown_end(option: int = constants.MAIN_MENU_END_OPTION):
    """
    The function that is called after the countdown timer is over. This
    function determines what to do when the countdown timer is over based on
    the option that is passed.

    Args:
    option
        - `0` (default) -> Displays the main menu after the countdown timer is complete.
        - `1` -> Continues to the break after the session is complete.
        - `2` -> Continues to the next session after a break is complete.
        - `3` -> Exits the program after the countdown timer is complete.
    """
    global flashing_process
    global isBreak
    global current_session

    # Sessions will automatically start after the break if enabled
    dontAutoStartNextSession = not (pomo['autoStartNextSession'] and option == constants.CONTINUE_TO_NEXT_SESSION_END_OPTION)
    dontAutoStartBreak = not (pomo['autoStartBreak'] and option == constants.CONTINUE_TO_BREAK_END_OPTION)

    if dontAutoStartNextSession == True and dontAutoStartBreak == True:
        # Draw flashing animation
        if pomo['timerEndFlash'] == True:
            flashing_process = multiprocessing.Process(target=draw_countdown_timer_end, daemon=True)
            flashing_process.start()
            child_processes.append(flashing_process)
        else:
            message = "Break Over!" if isBreak else "Session Over!"
            draw_countdown_timer(generate_ascii_time(0, 0), message, ansi.str_to_color(pomo['color']['border']), ansi.str_to_color(pomo['color']['time']))

        # Start Audio process
        if pomo['playAlarmSound'] == True:
            audio_multiprocess = multiprocessing.Process(target=play_audio_end, daemon=True)
            audio_multiprocess.start()
            child_processes.append(audio_multiprocess)

        # Wait for the user to hit ENTER before continuing...
        termios.tcflush(sys.stdin, termios.TCIFLUSH) # Flushes the input buffer
        input()

        # Terminate the process
        if pomo['timerEndFlash'] == True:
            flashing_process.terminate()
            flashing_process.join()

        if pomo['playAlarmSound'] == True:
            audio_multiprocess.terminate()
            audio_multiprocess.join()

        # Ensure child processes are terminated
        if multiprocessing.current_process().name == "MainProcess":
            for process in child_processes:
                if process.is_alive():
                    print(f"Terminating child process: {process.pid}")
                    process.terminate()
                    process.join()

    if option == constants.MAIN_MENU_END_OPTION:
        # Go back to the main menu of the program
        main.show_main_menu(message = "Timer ended!")
    elif pomo and option == constants.CONTINUE_TO_BREAK_END_OPTION:
        # Continue to next break       
        isBreak = True

        # If the current session is the final session, end the pomo.
        if current_session + 1 == sessions:
            # End the pomo
            if pomo_source and pomo_source == constants.MAIN_MENU_SOURCE:
                # TODO add more verbose pomo complete message... including total focus time?
                # TODO add focus time
                main.show_main_menu(constants.CHOOSE_SELECTION, f'{ansi.GREEN}{ansi.BOLD}Pomo Completed!')
            else:
                # TODO add focus time
                os.system('clear')
                print(f"{ansi.GREEN}Pomo Completed!")
        else:
            if pomo['longBreak'] and (current_session + 1) in pomo['longBreakAfterSessions']:
                # Enter a long break
                # TODO add focus time
                countdown_timer(pomo.get('longBreakTime'), pomo.get('longBreakMessage'), constants.CONTINUE_TO_NEXT_SESSION_END_OPTION)
            elif pomo['shortBreak']:
                # TODO determine that if the current_session is a long break, use long break for next countdown timer call
                countdown_timer(pomo.get('shortBreakTime'), pomo.get('breakMessage'), constants.CONTINUE_TO_NEXT_SESSION_END_OPTION)
            else:
                # Immediately go to the next session
                isBreak = False
                current_session = current_session + 1
                countdown_timer(pomo.get('focusTime'), pomo.get('sessionMessage'), constants.CONTINUE_TO_BREAK_END_OPTION)
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
            draw_countdown_timer(generate_ascii_time(minutes, seconds), message)
        else:
            draw_countdown_timer(generate_ascii_time(minutes, seconds), message, ansi.str_to_color(pomo['color']['border']), ansi.str_to_color(pomo['color']['time']))
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

def pomodoro_timer_global(total_seconds: int):
    """
    Starts a simple countdown timer that lasts only one session. This acts as
    just a regular countdown timer that will terminate the program once the time
    is up.
    """
    global pomo
    pomo = settings.make_countdown_pomo(total_seconds)

    # Begin one time pomodoro
    countdown_timer(pomo.get('focusTime'), pomo.get('sessionMessage'), constants.TERMINATE_END_OPTION)

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

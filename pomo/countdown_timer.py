import main
import ansi
import time
import os
import sys
import threading
import subprocess
import signal

sessions = 0
current_session = 0
isBreak = False

def draw_border(content, message=None, color=ansi.RED):
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

    print(color + border_top + ansi.RESET)
    print(padding_x + color + f"│{' ' * width}│" + ansi.RESET)  # Top padding
    for line in content:
        print(padding_x + color + f"│  {ansi.YELLOW}{line}{color} │" + ansi.RESET)  # Keep clock ANSI colors
    print(padding_x + color + f"│{' ' * width}│" + ansi.RESET)  # Bottom padding
    print(color + border_bottom + ansi.RESET)

    # Display the message centered below the timer
    if message:
        print("\n" + ansi.center_text(message))

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

stop_event = threading.Event()  # Shared stop event for graceful shutdown
sound_process = None  # To track sound subprocess

def handle_exit(signum, frame):
    """Handles exit signals (SIGINT, SIGHUP, SIGTERM) and ensures proper cleanup."""
    print("\nReceived exit signal, cleaning up...")

    # Stop flashing alert
    stop_event.set()

    # Terminate sound process if running
    global sound_process
    if sound_process and sound_process.poll() is None:
        sound_process.terminate()
        sound_process.wait()

    # Clear screen before exiting (optional)
    os.system("clear" if os.name == "posix" else "cls")

    print("Exited cleanly.")
    sys.exit(0)  # Ensure a clean exit

# Register signal handlers
signal.signal(signal.SIGINT, handle_exit)   # Handle Ctrl+C
signal.signal(signal.SIGHUP, handle_exit)   # Handle terminal close (Unix)
signal.signal(signal.SIGTERM, handle_exit)  # Handle kill command

def flashing_alert():
    """Flashes the screen repeatedly showing 00:00 until the user presses Enter."""
    def flash():
        while not stop_event.is_set():
            for color in [ansi.RED, ansi.WHITE]:  # Alternate between red and white
                if stop_event.is_set():
                    return  # Stop flashing immediately if flag is set
                os.system('clear')
                draw_border(generate_ascii_time(0, 0), f"{ansi.BLUE}Press ENTER to acknowledge...", color=color)
                time.sleep(0.5)  # Adjust flash speed

    flash_thread = threading.Thread(target=flash, daemon=True)
    flash_thread.start()

def play_sound_loop(sound_path, volume):
    """Continuously plays the alarm sound until the user presses ENTER."""
    global sound_process
    while not stop_event.is_set():
        try:
            if sys.platform == "win32":
                sound_process = subprocess.Popen([
                    "ffmpeg", "-i", sound_path, "-filter:a", f"volume={volume}", "-f", "wav", "pipe:1"
                ], stdout=subprocess.PIPE)
                subprocess.Popen(["powershell", "-c", "(New-Object Media.SoundPlayer).PlaySync()"], stdin=sound_process.stdout)
            elif sys.platform == "darwin":  # macOS
                sound_process = subprocess.Popen(["afplay", "-v", volume, sound_path])
            elif sys.platform == "linux":
                sound_process = subprocess.Popen(["play", sound_path, "vol", volume])

            sound_process.wait()
        except Exception as e:
            print(f"Error playing sound: {e}")
            break

def wait_for_user_input(stop_event):
    """Waits for the user to press ENTER, then stops the flashing and sound."""
    input()
    stop_event.set()

    # Terminate the sound process if it's still running
    if sound_process and sound_process.poll() is None:
        sound_process.terminate()

def countdown_end(option=0):
    """Plays an alarm with both flashing and sound, stopping when user presses ENTER."""
    sound_file = os.path.join("sfx", "DEFAULT_ALARM.wav")

    if not os.path.exists(sound_file):
        print("Error: Sound file not found!")
        sys.exit(1)

    # Start flashing and playing sound in parallel
    flashing_alert()
    sound_thread = threading.Thread(target=play_sound_loop, args=(sound_file, "0.5"), daemon=True)
    sound_thread.start()

    # Wait for user input and stop everything
    input()
    stop_event.set()

    # Ensure sound process is terminated
    global sound_process
    if sound_process and sound_process.poll() is None:
        sound_process.terminate()
        sound_process.wait()

    if option == 0:
        main.show_main_menu()
    elif option == 1:
        # continue to next break
        pass
    elif option == 2:
        # continue to next focus session
        pass
    else:
        print(f"{ansi.RESET}\nTimer acknowledged. Exiting...\n")

def countdown_timer(total_seconds: int, message:str="Focusing..."):
    """Runs the countdown timer one time"""
    for remaining in range(total_seconds, -1, -1):
        minutes = remaining // 60
        seconds = remaining % 60
        os.system("clear" if os.name == "posix" else "cls")  # Clear screen
        draw_border(generate_ascii_time(minutes, seconds), message)
        time.sleep(1)

    os.system("clear" if os.name == "posix" else "cls")  # Clear screen before flashing
    countdown_end(3)

def pomodoro_timer(name: str, source=0):
    """
    Runs a pomodoro timer based on the name provided.

        args
        name: str -> the name of the pomodoro
        source: where this function was called.
            0 -> From the Main Menu
                Will redirect error to the main menu.
            1 -> Directly from CLI
                Will print error from CLI then stop program.

    Reads the list of pomodoros in the settings.json file stored in the
    $HOME/Documents/narlock/pomo/settings.json file. If the pomodoro
    name is not found in the "pomos" list, this will return an error message.

    If the pomodoro is found, then we will set the properties of the global
    variables "sessions", "current_session", and "isBreak", then call the
    countdown_timer function and begin the first session.

    After sessions are over, we will check if the session has a break, if it does,
    we will set isBreak to true and then call countdown_timer to begin the 
    """
import ansi
import time
import os
import sys
import threading
import subprocess

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

def flashing_alert(stop_event):
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

def play_sound_loop(sound_path, volume, stop_event):
    """Continuously plays the alarm sound until the user presses ENTER."""
    global sound_process
    while not stop_event.is_set():
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

def wait_for_user_input(stop_event):
    """Waits for the user to press ENTER, then stops the flashing and sound."""
    input()
    stop_event.set()

    # Terminate the sound process if it's still running
    if sound_process and sound_process.poll() is None:
        sound_process.terminate()

def countdown_end():
    """Plays an alarm with both flashing and sound, stopping when user presses ENTER."""
    sound_file = os.path.join("sfx", "DEFAULT_ALARM.wav")

    if not os.path.exists(sound_file):
        print("Error: Sound file not found!")
        sys.exit(1)

    stop_event = threading.Event()

    # TODO only flash if enabled...
    # Start flashing and playing sound in parallel
    flashing_alert(stop_event)
    # TODO only play sound if enabled...
    sound_thread = threading.Thread(target=play_sound_loop, args=(sound_file, "0.5", stop_event), daemon=True)
    sound_thread.start()

    # Wait for user input and stop everything
    wait_for_user_input(stop_event)

def countdown_timer(total_seconds):
    """Runs the countdown timer."""
    for remaining in range(total_seconds, -1, -1):
        minutes = remaining // 60
        seconds = remaining % 60
        os.system("clear" if os.name == "posix" else "cls")  # Clear screen
        draw_border(generate_ascii_time(minutes, seconds), "Focusing...")
        time.sleep(1)

    os.system("clear" if os.name == "posix" else "cls")  # Clear screen before flashing
    countdown_end()
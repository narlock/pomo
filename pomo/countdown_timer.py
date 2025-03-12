import ansi
import time
import os
import sys
import threading
import signal

CLEAR_SCREEN = "\033[2J\033[H"  # Clears screen and moves cursor to top-left

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

def flashing_alert():
    """Flashes the screen repeatedly showing 00:00 until the user presses Enter."""
    def flash():
        """Inner function that flashes the screen in a loop."""
        while not stop_flashing.is_set():
            for color in [ansi.RED, ansi.WHITE]:  # Alternate between red and white
                if stop_flashing.is_set():
                    return  # Stop flashing immediately if flag is set
                os.system("clear" if os.name == "posix" else "cls")  # Full clear
                sys.stdout.write(CLEAR_SCREEN)  # Clear screen buffer
                sys.stdout.flush()
                draw_border(generate_ascii_time(0, 0), "Press ENTER to acknowledge...", color=color)
                time.sleep(0.5)  # Adjust flash speed

    # Start flashing in a separate thread
    stop_flashing = threading.Event()
    flash_thread = threading.Thread(target=flash, daemon=True)
    flash_thread.start()

    # Wait for user to press Enter
    input()
    stop_flashing.set()  # Stop flashing when user presses Enter

def countdown_timer(total_seconds):
    """Runs the countdown timer."""
    for remaining in range(total_seconds, -1, -1):
        minutes = remaining // 60
        seconds = remaining % 60
        os.system("clear" if os.name == "posix" else "cls")  # Clear screen
        draw_border(generate_ascii_time(minutes, seconds), "Focusing...")
        time.sleep(1)

    os.system("clear" if os.name == "posix" else "cls")  # Clear screen before flashing
    flashing_alert()  # Start flashing effect
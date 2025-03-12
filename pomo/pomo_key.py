import sys
import termios
import tty

# Get a single keypress
def get_keypress():
    """
    Reads a single keypress from the user without requiring Enter.
    
    This function temporarily sets the terminal to raw mode so that it
    can capture keypresses directly, including special keys like arrow keys.
    
    Steps:
    1. Get the file descriptor for standard input (`sys.stdin.fileno()`).
    2. Store the current terminal settings (`termios.tcgetattr`).
    3. Switch the terminal to raw mode (`tty.setraw`), allowing key-by-key input.
    4. Read a single character (`sys.stdin.read(1)`).
    5. If the first character is the escape character (`\x1b`), read two more characters
       to capture full arrow key sequences.
    6. Restore the terminal to its original settings (`termios.tcsetattr`).
    7. Return the captured key.
    
    Returns:
        str: The captured key sequence as a string.
    """
    try:
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        tty.setraw(sys.stdin.fileno())
        key = sys.stdin.read(1)
        if key == '\x1b':  # Handle escape sequence (arrow keys)
            key += sys.stdin.read(2)  # Read the next two characters
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return key
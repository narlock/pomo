"""
kbCLI - ansi.py
author: narlock

This file contains ansi color codes and ability to create colors.
"""

import re
import shutil

# 256-Color Mode
def ansi_256(color_id):
    return f"\033[38;5;{color_id}m"

def bg_ansi_256(color_id):
    return f"\033[48;5;{color_id}m"

# True Color (24-bit RGB)
def ansi_rgb(r, g, b):
    return f"\033[38;2;{r};{g};{b}m"

def bg_ansi_rgb(r, g, b):
    return f"\033[48;2;{r};{g};{b}m"

def ansi_link(link, link_title):
    return f"\033]8;;{link}\033\\{link_title}\033]8;;\033\\"

# Standard ANSI Colors
BLACK = "\033[30m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
WHITE = "\033[37m"
ORANGE = ansi_rgb(255, 165, 0)

# Bright ANSI Colors
BRIGHT_BLACK = "\033[90m"
BRIGHT_RED = "\033[91m"
BRIGHT_GREEN = "\033[92m"
BRIGHT_YELLOW = "\033[93m"
BRIGHT_BLUE = "\033[94m"
BRIGHT_MAGENTA = "\033[95m"
BRIGHT_CYAN = "\033[96m"
BRIGHT_WHITE = "\033[97m"

# Background Colors
BG_BLACK = "\033[40m"
BG_RED = "\033[41m"
BG_GREEN = "\033[42m"
BG_YELLOW = "\033[43m"
BG_BLUE = "\033[44m"
BG_MAGENTA = "\033[45m"
BG_CYAN = "\033[46m"
BG_WHITE = "\033[47m"

# Bright Background Colors
BG_BRIGHT_BLACK = "\033[100m"
BG_BRIGHT_RED = "\033[101m"
BG_BRIGHT_GREEN = "\033[102m"
BG_BRIGHT_YELLOW = "\033[103m"
BG_BRIGHT_BLUE = "\033[104m"
BG_BRIGHT_MAGENTA = "\033[105m"
BG_BRIGHT_CYAN = "\033[106m"
BG_BRIGHT_WHITE = "\033[107m"

COLOR_MAP = {
    "black": BLACK,
    "red": RED,
    "green": GREEN,
    "yellow": YELLOW,
    "blue": BLUE,
    "magenta": MAGENTA,
    "cyan": CYAN,
    "white": WHITE,
    "orange": ORANGE,
    
    "bright_black": BRIGHT_BLACK,
    "bright_red": BRIGHT_RED,
    "bright_green": BRIGHT_GREEN,
    "bright_yellow": BRIGHT_YELLOW,
    "bright_blue": BRIGHT_BLUE,
    "bright_magenta": BRIGHT_MAGENTA,
    "bright_cyan": BRIGHT_CYAN,
    "bright_white": BRIGHT_WHITE,

    "bg_black": BG_BLACK,
    "bg_red": BG_RED,
    "bg_green": BG_GREEN,
    "bg_yellow": BG_YELLOW,
    "bg_blue": BG_BLUE,
    "bg_magenta": BG_MAGENTA,
    "bg_cyan": BG_CYAN,
    "bg_white": BG_WHITE,

    "bg_bright_black": BG_BRIGHT_BLACK,
    "bg_bright_red": BG_BRIGHT_RED,
    "bg_bright_green": BG_BRIGHT_GREEN,
    "bg_bright_yellow": BG_BRIGHT_YELLOW,
    "bg_bright_blue": BG_BRIGHT_BLUE,
    "bg_bright_magenta": BG_BRIGHT_MAGENTA,
    "bg_bright_cyan": BG_BRIGHT_CYAN,
    "bg_bright_white": BG_BRIGHT_WHITE
}

# Reset Color
RESET = "\033[0m"

# Other
BOLD = "\033[1m"
UNDERLINE = "\u001b[4m"

# ASCII numbers for display
ascii_numbers = {
    "0": [
        "  █████  ",
        " ██   ██ ",
        " ██   ██ ",
        " ██   ██ ",
        "  █████  "
    ],
    "1": [
        "   ██    ",
        "  ███    ",
        "   ██    ",
        "   ██    ",
        " ██████  "
    ],
    "2": [
        " ██████  ",
        "      ██ ",
        "  █████  ",
        " ██      ",
        " ███████ "
    ],
    "3": [
        " ██████  ",
        "      ██ ",
        "  █████  ",
        "      ██ ",
        " ██████  "
    ],
    "4": [
        " ██  ██  ",
        " ██  ██  ",
        " ███████ ",
        "     ██  ",
        "     ██  "
    ],
    "5": [
        " ███████ ",
        " ██      ",
        " ██████  ",
        "      ██ ",
        " ██████  "
    ],
    "6": [
        "  █████  ",
        " ██      ",
        " ██████  ",
        " ██   ██ ",
        "  █████  "
    ],
    "7": [
        " ███████ ",
        "     ██  ",
        "    ██   ",
        "   ██    ",
        "  ██     "
    ],
    "8": [
        "  █████  ",
        " ██   ██ ",
        "  █████  ",
        " ██   ██ ",
        "  █████  "
    ],
    "9": [
        "  █████  ",
        " ██   ██ ",
        "  ██████ ",
        "      ██ ",
        "  █████  "
    ],
    ":": [
        "        ",
        "   ██   ",
        "        ",
        "   ██   ",
        "        "
    ]
}

ascii_letters = {
    "A": [
        "   ████   ",
        "  ██  ██  ",
        " ████████ ",
        " ██    ██ ",
        " ██    ██ "
    ],
    "B": [
        " █████   ",
        " ██   ██ ",
        " █████   ",
        " ██   ██ ",
        " █████   "
    ],
    "P": [
        " ██████  ",
        " ██   ██ ",
        " ██████  ",
        " ██      ",
        " ██      "
    ],
    "O": [
        "  █████  ",
        " ██   ██ ",
        " ██   ██ ",
        " ██   ██ ",
        "  █████  "
    ],
    "M": [
        " ██   ██ ",
        " ███ ███ ",
        " ██ █ ██ ",
        " ██   ██ ",
        " ██   ██ "
    ]
}

def strip_ansi(text):
    """Removes ANSI color codes and hyperlink sequences from text."""
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    osc_escape = re.compile(r'\033]8;;.*?\033\\')  # Matches ANSI hyperlinks
    text = osc_escape.sub('', text)  # Remove links
    return ansi_escape.sub('', text)  # Remove other ANSI codes

def center_text(text):
    """Centers multiline text according to terminal width, handling ANSI sequences."""
    term_width, _ = get_terminal_size()
    
    centered_lines = []
    for line in text.splitlines():
        stripped_line = strip_ansi(line)
        left_padding = max((term_width - len(stripped_line)) // 2, 0)
        centered_lines.append(" " * left_padding + line)  # Keep ANSI codes in the text
    
    return "\n".join(centered_lines)

def get_terminal_size():
    """Returns the current terminal width and height."""
    size = shutil.get_terminal_size()
    return size.columns, size.lines

def str_to_color(color_name: str):
    """
    Returns the ANSI escape code for the given color name.
    """
    return COLOR_MAP.get(color_name.lower(), "")
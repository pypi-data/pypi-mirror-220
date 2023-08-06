class CLIColorizer:
    """
    This class is used to colorize and style console text.
    """
    def __init__(self):
        self.styles = {
            "reset": "\033[0m", # resets all colors and styles
            "bold_bright": "\033[1m",
            "dim": "\033[2m",
            "italic": "\033[3m",
            "underline": "\033[4m",
            "blink": "\033[5m",
            "rapid_blink": "\033[6m",
            "reverse": "\033[7m",
            "hide": "\033[8m",
            "strikethrough": "\033[9m",
            "reset_bold_bright": "\033[21m",
            "reset_dim": "\033[22m",
            "reset_italic": "\033[23m",
            "reset_underline": "\033[24m",
            "reset_blink": "\033[25m",
            "reset_reverse": "\033[27m",
            "reset_hide": "\033[28m",
            "reset_strikethrough": "\033[29m",
}
        
        self.foreground_colors = {
            "black": "\033[30m",
            "red": "\033[31m",
            "green": "\033[32m",
            "yellow": "\033[33m",
            "blue": "\033[34m",
            "magenta": "\033[35m",
            "cyan": "\033[36m",
            "white": "\033[37m",
            "bright_black": "\033[90m",
            "bright_red": "\033[91m",
            "bright_green": "\033[92m",
            "bright_yellow": "\033[93m",
            "bright_blue": "\033[94m",
            "bright_magenta": "\033[95m",
            "bright_cyan": "\033[96m",
            "bright_white": "\033[97m",
        }
        
        self.background_colors = {
            "black_bg": "\033[40m",
            "red_bg": "\033[41m",
            "green_bg": "\033[42m",
            "yellow_bg": "\033[43m",
            "blue_bg": "\033[44m",
            "magenta_bg": "\033[45m",
            "cyan_bg": "\033[46m",
            "white_bg": "\033[47m",
            "bright_black_bg": "\033[100m",
            "bright_red_bg": "\033[101m",
            "bright_green_bg": "\033[102m",
            "bright_yellow_bg": "\033[103m",
            "bright_blue_bg": "\033[104m",
            "bright_magenta_bg": "\033[105m",
            "bright_cyan_bg": "\033[106m",
            "bright_white_bg": "\033[107m",
        }
        
        self.all_codes = {**self.styles, **self.foreground_colors, **self.background_colors}

    def __getattr__(self, code):
        """
        This method returns the ANSI escape code for the requested color or style.
        """
        try:
            return self.all_codes[code]
        except KeyError:
            raise ValueError(f"Unsupported code: {code}")


def print_colored_text(text, code_name):
    """
    This function prints text in the specified color or style.
    """
    color = CLIColorizer()
    print(f"{getattr(color, code_name)}{text}{color.reset}")


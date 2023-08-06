from msvcrt import getch
import termcolor
import os

keyboard = {
    119: 'W', 97: 'A', 115: 'S', 100: 'D',
    72: 'UP_ARROW', 80: 'DOWN_ARROW', 75: 'LEFT_ARROW', 77: 'RIGHT_ARROW',
    56: 'KP_UP', 50: 'KP_DOWN', 52: 'KP_LEFT', 53: 'KP_ENTER', 54: 'KP_RIGHT',
    13: 'ENTER', 32: 'SPACE', 8: 'BACKSPACE', 83: 'DEL',
}

windows_terminal_colors = {
    'black': '0',
    'blue': '1',
    'green': '2',
    'cyan': '3',
    'red': '4',
    'purple': '5',
    'yellow': '6',
    'white': 'F',
    'gray': '8',
    'light_blue': '9',
    'light_green': 'A',
    'light_aqua': 'B',
    'light_red': 'C',
    'light_purple': 'D',
    'light_yellow': 'E',
}


def echo(msg: str):
    return lambda: msg


def resize_terminal(rows=128, cols=32):
    # todo Linux terminal resize
    os.system(f'mode con: cols={cols} lines={rows}')


def prepare_terminal(foreground_color: str, background_color: str):
    # WINDOWS

    os.system(f'color {windows_terminal_colors[background_color]}{windows_terminal_colors[foreground_color]}')
    # LINUX
    # os.system(f'setterm -term linux -back $' + color + ' -fore white -clear')


def get_key() -> str:
    # ToDo Linux input
    key = ord(getch())
    if key not in keyboard.keys() or key == 224:
        return 'unknown'
    else:
        return keyboard[key]


def colored_center(text: str, width: int, fill_char: str, background_color: str, padding=0) -> str:
    assert len(fill_char) == 1
    space = width - len(text) + 1
    text = termcolor.colored(
        text=fill_char * (space // 2 + padding),
        on_color=background_color) + text + termcolor.colored(
        text=fill_char * (space // 2 + space % 2 - padding),
        on_color=background_color)
    return text


def colored_ljust(text: str, width: int, fill_char: str, background_color: str, padding=0) -> str:
    assert len(fill_char) == 1
    assert padding >= 0
    space = width - len(text) + 1
    text = termcolor.colored(
        text=fill_char*(0+padding),
        on_color=background_color
    ) + text + termcolor.colored(
        text=fill_char*(space-padding),
        on_color=background_color
    )
    return text


def colored_rjust(text: str, width: int, fill_char: str, background_color: str, padding=0) -> str:
    assert len(fill_char) == 1
    assert padding <= 0
    space = width - len(text) + 1
    text = termcolor.colored(
        text=fill_char*(space+padding),
        on_color=background_color
    ) + text + termcolor.colored(
        text=fill_char*(0-padding),
        on_color=background_color
    )
    return text

from .utils import *
from configparser import ConfigParser
import termcolor


class Text(object):
    def __init__(self, text: str, colorscheme: ConfigParser, alignment='center', padding=0, fill_char=' ') -> None:
        assert alignment in ('left', 'center', 'right')
        assert isinstance(padding, int)
        assert isinstance(fill_char, str) and len(fill_char) == 1

        self.text = text
        self.colorscheme = colorscheme
        self.alignment = alignment
        self.padding = padding
        self.fill_char = fill_char

        self.lines = self.text.split('\n')

    def get_representation(self, width: int) -> str:
        assert width > 0

        if any([len(x) + abs(self.padding) > width for x in self.lines]):
            print(f'WARNING: text too long for given width: {self.text}')

        representation = ''
        for line in self.lines:
            # Use padding
            if self.padding >= 0:
                line = self.fill_char * self.padding + line
            else:
                line = line + self.fill_char * (-self.padding)

            # Use alignment
            if self.alignment == 'left':
                line = line.ljust(width, self.fill_char)
            elif self.alignment == 'right':
                line = line.rjust(width, self.fill_char)
            else:
                line = line.center(width, self.fill_char)

            # Use colors
            representation += termcolor.colored(
                text=line,
                color=self.colorscheme['information']['foreground'],
                on_color='on_' + self.colorscheme['information']['background'],
            )

        return representation

    def __repr__(self) -> str:
        return f'<Text> [{self.text}, {self.alignment}, {self.padding}]'


class Button(object):
    def __init__(self, text: str, colorscheme: ConfigParser, callback=None, instant_callback=None, alignment='center',
                 padding=0, fill_char=' ') -> None:
        self.text = text
        self.callback = echo(text) if callback is None else callback
        self.colorscheme = colorscheme
        self.fill_char = fill_char
        self.alignment = alignment
        self.padding = padding

        self.is_active = False
        self.is_selected = False

    def change_activation(self):
        self.is_active = bool((self.is_active + 1) % 2)

    def get_representation(self, width: int, *args) -> str:
        res = self.text

        # Current selection
        if self.is_selected:
            res = termcolor.colored(
                text=res,
                color=self.colorscheme['current selection']['foreground'],
                on_color='on_' + self.colorscheme['current selection']['background'],
            )

        else:
            if self.is_active:
                res = termcolor.colored(
                    text=res,
                    color=self.colorscheme['selected']['foreground'],
                    on_color='on_' + self.colorscheme['selected']['background'],
                )
            else:
                res = termcolor.colored(
                    text=res,
                    color=self.colorscheme['not selected']['foreground'],
                    on_color='on_' + self.colorscheme['not selected']['background']
                )
        # Use alignment
        delta = len(res) - len(self.text) - 1

        if self.alignment == 'center':
            res = colored_center(res,
                                 width+delta,
                                 self.fill_char,
                                 'on_' + self.colorscheme['terminal']['background'],
                                 padding=self.padding)
        elif self.alignment == 'right':
            res = colored_rjust(res,
                                width+delta,
                                self.fill_char,
                                'on_' + self.colorscheme['terminal']['background'],
                                padding=self.padding)
        else:
            res = colored_ljust(res,
                                width+delta,
                                self.fill_char,
                                'on_' + self.colorscheme['terminal']['background'],
                                padding=self.padding)

        self.is_selected = False
        return termcolor.colored(res, on_color='on_' + self.colorscheme['terminal']['background'])


################################
# S P E C I A L    B U T T O N S
################################
class BackButton(Button):
    def __init__(self, text: str, colorscheme: ConfigParser, alignment='center', padding=0, fill_char=' ') -> None:
        super().__init__(
            text=text,
            colorscheme=colorscheme,
            alignment=alignment,
            padding=padding,
            fill_char=fill_char,

            callback=lambda: 'back',
        )


class ConfirmButton(Button):
    def __init__(self, text: str, colorscheme: ConfigParser, alignment='center', padding=0, fill_char=' ') -> None:
        super().__init__(
            text=text,
            colorscheme=colorscheme,
            alignment=alignment,
            padding=padding,
            fill_char=fill_char,

            callback=lambda: 'confirm',
        )

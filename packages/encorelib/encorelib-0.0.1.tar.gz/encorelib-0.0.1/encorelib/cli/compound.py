from .atomic import *


class Selection(object):
    def __init__(self, placeholder, max_selection=1) -> None:
        assert isinstance(max_selection, int) and max_selection > 0

        self.placeholder = self.__translate(placeholder)
        self.__max_selection = max_selection
        self.__selected = set()

    def __translate(self, modules) -> list:
        out = []
        for module in modules:
            if isinstance(module, list):
                res = self.__translate(module)
            elif isinstance(module, tuple):
                res = self.__translate(module)
            elif isinstance(module, Text):
                res = [Button(
                    text=module.text,
                    callback=None,
                    colorscheme=module.colorscheme,
                    alignment=module.alignment,
                    padding=module.alignment,
                )]
            elif isinstance(module, Button):
                res = [module]
            elif module is None:
                res = [None]
            else:
                raise TypeError(f'Unsupported module {type(module)} for module {module}')
            out.append(res)

        max_width = max(len(x) for x in out)
        for i, line in enumerate(out):
            line += [None]*(max_width - len(line))
            out[i] = line
        return out

    def get_representation(self, width: int, *args) -> str:
        res = ''
        for line in self.placeholder:
            truth_length = len([obj for obj in line if obj is not None])
            for subline in line:
                if isinstance(subline, list):
                    for button in subline:
                        res += button.get_representation(width=round(width/truth_length))
                elif isinstance(subline, Button):
                    res += subline.get_representation(width=round(width/truth_length))
            #res += '\n'
        return res

    def select(self, row: int, col: int, type_: str):
        col = min(
            len([x for x in self.placeholder[row] if x is not None])-1,
            col
        )
        if isinstance(self.placeholder[row][col], list):
            button = self.placeholder[row][col][0]
        else:
            button = self.placeholder[row][col]

        if type_ == 'SELECT':
            button.is_selected = True
        else:
            ###################
            # Select
            ###################
            if len(self.__selected) < self.__max_selection:
                if button.is_active:
                    self.__selected.remove(button)
                    button.is_active = False
                else:
                    self.__selected.add(button)
                    button.is_active = True
                    return row, col, button.callback, isinstance(button, BackButton) or isinstance(button, ConfirmButton)
            else:
                if button.is_active:
                    self.__selected.remove(button)
                    button.is_active = False

        return row, col, None, False

    def get_sizes(self) -> list:
        out = []
        for line in self.placeholder:
            out.append(len(line))
        return out

    def expand(self, target_size: int) -> None:
        for i, line in enumerate(self.placeholder):
            line += [None]*(target_size - len(line))
            self.placeholder[i] = line

    def __repr__(self) -> str:
        return f'<Select> [{self.__max_selection}, {self.placeholder}]'


class Keypad(object):
    def __init__(self, *args) -> None:
        assert all(isinstance(x, Selection) for x in args)
        self.selections = args

    def get_representation(self, width: int) -> str:
        res = ''
        for selection in self.selections:
            res += selection.get_representation(width=width)
        return res

    def get_shape(self) -> tuple[int, int]:
        return len(self.selections), len(self.selections[0])

    def select(self, row: int, col: int, type_: str):
        dline = 0
        callback, activate = None, False
        for selection in self.selections:
            if row-dline in range(len(selection.placeholder)):
                row, col, callback, activate = selection.select(row-dline, col, type_)
                break
            dline += len(selection.placeholder)
        return row+dline, col, callback, activate

    def __add__(self, other):
        if isinstance(other, Keypad):
            self_sizes = [max(x.get_sizes()) for x in self.selections]
            other_sizes = [max(x.get_sizes()) for x in other.selections]
            target_size = max(self_sizes + other_sizes)

            self.selections += other.selections

            for selection in self.selections:
                selection.expand(target_size)
        return self


class Menu(object):
    def __init__(self, *args, width: int, length: int, colorscheme: ConfigParser) -> None:
        assert any(isinstance(x, Keypad) for x in args)

        self.__modules = args
        self.__width = width
        self.__length = length
        self.__colorscheme = colorscheme

        self.__data = []

    def update(self):
        self.__data = []
        for obj in self.__modules:
            self.set_line(obj)

    def set_line(self, obj) -> None:
        rep = obj.get_representation(width=self.__width).split('\n')
        for line in rep:
            self.__data.append(line)

    def run(self):
        cur_line, cur_col = -1, 0
        callbacks = []
        # get sizes of keypads
        sizes = {
            i: (
                sum(len(selection.placeholder) for selection in keypad.selections),
                max(max(selection.get_sizes()) for selection in keypad.selections),
            )
            for i, keypad in enumerate(self.__modules)
            if isinstance(keypad, Keypad)
        }
        max_lines, max_cols = sum(x[0] for x in sizes.values()), max(x[1] for x in sizes.values())

        while True:
            self.update()

            resize_terminal(self.__length, self.__width)

            for line in self.__data:
                print(line)

            ##############
            # Use keyboard
            ##############
            while True:
                key = get_key()
                if key == 'unknown':
                    continue

                # Move up
                elif key in ('W', 'UP_ARROW', 'KP_UP'):
                    cur_line = (cur_line - 1) % max_lines

                # Move down
                elif key in ('S', 'DOWN_ARROW', 'KP_DOWN'):
                    cur_line = (cur_line + 1) % max_lines

                # Move left
                elif key in ('A', 'LEFT_ARROW', 'KP_LEFT'):
                    cur_col = (cur_col - 1) % max_cols

                # Move right
                elif key in ('D', 'RIGHT_ARROW', 'KP_RIGHT'):
                    cur_col = (cur_col + 1) % max_cols

                # Entered
                elif key in ('ENTER', 'SPACE', 'KP_ENTER'):
                    dline = 0
                    for i in sizes:
                        shape = sizes[i]
                        if cur_line - dline in range(shape[0]):
                            row, col, callback, activate = self.__modules[i].select(cur_line - dline, cur_col, 'ENTER')

                            if activate:
                                command = callback()
                                if command == 'confirm':
                                    return [callback_() for callback_ in callbacks]
                                if command == 'back':
                                    return 'back'
                            else:
                                callbacks.append(callback)
                            # Reassign coordinates
                            cur_line = row+dline
                            cur_col = col
                            break
                        dline += shape[0]

                elif key in ('BACKSPACE',):
                    exit(0)

                # Select
                dline = 0
                for i in sizes:
                    shape = sizes[i]
                    if cur_line - dline in range(shape[0]):
                        row, col, _, _ = self.__modules[i].select(cur_line - dline, cur_col, 'SELECT')
                        # Reassign coordinates
                        cur_line = row + dline
                        cur_col = col
                        break
                    dline += shape[0]
                break

    def get_selection_size(self) -> int:
        res = 0
        for obj in self.__modules:
            if isinstance(obj, Button):
                res += 1
            if isinstance(obj, Text):
                res += len(obj.lines)
        return res

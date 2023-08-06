class ProgressBar(object):
    def __init__(self, width=150, empty_char=' ', fill_char='#', cur_char='>') -> None:
        self.width = width
        self.cur_char = cur_char
        self.fill_char = fill_char
        self.empty_char = empty_char

        self.current_progress = 0

    def set_progress(self, progress):
        self.current_progress = min(1, progress/100)

    def __repr__(self) -> str:
        fill_count = int(self.width*self.current_progress)
        empty_count = self.width - fill_count

        fill_part = self.fill_char*fill_count
        fill_part += self.cur_char

        empty_part = self.empty_char*empty_count

        return f'{fill_part}{empty_part}| [{str(int(self.current_progress*100)).rjust(3, "0")}%]'


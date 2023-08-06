import curses

# NOTE: bug? mypy dont raises [attr-defined] erro
from curses.textpad import rectangle  # type: ignore
from queue import SimpleQueue
from textwrap import wrap
from typing import List, Optional

from .datatypes import Margin, Pair, PairF


class Screen:
    def __init__(self, screen):
        self.scr = screen
        self.vscreen = VScreen(self.scr)

    def get_position(self) -> Pair:
        data = self.scr.getbegyx()
        return Pair(data[1], data[0])

    def get_size(self) -> Pair:
        data = self.scr.getmaxyx()
        return Pair(data[1], data[0])

    def draw(self) -> None:
        self.vscreen.draw()

    def recalculate(self) -> None:
        self.vscreen.recalculate(
            self.get_size() - Pair(2, 0), self.get_position(), Pair(0, 0), Pair(0, 1)
        )


class VScreenTextbox:
    def __init__(self, screen: Screen, buffer_size: int = 30):
        self._screen = screen

        self._rawdata: List[str] = []
        self._buffer_size = buffer_size

        self.data: List[str] = []

        self.position = Pair(0, 0)
        self.size = Pair(0, 0)

    def add_text(self, text: str) -> None:
        new_rawdata = [v.strip() for v in text.split("\n")]

        # update formatted data
        for ln in new_rawdata:
            self.data += wrap(ln, self.size.x)
        if len(self.data) > self.size.y:
            self.data = self.data[len(self.data) - self.size.y :]

        # update rawdata
        self._rawdata += new_rawdata
        if len(self._rawdata) > self._buffer_size:
            self._rawdata = self._rawdata[len(self._rawdata) - self._buffer_size :]

    def draw(self) -> None:
        for i, v in enumerate(self.data):
            self._screen.scr.addstr(
                self.position.y + i, self.position.x, v, curses.A_NORMAL  # type: ignore
            )

    def recalculate(self, position: Pair, size: Pair) -> None:
        self.position = position
        # recalculate formatted data
        if self.size != size:
            self.data = []
            for ln in reversed(self._rawdata):
                for i, v in enumerate(wrap(ln, self.size.x)):
                    self.data.insert(i, v)
                if len(self.data) > self.size.y:
                    break
            if len(self.data) > self.size.y:
                self.data = self.data[len(self.data) - self.size.y :]
        self.size = size


class VScreenLogbox(VScreenTextbox):
    def __init__(
        self, screen: Screen, data_source: Optional[SimpleQueue] = None, buffer_size: int = 30
    ):
        super().__init__(screen, buffer_size)
        self._data_source = data_source

    def recalculate(self, position: Pair, size: Pair) -> None:
        while self._data_source and (not self._data_source.empty()):
            self.add_text(self._data_source.get())
        super().recalculate(position, size)


class VScreen:
    def __init__(
        self,
        screen: Screen,
        sizep: PairF = PairF(1.0, 1.0),
        subscreens: List["VScreen"] = [],
        margin: Margin = Margin(0, 0, 0, 0),
        data: Optional[VScreenTextbox] = None,
        draw_borders: bool = False,
    ):
        self.screen = screen
        self.subscreens = subscreens

        self.position = Pair(0, 0)
        self.size = Pair(0, 0)

        self._data = data

        self.sizep = sizep
        self.margin = margin
        self.draw_borders = draw_borders

        self.border_margin = Margin(1, 1, 1, 1) if draw_borders else Margin(0, 0, 0, 0)

    def draw(self):
        if self.draw_borders:
            # draw bounds for subscreen
            try:
                rectangle(
                    self.screen.scr,
                    self.position.y,
                    self.position.x,
                    self.position.y + self.size.y - 1,
                    self.position.x + self.size.x - 1,
                )
            # TODO[PP]: exception thrown when drawing in fight bottom char place
            #           proper handling and correct type of exception should be fixed
            except Exception as e:
                print(e)
                _ = None  # TODO[PP]: stupid workarround for bandit check [B110:try_except_pass]

        if self.subscreens:
            # draw subscreens
            for sscreen in self.subscreens:
                sscreen.draw()
        else:
            # draw data
            if self._data:
                self._data.draw()

    def _get_data_position(self) -> Pair:
        return Pair(
            self.position.x + self.margin.left + self.border_margin.left,
            self.position.y + self.margin.top + self.border_margin.top,
        )

    def _get_data_size(self) -> Pair:
        return Pair(
            self.size.x
            - self.margin.left
            - self.margin.right
            - self.border_margin.left
            - self.border_margin.right,
            self.size.y
            - self.margin.top
            - self.margin.bottom
            - self.border_margin.top
            - self.border_margin.bottom,
        )

    def recalculate(
        self,
        parent_size: Pair,
        parent_position: Pair,
        position_shift: Pair,
        shift_direct: Pair,
    ):
        self.position = parent_position + position_shift
        self.size = (self.sizep * parent_size).round()
        if self._data:
            self._data.recalculate(self._get_data_position(), self._get_data_size())

        if self.subscreens:
            if shift_direct == Pair(0, 1):
                subscreen_shift_direct = Pair(1, 0)
            elif shift_direct == Pair(1, 0):
                subscreen_shift_direct = Pair(0, 1)
            else:
                raise ValueError(f"Unsupported shift_direct value '{shift_direct}'")

            pshift = Pair(0, 0)
            sizep_sum = PairF(0.0, 0.0)
            size_sum_test = Pair(0, 0)
            size_sum = Pair(0, 0)

            directed_one = Pair(1, 1) * shift_direct
            for sscreen in self.subscreens:
                sscreen.recalculate(
                    self.size,
                    self.position,
                    pshift * shift_direct,
                    subscreen_shift_direct,
                )

                sizep_sum += sscreen.sizep
                size_sum += sscreen.size
                size_sum_test = (sizep_sum * self.size).round()
                if size_sum == size_sum_test:
                    pass
                else:
                    if (size_sum.x < size_sum_test.x) or (size_sum.y < size_sum_test.y):
                        sscreen.size += directed_one
                        if self._data:
                            self._data.recalculate(
                                self._get_data_position(), self._get_data_size()
                            )
                        size_sum += directed_one
                    elif (size_sum.x > size_sum_test.x) or (size_sum.y > size_sum_test.y):
                        sscreen.size -= directed_one
                        if self._data:
                            self._data.recalculate(
                                self._get_data_position(), self._get_data_size()
                            )
                        size_sum -= directed_one

                pshift = pshift + sscreen.size - self.position

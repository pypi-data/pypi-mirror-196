import math
from dataclasses import dataclass
from typing import Union


@dataclass
class Pair:
    x: int
    y: int

    def __add__(self, value: "Pair") -> "Pair":
        return Pair(self.x + value.x, self.y + value.y)

    def __sub__(self, value: "Pair") -> "Pair":
        return Pair(self.x - value.x, self.y - value.y)

    def __mul__(self, value: "Pair") -> "Pair":
        return Pair(self.x * value.x, self.y * value.y)

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Pair):
            raise NotImplementedError()
        return all([self.x == value.x, self.y == value.y])

    def __ne__(self, value: object) -> bool:
        if not isinstance(value, Pair):
            raise NotImplementedError()
        return any([self.x != value.x, self.y != value.y])


@dataclass
class PairF:
    x: float
    y: float

    def __add__(self, value: "PairF") -> "PairF":
        return PairF(self.x + value.x, self.y + value.y)

    def __mul__(self, value: Union["PairF", Pair]) -> "PairF":
        return PairF(self.x * value.x, self.y * value.y)

    def ceil(self) -> Pair:
        return Pair(math.ceil(self.x), math.ceil(self.y))

    def round(self) -> Pair:
        return Pair(int(round(self.x, 0)), int(round(self.y, 0)))


@dataclass
class Margin:
    top: int
    bottom: int
    left: int
    right: int

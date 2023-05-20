from __future__ import annotations
from abc import ABC, abstractmethod
import math
from core.dataclasses.DataVector import Point


class Kernel(ABC):

    # h: float

    @abstractmethod
    def get_weight(self, point1: Point, point2: Point) -> float:
        pass


class FlatKernel(Kernel):
    def __init__(self, h: float):
        self.h = h

    def get_weight(self, point1: Point, point2: Point) -> float:
        return 1 if point1.distance(point2) <= self.h else 0

class GaussianKernel(Kernel):
    def __init__(self, sigma: float):
        self.sigma = sigma

    def get_weight(self, point1: Point, point2: Point) -> float:
        return math.exp(-point1.distance(point2) ** 2 / (2 * self.sigma ** 2))

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List
from .Point import Point

class DataVector:
    def __init__(self, points: List[Point]):
        self.points = points

    def __iter__(self):
        return iter(self.points)

    def __getitem__(self, index):
        return self.points[index]

    def __len__(self):
        return len(self.points)

    def append(self, point):
        self.points.append(point)

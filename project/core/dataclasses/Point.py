from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Tuple


class Point(ABC):
    @abstractmethod
    def __init__(self, coordinates: Tuple[float,...]) -> None:
        self.coordinates = coordinates

    @abstractmethod
    def distance(self, other: Point) -> float:
        pass

    def __repr__(self) -> str:
        return f"{__class__.__name__}({self.coordinates})"
    
    def __getitem__(self, index):
        return self.coordinates[index]

    def __len__(self):
        return len(self.coordinates)
    
    def __eq__(self, other):
        if isinstance(other, Point) and self.coordinates == other.coordinates:
            return True
        return False

class Point1D(Point):
    def __init__(self, x: float) -> None:
        super().__init__((x,))

    def distance(self, other: Point1D) -> float:
        return abs(self.coordinates[0] - other.coordinates[0])

    # def __repr__(self):
    #     return f"Point1D({self.coordinates})"


class Point2D(Point):
    def __init__(self, x: float, y: float) -> None:
        super().__init__((x, y))

    def distance(self, other: Point2D) -> float:
        return (
            (self.coordinates[0] - other.coordinates[0]) ** 2
            + (self.coordinates[1] - other.coordinates[1]) ** 2
        ) ** 0.5

    # def __repr__(self) -> str:
    #     return f"Point2D({self.coordinates})"


class Point3D(Point):
    def __init__(self, x: float, y: float, z: float) -> None:
        super().__init__((x, y, z))

    def distance(self, other: Point) -> float:
        return (
            (self.coordinates[0] - other.coordinates[0]) ** 2
            + (self.coordinates[1] - other.coordinates[1]) ** 2
            + (self.coordinates[2] - other.coordinates[2]) ** 2
        ) ** 0.5

    # def __repr__(self) -> str:
    #     return f"Point3D({self.coordinates})"

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List
from core.kernel.Kernel import Kernel
from core.dataobject.DataVector import Point, DataVector
from .MeanShiftClustering import MeanShiftClustering

class LengthVectorizer:
    def __init__(self):
        pass

    def fit(self, data: List[str]):
        return [len(s) for s in data]

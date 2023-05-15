from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Union

from tqdm import tqdm

from core.dataobject.DataVector import DataVector, Point
from core.kernel.Kernel import Kernel


class MeanShiftClustering:
    # TODO: implement an abstract class for clustering algorithms
    def __init__(self, kernel: Kernel, threshold: float = 1e-5):
        # self.h = h
        self.threshold = threshold
        self.kernel = kernel


    @staticmethod
    def shift_mode(point: Point, data: Union[DataVector, List[Point]], kernel: Kernel):
        # TODO: fix this method to work with other objects
        total_weights = 0
        weighted_sum = [0, 0, 0]
        for i in range(len(data)):
            weight = kernel.get_weight(point, data[i])
            total_weights += weight
            weighted_sum[0] += weight * data[i][0]
            weighted_sum[1] += weight * data[i][1]
            weighted_sum[2] += weight * data[i][2]

        if total_weights != 0:
            point_cls = type(point)
            coordinates = tuple([coordinate / total_weights for coordinate in weighted_sum])
            return point_cls(*coordinates) 
        else:
            return point

    def fit(self, data: DataVector, verbose: bool = False):
        mode = [[] for _ in range(len(data))]

        if not verbose:
            iterator = range(len(data))
        else:
            iterator = tqdm(range(len(data)), total=len(data), desc=self.__class__.__name__)
        for i in iterator:
        # for i in range(len(data)):
            m = 0
            mode[i].append(data[i])
            while True:
                mode[i].append(self.shift_mode(mode[i][m], data, self.kernel))
                m += 1
                if mode[i][m].distance(mode[i][m - 1]) < self.threshold:
                    break
            mode[i][0] = mode[i][m]

        centroids = []
        for i in range(len(data)):
            if mode[i][0] not in centroids:
                centroids.append(mode[i][0])

        # labels = []
        # for i in range(len(data)):
        #     labels.append(centroids.index(mode[i][0]))

        self.centroids = centroids
        # self.labels = labels

    def predict(self, data: DataVector):
        labels = []
        for i in range(len(data)):
            nearest_centroid = self.centroids[0]
            for centroid in self.centroids:
                if data[i].distance(centroid) < data[i].distance(nearest_centroid):
                    nearest_centroid = centroid
            labels.append(self.centroids.index(nearest_centroid))
        return labels

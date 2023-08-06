from . import _cloud_geodesic
import numpy as np
import matplotlib.pyplot as plt
from typing import Optional


class FastMarchingTree:

    def __init__(self, points: np.ndarray, radius: float):
        self._tree = _cloud_geodesic._FastMarchingTree(points, radius)

    def span_tree(self, radius: Optional[float] = None) -> None:
        self._tree.span_tree(radius)

    def get_costs(self) -> np.ndarray:
        costs = self._tree.get_costs()
        return np.array(costs)

    def get_geodesic_path(self, dest_idx: int) -> np.ndarray:
        path = self._tree.get_geodesic_path(dest_idx)
        return np.array(path)

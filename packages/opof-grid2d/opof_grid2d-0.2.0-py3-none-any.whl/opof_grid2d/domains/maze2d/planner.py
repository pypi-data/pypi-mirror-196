import itertools
import re
from typing import Any, List, Optional, Tuple

import numpy as np
import opof
from sortedcontainers import SortedListWithKey


class Maze2DPlanner(opof.Planner):
    def __init__(self):
        pass

    def __call__(
        self,
        problem: Tuple[np.ndarray, Tuple[int, int], Tuple[int, int]],
        parameters: List[np.ndarray],
        extras: List[Any],
    ):
        (board, start, goal) = problem

        h_values = np.prod(board.shape) * parameters[0][
            -np.prod(board.shape) :
        ].reshape(board.shape)

        def h(n: Tuple[int, int]):
            return h_values[n]

        # Distances from start.
        g = np.ones(board.shape, dtype=np.int32) * np.iinfo(np.int32).max
        g[start] = 0

        # Open set.
        sf = np.zeros(board.shape, dtype=np.float32)
        sf[start] = h(start)
        s = SortedListWithKey([start], key=lambda n: sf[n])

        # Visit count.
        v = np.zeros(board.shape, dtype=np.int32)

        i = 0
        while True:
            i += 1

            n = s.pop(0)  # Get next node.
            v[n] += 1

            # Check goal.
            if n == goal:
                # Compute performance measure.
                performance = -(float(i) / (1 - board).sum())

                result = dict()
                result["objective"] = performance
                result["visits"] = v
                result["length"] = g[n]
                return result

            # Loop through neighbours.
            neighbours = [
                (n[0] - 1, n[1]),
                (n[0] + 1, n[1]),
                (n[0], n[1] - 1),
                (n[0], n[1] + 1),
            ]
            for nn in neighbours:
                # Check bounds.
                if nn[0] < 0 or nn[0] >= board.shape[0]:
                    continue
                if nn[1] < 0 or nn[1] >= board.shape[1]:
                    continue

                # Check collision.
                if board[nn]:
                    continue

                # Update g(nn) <- g(n) + 1 if smaller.
                if g[n] + 1 < g[nn]:
                    g[nn] = g[n] + 1

                    # Update open set.
                    sf[nn] = g[nn] + h(nn)
                    if nn in s:
                        s.remove(nn)
                    s.update([nn])

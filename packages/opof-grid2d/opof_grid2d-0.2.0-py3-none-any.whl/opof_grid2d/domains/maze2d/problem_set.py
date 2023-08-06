from typing import Tuple

import numpy as np
from mazelib.generate.Wilsons import Wilsons


def generate_problem(size: int) -> Tuple[np.ndarray, Tuple[int, int], Tuple[int, int]]:
    g = Wilsons(
        int((size + 1) / 2),
        int((size + 1) / 2),
        hunt_order="random",
    )
    while True:
        # The library generates this with a padding.
        board = g.generate()
        start = (
            np.random.randint(1, board.shape[0] - 1),
            np.random.randint(1, board.shape[1] - 1),
        )
        goal = (
            np.random.randint(1, board.shape[0] - 1),
            np.random.randint(1, board.shape[1] - 1),
        )
        if start == goal or board[start] or board[goal]:
            continue
        # Remove padding.
        return (
            board[1:-1, 1:-1],
            (start[0] - 1, start[1] - 1),
            (goal[0] - 1, goal[1] - 1),
        )

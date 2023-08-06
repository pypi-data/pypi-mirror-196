import matplotlib.pylab as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
from opof_grid2d.domains import Maze2D

SIZE = 11


def to_display(x):
    return np.rot90(x.transpose())


def cost_to_go(board, start):
    searched = np.zeros(board.shape, dtype=np.uint8)
    searched[start] = True
    g_values = np.zeros(board.shape, dtype=np.float32)
    l = [start]
    while len(l) > 0:
        n = l.pop(0)
        neighbours = [
            (n[0] - 1, n[1]),
            (n[0] + 1, n[1]),
            (n[0], n[1] - 1),
            (n[0], n[1] + 1),
        ]
        for nn in neighbours:
            if nn[0] < 0 or nn[0] >= board.shape[0]:
                continue
            if nn[1] < 0 or nn[1] >= board.shape[1]:
                continue
            if board[nn]:
                continue

            if searched[nn]:
                continue
            searched[nn] = True

            g_values[nn] = g_values[n] + 1
            l.append(nn)
    return g_values


if __name__ == "__main__":
    domain = Maze2D(SIZE)
    (board, start, goal) = domain.create_problem_set()()
    g_values = cost_to_go(board, start)
    h_values = np.zeros_like(board)
    for i in range(board.shape[0]):
        for j in range(board.shape[1]):
            h_values[(i, j)] = abs(i - goal[0]) + abs(j - goal[1])
    f_values = (g_values + h_values) * (1 - board)
    f_values /= f_values.max()

    fig = plt.figure(figsize=(12, 12))
    ax = fig.add_subplot(111)
    board[start] = 1  # Don't draw heuristics on start.
    board[goal] = 1  # Don't draw heuristics on goal.
    board = (board * 2) + 0.85 * (1 - f_values) * (1 - board)
    board[start] = 3
    board[goal] = 4
    ax.pcolormesh(
        np.arange(0, SIZE),
        np.arange(0, SIZE),
        to_display(board),
        cmap=LinearSegmentedColormap.from_list(
            "", ["white", "#FF0000", "silver", "lime", "fuchsia"]
        ),
    )
    ax.set_xticks([])
    ax.set_yticks([])

    plt.show()

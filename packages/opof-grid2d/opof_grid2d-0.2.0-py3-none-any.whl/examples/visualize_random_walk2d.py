import matplotlib.pylab as plt
import numpy as np
from matplotlib.colors import ListedColormap
from opof_grid2d.domains import RandomWalk2D

SIZE = 11

if __name__ == "__main__":
    domain = RandomWalk2D(SIZE)
    (board, start, goal) = domain.create_problem_set()()

    fig = plt.figure(figsize=(12, 12))
    ax = fig.add_subplot(111)
    board[start] = 2
    board[goal] = 3
    ax.pcolormesh(
        np.arange(0, SIZE),
        np.arange(0, SIZE),
        board,
        cmap=ListedColormap(["white", "black", "lime", "fuchsia"]),
        alpha=0.8,
        linewidth=1,
        edgecolor="silver",
    )
    ax.set_xticks([])
    ax.set_yticks([])

    plt.show()

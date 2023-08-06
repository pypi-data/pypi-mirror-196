import pytest
import torch
from opof.algorithms import GC

from opof_grid2d.domains import Maze2D, RandomWalk2D

torch.set_num_threads(1)


@pytest.mark.timeout(600)
def test_train_RandomWalk2D_GC():
    domain = RandomWalk2D(11)
    algorithm = GC(domain, iterations=10, min_buffer_size=10, eval_interval=5)
    algorithm()


@pytest.mark.timeout(600)
def test_train_Maze2D_GC():
    domain = Maze2D(11)
    algorithm = GC(domain, iterations=10, min_buffer_size=10, eval_interval=5)
    algorithm()

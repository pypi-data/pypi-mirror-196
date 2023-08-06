import pickle
import re
from glob import glob
from typing import List, Optional, Tuple

import numpy as np
import pkg_resources
import torch

from opof import Domain
from opof.evaluators import ListEvaluator
from opof.parameter_spaces import Interval
from opof.problem_sets import ProblemList

from .planner import Maze2DPlanner


class Maze2D(Domain):
    maze_size: int
    train_problems: List[Tuple[np.ndarray, Tuple[int, int], Tuple[int, int]]]
    test_problems: List[Tuple[np.ndarray, Tuple[int, int], Tuple[int, int]]]

    def __init__(self, maze_size: int):
        assert maze_size % 2 == 1
        self.maze_size = maze_size

        self.train_problems = []
        self.test_problems = []
        for (p, t) in zip(
            ["train", "test"],
            [self.train_problems, self.test_problems],
            # Running MLP on CPU is too slow so we limit this.
        ):
            for path in sorted(
                glob(
                    pkg_resources.resource_filename(
                        "opof_grid2d", f"datasets/maze2d/{maze_size}/{p}/*.pt"
                    )
                )
            ):
                with open(path, "rb") as f:
                    t.append(pickle.load(f))

    def create_problem_set(self):
        return ProblemList(self.train_problems)

    def composite_parameter_space(self):
        return [Interval(self.maze_size * self.maze_size)]

    def create_planner(self):
        return Maze2DPlanner()

    def create_problem_embedding(self):
        class MazeEmbedding(torch.nn.Module):
            def __init__(self):
                super(MazeEmbedding, self).__init__()
                self.dummy_param = torch.nn.Parameter(torch.empty(0))

            def forward(self, problems):
                device = self.dummy_param.device
                dtype = self.dummy_param.dtype
                boards = torch.tensor(
                    np.array([p[0] for p in problems]), device=device, dtype=dtype
                )
                boards = boards.flatten(start_dim=1)
                starts = torch.tensor(
                    np.array([p[1] for p in problems]), device=device, dtype=dtype
                )
                goals = torch.tensor(
                    np.array([p[2] for p in problems]), device=device, dtype=dtype
                )
                return torch.concat([boards, starts, goals], dim=-1)

        return MazeEmbedding()

    def create_evaluator(self):
        return ListEvaluator(self, self.test_problems)

import pickle
from glob import glob
from typing import List, Tuple

import numpy as np
import pkg_resources
import torch

from opof import Domain
from opof.evaluators import ListEvaluator
from opof.parameter_spaces import Simplex
from opof.problem_sets import ProblemList


def generate_problem(size: int, obstacles: int):
    # Helper method to sample free position on a board.
    def rand_pos():
        return (np.random.randint(0, size), np.random.randint(0, size))

    board = np.zeros((size, size), dtype=np.uint8)
    start = rand_pos()
    while True:
        goal = rand_pos()
        if goal != start:
            break
    for _ in range(obstacles):
        while True:
            obstacle = rand_pos()
            if obstacle != start and obstacle != goal and not board[obstacle]:
                board[obstacle] = 1
                break

    return (board, start, goal)


class RandomWalk2D(Domain):
    train_problems: List[Tuple[np.ndarray, Tuple[int, int], Tuple[int, int]]]
    test_problems: List[Tuple[np.ndarray, Tuple[int, int], Tuple[int, int]]]

    def __init__(self, size):
        self.size = size
        self.max_steps = 4 * size**2
        self.train_problems = []
        self.test_problems = []
        for (p, t) in zip(
            ["train", "test"],
            [self.train_problems, self.test_problems],
        ):
            for path in sorted(
                glob(
                    pkg_resources.resource_filename(
                        "opof_grid2d", f"datasets/random_walk2d/{self.size}/{p}/*.pt"
                    )
                )
            ):
                with open(path, "rb") as f:
                    t.append(pickle.load(f))

    def create_problem_set(self):
        return ProblemList(self.train_problems)

    def composite_parameter_space(self):
        return [Simplex(1, 4)]

    def create_planner(self):
        def planner(problem, parameters, extras):
            # Extract problem information.
            (board, start, goal) = problem
            # Extract parameters.
            probs = parameters[0][0]

            # Run random walk.
            pos = start
            steps = 0
            while True:
                # Compute next position.
                action = np.random.choice(4, p=probs)
                action = [(1, 0), (-1, 0), (0, 1), (0, -1)][action]
                next_pos = (pos[0] + action[0], pos[1] + action[1])

                # Move only if valid.
                if not (
                    pos[0] < 0
                    or pos[0] >= self.size
                    or pos[1] < 0
                    or pos[1] >= self.size
                    or board[pos]
                ):
                    pos = next_pos

                # Add to steps.
                steps += 1

                # Check termination
                if pos == goal:
                    break
                if steps >= self.max_steps:
                    break

            # OPOF maximizes objective, but we want to minimze steps.
            # So we add the negative as objective.
            return {"objective": -steps / self.max_steps}

        return planner

    def create_problem_embedding(self):
        class RandomWalkEmbedding(torch.nn.Module):
            def __init__(self):
                super(RandomWalkEmbedding, self).__init__()
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

        return RandomWalkEmbedding()

    def create_evaluator(self):
        return ListEvaluator(self, self.test_problems)

import multiprocessing as mp
import pickle
import sys
from pathlib import Path

from opof_grid2d.domains.maze2d.problem_set import generate_problem
from tqdm import tqdm

from opof.registry import concurrency

if __name__ == "__main__":
    size = int(sys.argv[1])
    count = int(sys.argv[2])

    for output in ["train", "test"]:
        with mp.Pool(concurrency()) as p:
            for (i, x) in tqdm(
                enumerate(p.imap_unordered(generate_problem, [size] * count)),
                total=count,
                desc=f"Sampling {output} set...",
            ):
                path = Path(
                    f"../opof_grid2d/datasets/maze2d/{size}/{output}/{i:06d}.pt"
                )
                path.parent.mkdir(parents=True, exist_ok=True)
                with path.open("wb") as f:
                    pickle.dump(x, f)

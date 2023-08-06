import pickle
import sys
from pathlib import Path

from opof_grid2d.domains.random_walk2d.domain import generate_problem
from tqdm import tqdm

if __name__ == "__main__":
    size = int(sys.argv[1])
    count = int(sys.argv[2])

    for output in ["train", "test"]:
        for (i, x) in tqdm(enumerate(range(count)), desc=f"Sampling {output} set..."):
            p = generate_problem(size, int(size / 2))
            path = Path(
                f"../opof_grid2d/datasets/random_walk2d/{size}/{output}/{i:06d}.pt"
            )
            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open("wb") as f:
                pickle.dump(p, f)

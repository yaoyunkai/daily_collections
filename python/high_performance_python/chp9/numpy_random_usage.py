"""
numpy_random_usage.py


created at 2026-08-04
"""

import numpy as np


def run():
    rng = np.random.default_rng()
    arr = rng.random(100)
    # arr.mean()


if __name__ == "__main__":
    run()

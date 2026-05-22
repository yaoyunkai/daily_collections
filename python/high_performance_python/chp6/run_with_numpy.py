"""
run_with_numpy.py


created at 2026-05-22
"""

from array import array

import numpy as np


def norm_square_list(vector):
    norm = 0
    for v in vector:
        norm += v * v
    return norm


def norm_square_list_comprehension(vector):
    return sum([v * v for v in vector])


def norm_square_array(vector):
    norm = 0
    for v in vector:
        norm += v * v
    return norm


def norm_square_numpy(vector):
    return np.sum(vector * vector)


def norm_square_numpy_dot(vector):
    return np.dot(vector, vector)

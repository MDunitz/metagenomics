import numpy as np
import numba
rng = np.random.default_rng()


@numba.njit
def draw_perm_sample(x, y):
    """Generate a permutation sample."""
    concat_data = np.concatenate((x, y))
    np.random.shuffle(concat_data)

    return concat_data[:len(x)], concat_data[len(x):]


def draw_perm_reps(x, y, stat_fun, size=1):
    """Generate array of permuation replicates."""
    return np.array([stat_fun(*draw_perm_sample(x, y)) for _ in range(size)])


@numba.njit
def draw_perm_reps_diff_mean(x, y, size=1):
    """Generate array of permuation replicates."""
    out = np.empty(size)
    for i in range(size):
        x_perm, y_perm = draw_perm_sample(x, y)
        out[i] = np.mean(x_perm) - np.mean(y_perm)

    return out
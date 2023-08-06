from __future__ import annotations

import numpy as np

def estimator(l, a : float, b : float, probits = False, **kwargs) -> tuple[list, list]:
    """
    Calculated estimated probability/probits according to :math:`F(t_{i}) = \\frac{i - a}{n + b}` with:
    - :math:`n`: the length of `l`
    - :math:`i`: the :math:`i^{th}` element of `l`
    
    Parameters
    ----------
    l
        object to apply estimator to.
    a : float
        term `a` in equation
    b : float
        term `b` in equation
    probits : bool, default False
        Whether return estimated values in probits (True) or in percentage (False)
    Returns
    -------
    sorted_input : array
        Sorted copy of the input
    probabilty_data : array
        Estimated probability data
    """
    arr = np.array(l if hasattr(l, "__iter__") else [l]).flatten()
    arr.sort()
    prob = _get_prob_data(arr.size, a, b, probits)
    return arr, prob

def benard_estimator(l, **kwargs):
    """Benard estimator abstraction of :func:`estimator` with :math:`a = 0.3` and :math:`b = 0.4`."""
    return estimator(l, 0.3, 0.4, **kwargs)

def _get_prob_data(size : int, a : int, b : int, probits : bool, dist = None):
    arr = ((np.arange(1, size + 1) - a) / (size + b))

    if probits:
        import statistics
        dist = dist or statistics.NormalDist()
        return np.vectorize(dist.pff)(arr)
    else:
        return arr * 100
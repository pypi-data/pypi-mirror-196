import pytest

from semicond import stats

import numpy as np

def test_benard_estimator():
    sorted_data, prob_data = stats.benard_estimator([2, 1, 3])
    assert (sorted_data == np.array([1, 2, 3])).all()
    assert (prob_data == np.array([(x - 0.3) / (3 + 0.4) * 100 for x in range(1, 4)])).all()
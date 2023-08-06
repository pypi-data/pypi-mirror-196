"""Module for expanding matplotlib scales with 'normal' scale"""

import matplotlib as mpl
from matplotlib.scale import register_scale, ScaleBase
from matplotlib.transforms import Transform
from matplotlib.ticker import NullFormatter, NullLocator, FixedLocator
import numpy as np
from numpy import ma
from statistics import NormalDist

class NormalScale(ScaleBase):
    name = "normal"
    dist = NormalDist()
    _fallback_margin = 1e-5

    def __init__(self, axis, **kwargs):
        super().__init__(axis)

    def get_transform(self):
        return self.NormalTransform(self.dist)

    def set_default_locators_and_formatters(self, axis):
        axis.set(
            major_locator = FixedLocator([1, 10, 30, 50, 70, 90, 99]),
            # major_locator = NullLocator(),
            # minor_locator = NullLocator(),
            # major_formatter = NullFormatter(),
            # minor_formatter = NullFormatter(),
        )

    def limit_range_for_scale(self, vmin, vmax, minpos):
        """Limit domain to 0-100 (excluding boundaries)."""
        return (
            self._fallback_margin if vmin <= 0 else vmin,
            (100 - self._fallback_margin) if vmax >= 100 else vmax
        )

    class NormalTransform(Transform):
        input_dims = output_dims = 1

        def __init__(self, dist : NormalDist):
            super().__init__()
            self.dist = dist
            self._transform = np.vectorize(self._transform_function)

        def transform_non_affine(self, a):
            a = np.asanyarray(a)

            if a.size == 0:
                return np.array([])

            masked = ma.masked_where((a <= 0) | (a >= 100), a)
            return self._transform(masked)

        def inverted(self):
            return NormalScale.InvertedNormalTransform(self.dist)

        def _transform_function(self, x):
            try:
                return self.dist.inv_cdf(x / 100)
            except:
                return 1e-5

    class InvertedNormalTransform(Transform):
        input_dims = output_dims = 1

        def __init__(self, dist : NormalDist):
            super().__init__()
            self.dist = dist
            self._transform = np.vectorize(lambda x: self.dist.cdf(x) * 100)

        def transform_non_affine(self, a):
            a = np.asanyarray(a)
            return self._transform(a)

        def inverted(self):
            return NormalScale.NormalTransform(self.dist)

register_scale(NormalScale)
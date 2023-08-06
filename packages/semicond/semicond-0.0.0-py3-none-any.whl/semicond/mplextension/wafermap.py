from __future__ import annotations

import matplotlib as mpl
import matplotlib.pyplot as plt

import pandas as pd
import seaborn as sns 

from enum import IntEnum
from matplotlib.patches import Ellipse

from typing import Literal

class WaferSize(IntEnum):
    W300 = 300
    W200 = 200
    W150 = 150
    W100 = 100

def wafermap(
    data : pd.DataFrame,
    diesize : tuple[float, float],
    wafersize : WaferSize = WaferSize.W300,
    center : tuple[float, float] = None,
    offset : tuple[float, float] = None,
    ax : mpl.axes.Axes = None,
    kind : Literal["indexed", "mm"] = "indexed",
    **kwargs
) -> mpl.axes.Axes:
    """
    Seaborn like function for plotting wafermaps.

    Two kind of plots:

    - indexed: plot characteristics with indices of the different dies
    - mm: plot characteristics in absolute position (mm)

    Parameters
    ----------
    data : pd.DataFrame
        Data to plot
    diesize : tuple[float, float]
        Size of one die (x-size, y-size) in mm
    wafersize : WaferSize, default WaferSize.W300
        Size of the wafer
    center : tuple[float, float], default None
        Center of the wafermap (x, y) in mm
    offset : tuple[float, float], default None
        Offset of the center die (x, y) in mm
    ax : mpl.axes.Axes, default None
        Axes to plot on
    kind : {"indexed", "mm"}, default "indexed"
        Kind of plot to do

    Returns
    -------
    ax : mpl.axes.Axes
        Axes with the plot
    """
    ax = ax or plt.gca()
    if kind == "indexed":
        if center is None:
            xdies, ydies = _get_die_number(offset, wafersize, diesize)
            xc = xdies / 2
            yc = ydies / 2
        else:
            xc, yc = center
        
        xdim, ydim = (
            wafersize.value / diesize[0],
            wafersize.value / diesize[1],
        )
        
        sns.heatmap(data, ax = ax, **kwargs)

        main_circ = Ellipse(
            xy = (xc, yc),
            width = xdim,
            height = ydim,
            color = "#777777",
            zorder = -2,
        )
        notch_circ = Ellipse(
            xy = (xc, yc - ydim / 2),
            width = xdim / 50,
            height = ydim / 50,
            color = "white",
            zorder = -1,
        )
        ax.add_patch(main_circ)
        ax.add_patch(notch_circ)
        ax.set_xlim(xc - xdim / 1.9, xc + xdim / 1.9)
        ax.set_ylim(yc - ydim / 1.9, yc + ydim / 1.9)
    elif kind == "mm":
        pass
    else:
        raise ValueError(f"Unknown kind: {kind}, should be 'indexed' or 'mm'")
    
def _get_die_number(
    offset : tuple[float, float],
    wafersize : WaferSize, 
    diesize : tuple[float, float]
) -> tuple[int, int]:
    if offset is None:
        xr = (wafersize / 2 - diesize[0] / 2) // diesize[0]
        yr = (wafersize / 2 - diesize[1] / 2) // diesize[1]
        return xr * 2 + 1, yr * 2 + 1
    else:
        raise NotImplementedError("Offset not implemented yet")
    
from importlib.metadata import distribution
__version__ = distribution("semicond").version

def ensure_list(obj) -> list:
    """
    Transforms obj into list.

    Parameters
    ----------
    obj : Any
        Any object that you can think of
    
    Returns
    -------
    listed_obj : list
        Object return into a list
    """
    if isinstance(obj, str):
        return [obj]
    elif hasattr(obj, "__iter__"):
        return list(obj)
    elif obj is None:
        return []
    else:
        return [obj]
    
from .stats import benard_estimator, estimator
from .mplextension import WaferSize, wafermap
    
__all__ = [
    "ensure_list",
    # stats
    "benard_estimator",
    "estimator",
    # mplextension
    "WaferSize",
    "wafermap",
]
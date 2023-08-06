import pandas
import numpy
import torch

from .tools import fetch_num_rows

def verify_array(data):
    return isinstance(data, numpy.ndarray)

def verify_dataframe(data):
    return isinstance(data, pandas.core.frame.DataFrame) 

def verify_series(data):
    return isinstance(data, pandas.core.series.Series)

def verify_tensor(data):
    return isinstance(data, torch.Tensor)

def verify_list(data):
    return isinstance(data, list)

def verify_number(data):
    return isinstance(data, int) or isinstance(data, float)

def verify_consistent_rows(*tensors):
    """
    Check that all tensors have consistent first dimensions.
    Checks whether all objects in tensors have the same number of rows or length.

    Parameters
    ----------
    *tensors : list or tuple of input objects.
        Objects that will be checked for consistent length.
    """
    num_rows = [fetch_num_rows(tensor) for tensor in tensors if tensor is not None]
    unique = len(set(num_rows))
    if unique > 1:
        raise ValueError(f'Found input variables with inconsistent numbers of rows: {[int(l) for l in num_rows]}')
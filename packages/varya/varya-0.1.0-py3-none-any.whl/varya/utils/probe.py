import torch
from .tools import fetch_num_rows

def probe_tensor(tensor):
    if isinstance(tensor, torch.Tensor):
        return tensor
    else:
        raise TypeError(f'Expected torch.Tensor, got {type(tensor)}.')

def probe_regression_targets(y_true, y_pred):
    
    y_true = probe_tensor(y_true)
    y_pred = probe_tensor(y_pred)

    if y_true.ndimension() == 1:
        y_true = y_true.view(-1, 1)
    
    if y_pred.ndimension() == 1:
        y_pred = y_pred.view(-1, 1)

    if fetch_num_rows(y_true) != fetch_num_rows(y_pred):
        raise ValueError(
            f'y_true and y_pred have different number of rows ({fetch_num_rows(y_true)}!={fetch_num_rows(y_pred)})'
            )
    
    return y_true, y_pred
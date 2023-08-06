import torch

def verify_tensor(data):
    return isinstance(data, torch.Tensor)

def fetch_num_rows(tensor):
    if verify_tensor(tensor):
        return tensor.shape[0]

def fetch_num_columns(tensor):
    if verify_tensor(tensor):
        return tensor.shape[1]
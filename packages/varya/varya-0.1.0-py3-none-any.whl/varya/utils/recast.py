import torch
from .verify import (
    verify_array,
    verify_series,
    verify_tensor,
    verify_list,
    verify_dataframe,
    verify_number
)

def recast_to_tensor(data, dtype=torch.float64):
    
    if verify_array(data):
        return torch.from_numpy(data).to(dtype)
    
    if verify_dataframe(data):
        return torch.from_numpy(data.values).to(dtype)
    
    if verify_series(data):
        return torch.from_numpy(data.values).to(dtype)
    
    if verify_list(data):
        return torch.tensor(data).to(dtype)
    
    if verify_tensor(data):
        return data.to(dtype)

    if verify_number(data):
        return torch.tensor([data]).to(dtype)
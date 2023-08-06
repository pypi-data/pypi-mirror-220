
import torch



def align_station_dict(in_model_path, out_model_path):
    in_model = torch.load(in_model_path)
    out_model = torch.load(out_model_path)

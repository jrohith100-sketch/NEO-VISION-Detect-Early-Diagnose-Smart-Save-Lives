import torch
import torch.nn as nn
from torchvision import models

DEVICE = "cpu"


def load_ct_model(path):
    model = models.resnet18(weights=None)
    model.fc = nn.Linear(model.fc.in_features, 2)
    model.load_state_dict(torch.load(path, map_location=DEVICE))
    model.eval()
    return model



def load_mri_model(path):
    model = models.resnet18(weights=None)
    model.fc = nn.Linear(model.fc.in_features, 4)  
    model.load_state_dict(torch.load(path, map_location=DEVICE))
    model.eval()
    return model



class FusionModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.linear = nn.Linear(6, 4)  

    def forward(self, x):
        return self.linear(x)




def load_fusion_model(path):
    model = FusionModel()
    model.load_state_dict(torch.load(path, map_location=DEVICE))
    model.eval()
    return model

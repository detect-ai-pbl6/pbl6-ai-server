from functools import lru_cache

import torch

from networks.resnet import resnet50


@lru_cache
def load_model(model_path):
    model = resnet50(num_classes=1)
    try:
        state_dict = torch.load(
            model_path, map_location="cpu", weights_only=True
        )  # noqa
        model.load_state_dict(state_dict["model"])

        model.eval()
        return model
    except Exception:
        raise

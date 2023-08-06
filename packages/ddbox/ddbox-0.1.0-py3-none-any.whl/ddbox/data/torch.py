import os
from typing import List

import pandas as pd
from torch.utils.data import Dataset
from torchvision.io import read_image

from ddbox.data.utils.loaders import MosesDataLoader

__all__ = ['MosesDataset']


class MosesDataset(Dataset):

    def __init__(self, split: str = 'train', attributes: List[str] = ['smiles'], transform=None):
        self.data_loader = MosesDataLoader(split, attributes)
        self.transform = transform
        self.data_loader.download()

    def __len__(self):
        return self.data_loader.get_total()

    def __getitem__(self, idx):
        item = self.data_loader.get(idx, 1)
        if self.transform:
            item = self.transform(item)
        return item

import io
from typing import *

import pandas as pd
import requests


class ZINCDatasetService:

    base_url: str

    def __init__(self, base_url: str) -> None:
        self.base_url = base_url

    def load(self, params: Mapping[str, str]) -> pd.DataFrame:
        response = requests.get(self.base_url + '/rest/1.0/property/mols/', params=params)
        print(response.text)
        # df = pd.read_csv(io.StringIO(response.text), sep=' ', header=None, names=['SMILES'])
        # return df

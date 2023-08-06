import pandas as pd  # for typehinting below
from IPython.display import display
from rdkit import Chem
from rdkit.Chem import PandasTools
from smallworld_api import SmallWorld

aspirin = 'O=C(C)Oc1ccccc1C(=O)O'
sw = SmallWorld()
results: pd.DataFrame = sw.search(aspirin, dist=5, db=sw.REAL_dataset)


display(results)

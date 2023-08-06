from typing import List

from fcd_torch import FCD
from rdkit import Chem

from ddbox.registries import metrics_regstry


@metrics_regstry.register('FCD')
def fcd(generated_molecules: List[Chem.rdchem.Mol], reference_molecules: List[Chem.rdchem.Mol]):
    fcd = FCD()
    return fcd([Chem.MolToSmiles(molecule) for molecule in generated_molecules], [Chem.MolToSmiles(molecule) for molecule in reference_molecules])

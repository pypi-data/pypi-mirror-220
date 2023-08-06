from typing import List

from ddbox.metrics.utils import get_molecule_from_smiles_if_valid_or_none
from ddbox.registries import metrics_regstry


@metrics_regstry.register('fraction_valid')
def fraction_valid(smiles_list: List[str]):
    count = 0
    total = len(smiles_list)
    for smiles in smiles_list:
        molecule = get_molecule_from_smiles_if_valid_or_none(smiles)
        if molecule is not None:
            count += 1
    return count / total

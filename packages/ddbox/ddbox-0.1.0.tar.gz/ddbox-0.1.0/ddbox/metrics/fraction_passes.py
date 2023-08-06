import os
from typing import List

import numpy as np
import pandas as pd
from rdkit import Chem

from ddbox.registries import metrics_regstry

_base_dir = os.path.split(__file__)[0]
_mcf = pd.read_csv(os.path.join(_base_dir, 'data/mcf.csv'))
_pains = pd.read_csv(os.path.join(_base_dir, 'data/wehi_pains.csv'),
                     names=['smarts', 'names'])
_filters = [Chem.MolFromSmarts(x) for x in _mcf._append(_pains, sort=True)['smarts'].values]


def molecule_passes_filters(molecule,
                            allowed=None,
                            isomericSmiles=False):
    allowed = allowed or {'C', 'N', 'S', 'O', 'F', 'Cl', 'Br', 'H'}
    if molecule is None:
        return False
    ring_info = molecule.GetRingInfo()
    if ring_info.NumRings() != 0 and any(
            len(x) >= 8 for x in ring_info.AtomRings()
    ):
        return False
    h_molecule = Chem.AddHs(molecule)
    if any(atom.GetFormalCharge() != 0 for atom in molecule.GetAtoms()):
        return False
    if any(atom.GetSymbol() not in allowed for atom in molecule.GetAtoms()):
        return False
    if any(h_molecule.HasSubstructMatch(smarts) for smarts in _filters):
        return False
    smiles = Chem.MolToSmiles(molecule, isomericSmiles=isomericSmiles)
    if smiles is None or len(smiles) == 0:
        return False
    if Chem.MolFromSmiles(smiles) is None:
        return False
    return True


@metrics_regstry.register('fraction_passes')
def fraction_passes(molecules: List[Chem.rdchem.Mol]):
    passes = []
    for molecule in molecules:
        passes.append(molecule_passes_filters(molecule))
    return np.mean(passes)

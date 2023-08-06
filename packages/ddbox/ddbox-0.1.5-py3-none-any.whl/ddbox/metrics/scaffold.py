from collections import Counter
from typing import List

from rdkit import Chem
from rdkit.Chem.Scaffolds import MurckoScaffold

from ddbox.metrics.utils import cos_similarity
from ddbox.registries import metrics_regstry


def compute_scaffold(molecule, min_rings=2):
    try:
        scaffold = MurckoScaffold.GetScaffoldForMol(molecule)
    except (ValueError, RuntimeError):
        return None
    n_rings = scaffold.GetRingInfo().NumRings()
    scaffold_smiles = Chem.MolToSmiles(scaffold)
    if scaffold_smiles == '' or n_rings < min_rings:
        return None
    return scaffold_smiles


def compute_scaffolds(molecules, min_rings=2):
    scaffolds = Counter([compute_scaffold(molecule, min_rings=min_rings) for molecule in molecules])
    if None in scaffolds:
        scaffolds.pop(None)
    return scaffolds


@metrics_regstry.register('Scaf')
def scaf_metric(generated_molecules: List[Chem.rdchem.Mol], reference_molecules: List[Chem.rdchem.Mol]):
    scaffolds_of_generated = compute_scaffolds(generated_molecules)
    scaffolds_of_reference = compute_scaffolds(reference_molecules)
    return cos_similarity(scaffolds_of_generated, scaffolds_of_reference)

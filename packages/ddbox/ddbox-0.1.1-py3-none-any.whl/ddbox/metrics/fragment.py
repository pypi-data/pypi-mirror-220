from collections import Counter
from typing import List

import numpy as np
from rdkit import Chem
from rdkit.Chem import AllChem

from ddbox.metrics.utils import cos_similarity
from ddbox.registries import metrics_regstry


def fragmenter(molecule):
    fgs = AllChem.FragmentOnBRICSBonds(molecule)
    fgs_smi = Chem.MolToSmiles(fgs).split(".")
    return fgs_smi


def compute_fragments(molecules):
    fragments = Counter()
    for molecule in molecules:
        fragment = fragmenter(molecule)
        fragments.update(fragment)
    return fragments


@metrics_regstry.register('Frag')
def frag_metric(generated_molecules: List[Chem.rdchem.Mol], reference_molecules: List[Chem.rdchem.Mol]):
    fragments_of_generated = compute_fragments(generated_molecules)
    fragments_of_reference = compute_fragments(reference_molecules)
    return cos_similarity(fragments_of_generated, fragments_of_reference)

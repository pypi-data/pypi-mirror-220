from typing import List

from rdkit import Chem

from ddbox.metrics.utils import average_agg_tanimoto, fingerprints
from ddbox.registries import metrics_regstry


@metrics_regstry.register('SNN')
def metric(generated_molecules: List[Chem.rdchem.Mol], reference_molecules: List[Chem.rdchem.Mol]):
    return average_agg_tanimoto(fingerprints(generated_molecules, fp_type='morgan'), fingerprints(reference_molecules, fp_type='morgan'))

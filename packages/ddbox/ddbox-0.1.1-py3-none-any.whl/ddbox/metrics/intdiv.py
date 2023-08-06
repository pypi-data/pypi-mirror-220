from typing import List

from rdkit import Chem

from ddbox.metrics.utils import average_agg_tanimoto, fingerprints
from ddbox.registries import metrics_regstry


def internal_diversity(molecules: List[Chem.rdchem.Mol], fp_type='morgan', p=1):
    fps = fingerprints(molecules, fp_type=fp_type)
    return 1 - (average_agg_tanimoto(fps, fps, agg='mean', p=p)).mean()


@metrics_regstry.register('IntDiv')
def intdiv_metric(molecules: List[Chem.rdchem.Mol]):
    return internal_diversity(molecules)


@metrics_regstry.register('IntDiv2')
def intdiv2_metric(molecules: List[Chem.rdchem.Mol]):
    return internal_diversity(molecules, p=2)

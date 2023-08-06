import logging
from typing import *
from typing import List

from ddbox.metrics import metrics_regstry
from ddbox.metrics.utils import get_molecule_from_smiles_if_valid_or_none

logger = logging.getLogger(__name__)


def compute_metrics(smiles_generated: List[str], smilest_reference: List[str], metrics: List[str] = [
    'fraction_valid',
    'fraction_unique',
    'fraction_passes',
    'IntDiv',
    'IntDiv2',
    'FCD',
    'SNN',
    'Frag',
    'Scaf',
    'DistributionDifferenceLogP',
    'DistributionDifferenceSA',
    'DistributionDifferenceQED',
    'DistributionDifferenceWeight',
]):
    test_molecules = [get_molecule_from_smiles_if_valid_or_none(smiles) for smiles in smilest_reference]

    molecules = [get_molecule_from_smiles_if_valid_or_none(smiles) for smiles in smiles_generated]
    molecules = [molecule for molecule in molecules if molecule is not None]

    results = {}

    if 'fraction_valid' in metrics:
        logger.info("Computing: fraction_valid")
        results['fraction_valid'] = metrics_regstry.eval('fraction_valid', smiles_generated)

    if 'fraction_unique' in metrics:
        logger.info("Computing: fraction_unique")
        results['fraction_unique'] = metrics_regstry.eval('fraction_unique', smiles_generated)

    if 'fraction_passes' in metrics:
        logger.info("Computing: fraction_passes")
        results['fraction_passes'] = metrics_regstry.eval('fraction_passes', molecules)

    if 'IntDiv' in metrics:
        logger.info("Computing: IntDiv")
        results['IntDiv'] = metrics_regstry.eval('IntDiv', molecules)

    if 'IntDiv2' in metrics:
        logger.info("Computing: IntDiv2")
        results['IntDiv2'] = metrics_regstry.eval('IntDiv2', molecules)

    if 'FCD' in metrics:
        logger.info("Computing: FCD")
        results['FCD'] = metrics_regstry.eval('FCD', molecules, test_molecules)

    if 'SNN' in metrics:
        logger.info("Computing: SNN")
        results['SNN'] = metrics_regstry.eval('SNN', molecules, test_molecules)

    if 'Frag' in metrics:
        logger.info("Computing: Frag")
        results['Frag'] = metrics_regstry.eval('Frag', molecules, test_molecules)

    if 'Scaf' in metrics:
        logger.info("Computing: Scaf")
        results['Scaf'] = metrics_regstry.eval('Scaf', molecules, test_molecules)

    if 'DistributionDifferenceLogP' in metrics:
        logger.info("Computing: DistributionDifferenceLogP")
        results['DistributionDifferenceLogP'] = metrics_regstry.eval('DistributionDifferenceLogP', molecules, test_molecules)

    if 'DistributionDifferenceSA' in metrics:
        logger.info("Computing: DistributionDifferenceSA")
        results['DistributionDifferenceSA'] = metrics_regstry.eval('DistributionDifferenceSA', molecules, test_molecules)

    if 'DistributionDifferenceQED' in metrics:
        logger.info("Computing: DistributionDifferenceQED")
        results['DistributionDifferenceQED'] = metrics_regstry.eval('DistributionDifferenceQED', molecules, test_molecules)

    if 'DistributionDifferenceWeight' in metrics:
        logger.info("Computing: DistributionDifferenceWeight")
        results['DistributionDifferenceWeight'] = metrics_regstry.eval('DistributionDifferenceWeight', molecules, test_molecules)

    return results

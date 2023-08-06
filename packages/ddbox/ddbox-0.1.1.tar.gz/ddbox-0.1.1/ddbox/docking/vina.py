import logging
from subprocess import PIPE, Popen
from typing import Tuple

from ddbox.docking.utils.vina import (
    download_if_needed,
    get_config_filepath,
    get_pdbqt_file_from_smiles,
    get_pdbqt_filepath,
    get_vina_filepath,
)

logger = logging.getLogger(__name__)


def vina_docking(receptor_id: str, ligand_smiles: str, center: Tuple[float, float, float] | None = None, size: Tuple[float, float, float] | None = None):
    download_if_needed(receptor_id)

    ligand_path = get_pdbqt_file_from_smiles(ligand_smiles)
    receptor_path = get_pdbqt_filepath(receptor_id)
    config_path = get_config_filepath(receptor_id)

    command = [
        get_vina_filepath(),
        '--receptor', receptor_path,
        '--ligand', ligand_path,
        '--config', config_path,
    ]
    if center is not None:
        command.extend([
            '--center_x', str(center[0]),
            '--center_y', str(center[1]),
            '--center_z', str(center[2]),
        ])
    if size is not None:
        command.extend([
            '--size_x', str(size[0]),
            '--size_y', str(size[1]),
            '--size_z', str(size[2]),
        ])
    p = Popen(command, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate()
    if p.returncode != 0:
        raise Exception(err.decode())

    *name, ext = ligand_path.split('.')
    name = '.'.join(name)
    return '%s_out.%s' % (name, ext)

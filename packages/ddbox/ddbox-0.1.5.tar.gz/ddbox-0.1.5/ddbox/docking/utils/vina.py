import logging
import os
import platform
import time
from subprocess import PIPE, Popen

import requests
from tqdm import tqdm

from ddbox.configs import BASE_API_URL, BINARIES_DIR, DOCKING_CACHE, VINA_RECEPTORS_CACHE
from ddbox.utils import ensure_path, exists_file, get_random_uuid_hex

logger = logging.getLogger(__name__)


RECEPTORS_INFO_API_URL = BASE_API_URL + '/data/docking/receptors/info/'
RECEPTORS_API_URL = BASE_API_URL + '/data/docking/receptors/'
RECEPTORS_DETAIL_API_URL = BASE_API_URL + '/data/docking/receptors/%(receptor_id)s/'


def get_pdbqt_filepath(receptor_id: str):
    pdbqt_filename = '%s_target.pdbqt' % receptor_id
    pdbqt_filepath = os.path.join(VINA_RECEPTORS_CACHE, pdbqt_filename)
    return pdbqt_filepath


def get_config_filepath(receptor_id: str):
    config_filename = '%s_conf.txt' % receptor_id
    config_filepath = os.path.join(VINA_RECEPTORS_CACHE, config_filename)
    return config_filepath


def check_if_downloaded(receptor_id: str):
    if not exists_file(get_pdbqt_filepath(receptor_id)) or \
            not exists_file(get_config_filepath(receptor_id)):
        return False
    return True


def download_file(url: str, output_path: str):
    ensure_path(os.path.dirname(output_path))
    attempts = 3
    while attempts > 0:
        try:
            response = requests.get(url)
            with open(output_path, 'wb') as f:
                f.write(response.content)
            return
        except Exception as err:
            attempts -= 1
            logger.warn(err)
            time.sleep(3)
    raise Exception("Could not download: %s" % url)


def download_if_needed(receptor_id: str):
    if not check_if_downloaded(receptor_id):
        attempts = 3
        while attempts > 0:
            try:
                response = requests.get(RECEPTORS_DETAIL_API_URL % {'receptor_id': receptor_id})
                if response.status_code != 200:
                    raise Exception(response.text)
                data = response.json()
                download_file(data['vina']['pdbqt_url'], get_pdbqt_filepath(receptor_id))
                download_file(data['vina']['config_url'], get_config_filepath(receptor_id))
                return
            except Exception as err:
                attempts -= 1
                logger.warn(err)
                time.sleep(3)
        raise Exception("Could not download: %s" % receptor_id)


def get_vina_filepath() -> str:
    system_name = platform.system()
    if system_name == 'Linux':
        machine_name = platform.machine()
        if machine_name == 'aarch64':
            return os.path.join(BINARIES_DIR, 'vina_1.2.5_linux_aarch64')
        else:
            return os.path.join(BINARIES_DIR, 'vina_1.2.5_linux_x86_64')
    if system_name == 'Darwin':
        return os.path.join(BINARIES_DIR, 'vina_1.2.5_mac_x86_64')
    else:
        raise Exception(f"System '{system_name}' not yet supported")


def get_pdbqt_file_from_smiles(smiles: str, temp_dir: str = DOCKING_CACHE):
    ensure_path(temp_dir)
    filepath = os.path.join(temp_dir, '%s.pdbqt' % get_random_uuid_hex())
    command = [
        'obabel',
        '-:%s' % smiles,
        '-p', '7.4',
        '--gen3d',
        '-o', 'pdbqt',
        '-O', filepath,
    ]

    p = Popen(command, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate()
    if not ('1 molecule converted' in output.decode() or '1 molecule converted' in err.decode()):
        raise Exception("Invalid smiles")
    return filepath


def download_all_receptors():
    response = requests.get(RECEPTORS_INFO_API_URL)
    if response.status_code != 200:
        raise Exception(response.text)
    data = response.json()
    total = data['total']

    response = requests.get(RECEPTORS_API_URL, params={
        'offset': 0,
        'limit': total,
    })

    if response.status_code != 200:
        raise Exception(response.text)

    records = response.json()['records']

    for i in tqdm(range(len(records))):
        receptor_id = records[i]['receptor_id']
        download_file(records[i]['vina']['pdbqt_url'], get_pdbqt_filepath(receptor_id))
        download_file(records[i]['vina']['config_url'], get_config_filepath(receptor_id))

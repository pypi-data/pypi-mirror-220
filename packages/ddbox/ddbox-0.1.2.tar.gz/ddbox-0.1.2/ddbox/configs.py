import os

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

DOCKING_CACHE = '.cache/ddbox/docking/'
DATA_CACHE = '.cache/ddbox/data/'
BINARIES_DIR = os.path.join(BASE_DIR, 'bin')
VINA_RECEPTORS_CACHE = '.cache/ddbox/vina-receptors/'
BASE_API_URL = 'http://localhost:8000'

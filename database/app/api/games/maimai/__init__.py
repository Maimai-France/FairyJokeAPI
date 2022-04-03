import os
from pathlib import Path

from app import Router


router = Router(__name__)

#DATA_JACKETS = Path(os.environ.get('DDR_JACKETS', ''))
DATA_JACKETS = 'https://maimai.sega.jp/storage/jacket/'

from . import models, routes

import requests
import pandas as pd
from .utils import BearerAuth, load_yaml
import os 
from .config import check_config
from pathlib import Path


def setup() -> tuple:
    # Load credentials and server information from YAML file
    check_config()
    INFO_PATH = Path(os.environ['MINDER_DOWNLOADER_HOME']) / 'info.yaml'
    os.environ['MINDER_TOKEN'] = load_yaml(INFO_PATH)['token']
    server = load_yaml(INFO_PATH)['server'] + '/export'
    auth = BearerAuth(os.environ['MINDER_TOKEN'])
    return server,auth


def upload_file(file_2_upload):
    server,auth = setup()
    file = open(f"{file_2_upload}", "rb")
    binary_data = file.read()
    requests.put(f'https://research.minder.care/api/reports/{file_2_upload}',
                        data=binary_data,
                        headers={'content-type': 'text/html'},
                        auth=AUTH)
    r1 = requests.get('https://research.minder.care/api/reports', auth=auth)
    r1 = pd.Series(r1.json())
    return f'https://research.minder.care/{r1[r1.str.contains(file_2_upload)].values[0]}'
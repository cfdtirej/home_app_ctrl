import os
from pathlib import Path

import yaml
from dotenv import load_dotenv


load_dotenv()

API_HAKUSAN = os.environ['API_HAKUSAN']
API_MYHOME = os.environ['API_MYHOME']


yaml_file = Path(__file__).parent / 'config.yaml'
with open(yaml_file, 'r') as f:
    CONFIG = yaml.safe_load(f)

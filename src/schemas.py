from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict, Optional

import yaml


yaml_path = Path(__file__).parent / 'config.yaml'
with open(yaml_path, 'r') as f:
    config_yaml = yaml.safe_load(f)


@dataclass
class DBConfig:
    host: str = config_yaml['InfluxDB']['host']
    port: int = config_yaml['InfluxDB']['port']
    username: str = config_yaml['InfluxDB']['username']
    password: int = config_yaml['InfluxDB']['password']
    database: int = config_yaml['InfluxDB']['database']

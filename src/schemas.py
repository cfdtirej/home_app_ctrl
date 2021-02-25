from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict, Match, Optional

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

@dataclass
class TVState:
    nickname: str
    type: str
    input: str
    created_at: str
    firmware_version: str
    humidity_offset: str
    id: str
    mac_address: str
    name: str
    serial_number: str
    temperature_offset: int
    updated_at: str


@dataclass
class AirconState:
    nickname: str
    type: str
    button: str
    dir: str
    mode: str
    temp: str
    vol: str
    created_at: str
    firmware_version: str
    humidity_offset: int
    id: str
    mac_address: str
    name: str
    serial_number: str
    temperature_offset: int
    updated_at: str


@dataclass
class LightState:
    type: str
    brightness: str
    last_button: str
    power: str
    created_at: str
    firmware_version: str
    humidity_offset: int
    id: str
    mac_address: str
    name: str
    serial_number: str
    temperature_offset: int
    updated_at: str

@dataclass
class RoomState:
    time: str
    name: str
    te: float
    il: float
    hu: float
    tm: float
    di: float 
    mac_address: str
    id: str
    update_at: str

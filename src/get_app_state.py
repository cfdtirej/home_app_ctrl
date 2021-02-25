import csv
import os
import datetime
import json
import time
from dataclasses import dataclass, asdict
from typing import List, Optional, Any, Dict
from pathlib import Path

import pytz
from remo import NatureRemoAPI
from influxdb import InfluxDBClient

import API_KEY
import calc_di_tm
import schemas


api = NatureRemoAPI(API_KEY.API_HAKUSAN)
# List[schemas.AirconState, schemas.AirconState, schemas.LightState, schemas.TVState]
def get_applience_state() -> List[Dict[str, str]]:
    result = []
    for appliance in api.get_appliances():
        data = json.loads(appliance.as_json_string())
        if appliance.aircon:
            aircon = {
                'nickname': appliance.nickname,
                'type': appliance.type,
                **json.loads(appliance.settings.as_json_string()),
                **json.loads(appliance.device.as_json_string())
            }
            
            result.append(aircon)
        elif appliance.light:
            light = {
                'nickname': appliance.nickname,
                'type': appliance.type,
                **json.loads(appliance.light.state.as_json_string()),
                **json.loads(appliance.device.as_json_string())
            }
            result.append(light)
        elif appliance.tv:
            tv = {
                'nickname': appliance.nickname,
                'type': appliance.type,
                **json.loads(appliance.tv.state.as_json_string()),
                **json.loads(appliance.device.as_json_string())
            }
            result.append(tv)

    return result
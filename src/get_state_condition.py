import csv
import os
import datetime
import json
import time
from dataclasses import dataclass
from typing import List, Optional, Any, Dict
from pathlib import Path

from remo import NatureRemoAPI
from influxdb import InfluxDBClient

import API_KEY
import calc_di_tm
import pytz


api = NatureRemoAPI(API_KEY.API_HAKUSAN)


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

    return result

def get_hu_il_te() -> List[List[Any]]:
    result = []
    for device in api.get_devices():
        result.append({
            'timenow': datetime.datetime.now(tz=pytz.timezone('Asia/Tokyo')).isoformat(),
            'name': device.name,
            'te': device.newest_events['te'].val,
            'il': device.newest_events['il'].val,
            'hu': device.newest_events['hu'].val,
            'tm': calc_di_tm.calc_tm(device.newest_events['te'].val, device.newest_events['hu'].val),
            'di': calc_di_tm.calc_di(device.newest_events['te'].val, device.newest_events['hu'].val),
            'mac_address': device.mac_address,
            'id': device.id,
            'update_at': device.updated_at.astimezone(pytz.timezone('Asia/Tokyo')).isoformat(),
        })
    return result

def hu_il_te_wirte():
    
    room_conditions = get_hu_il_te()
    dt = datetime.datetime.now(tz=pytz.timezone('Asia/Tokyo')).date()
    csvfile = Path(__file__).parent / 'room_condition' / f'{dt}.csv'
    if not csvfile.parent.exists():
        csvfile.parent.mkdir()
    if not csvfile.exists():
        csvfile.touch()
        with open(csvfile, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(room_conditions[0].keys())
    for condition in room_conditions:
        with open(csvfile, 'a') as f:
            writer = csv.writer(f)
            writer.writerow(condition.values())
    return room_conditions


# print('プログラム実行中>>>>>')
# while True:
#     hu_il_te_wirte()
#     time.sleep(10)

print(get_applience_state())

# app_state = get_applience_state()
# print(app_state)
# print(get_hu_il_te())
# print(datetime.datetime.now(tz=pytz.timezone('Asia/Tokyo')).date())
# from datetime import datetime
# import datetime
# d = datetime.datetime(2021, 2, 5, 4, 50, 46, tzinfo=datetime.timezone.utc)
# print(d.astimezone(datetime.timezone(datetime.timedelta(hours=9))))
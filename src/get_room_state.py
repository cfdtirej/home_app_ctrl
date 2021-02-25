import csv
import os
import datetime
import json
import time
from dataclasses import dataclass, asdict, field
from typing import List, Any, Dict
from pathlib import Path

import pytz
from remo import NatureRemoAPI
from influxdb import InfluxDBClient, client, line_protocol

import API_KEY
import calc_di_tm
import utils
import schemas

api = NatureRemoAPI(API_KEY.API_HAKUSAN)
influxconfig =asdict(schemas.DBConfig()) 
jst = pytz.timezone('Asia/Tokyo')


def get_hu_il_te() -> List[List[Any]]:
    result = []
    for device in api.get_devices():
        result.append({
            'time': datetime.datetime.now(tz=pytz.timezone('Asia/Tokyo')).isoformat(),
            'name': device.name,
            'te': device.newest_events['te'].val,
            'il': device.newest_events['il'].val,
            'hu': device.newest_events['hu'].val,
            'tm': calc_di_tm.calc_tm(device.newest_events['te'].val, device.newest_events['hu'].val),
            'di': calc_di_tm.calc_di(device.newest_events['te'].val, device.newest_events['hu'].val)
        })
    return result

def hu_il_te_csv_wirte(room_condition: Dict[str, Any]) -> None:
    dt = datetime.datetime.now(tz=pytz.timezone('Asia/Tokyo')).date()
    csvfile = Path(__file__).parents[1] / 'logcsv' / 'room' / f'{dt}.csv'
    if not csvfile.parent.exists():
        csvfile.parent.mkdir(parents=True)
    if not csvfile.exists():
        csvfile.touch()
        with open(csvfile, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(room_condition[0].keys())
    for condition in room_condition:
        with open(csvfile, 'a') as f:
            writer = csv.writer(f)
            writer.writerow(room_condition.values())
    return 

def main():
    room_state = get_hu_il_te()
    dt = datetime.datetime.now(jst)
    for state in room_state:
        # values = utils.list_val_type_conv(state.values())
        values = state.values()
        keys = state.keys()
        # 室内環境データ用のcsvファイルの確認と作成
        csvfile = Path(__file__).parents[1] / 'logcsv' / 'room' / f'{dt.date()}.csv'
        if not csvfile.parent.is_dir():
            csvfile.parent.mkdir(parents=True)
        if not csvfile.exists():
            csvfile.touch()
            with open(csvfile, 'w') as f:
                writer = csv.writer(f)
                writer.writerow(keys)
        with open(csvfile, 'a') as f:
            writer = csv.writer(f)
            # writer.writerow(values)
        # InfluxDBにInsert
        client = InfluxDBClient(**influxconfig)
        line_protocol = {
            'measurements': 'room_state',
            'time': state.pop('time'),
            'tags': {
                'name': state.pop('name'),
            },
            'fields': {
                'te': state['te'],
                'il': state['il'],
                'hu': state['hu'],
                'tm': state['tm'],
                'di': state['di']
            }
        }
        # print(line_protocol)
        
        print(state)
        # client.write_points(line_protocol)
main()




# print('プログラム実行中>>>>>')
# while True:
#     hu_il_te_wirte()
#     time.sleep(10)
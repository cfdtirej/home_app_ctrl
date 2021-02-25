import csv
from datetime import datetime
from pathlib import Path
from typing import Any, List, Union

import pytz
import numpy as np

import schemas


# listの値の型変換
def list_val_type_conv(data: List[Any]) -> List[Any]:
    numbers = {str(i) for i in range(10)}
    result = []
    for value in data:
        if (type(value) is float) or (type(value) is int):
            result.append(value)
            continue
        str_set = set()
        for string in value:
            str_set.add(str(string))
        try:
            result.append(float(value))
        except ValueError:
            if value in ['True', 'False', 'true', 'false']:
                result.append(bool(value))
            elif str_set - numbers:
                try:
                    if '-' in value:
                        ts = datetime.strptime(value + '+0900', '%Y-%m-%d %H:%M:%S.%f%z').isoformat()
                        result.append(ts)
                    elif '/' in value:
                        ts = datetime.strptime(value + '+0900', '%Y/%m/%d %H:%M:%S.%f%z').isoformat()
                        result.append(ts)
                except ValueError:
                    result.append(value)
            elif value == '':
                result.append(np.nan)
            else:
                pass
    return result



class DataCollectionPath:
    
    def __init__(self) -> None:
        
        self.room_state_dir =  Path(__file__).parents[1] / 'logcsv' / 'room'
        self.home_app_state_dir =  Path(__file__).parents[1] / 'logcsv' / 'homeApp'
        if not self.room_state_dir.exists():
            self.room_state_dir.mkdir(parents=True)
        if not self.home_app_state_dir.exists():
            self.home_app_state_dir.mkdir(parents=True)
    
    def room_state_csv(self, data: schemas.RoomState, cattagory: str):
        """部屋の状態をCSVに記録する
        """
        jtc = pytz.timezone('Asia/Tokyo')
        dt_now = datetime.now(jtc)
        # home_app_ctrl/logcsv/room/{year}/{date}.csvの確認と作成
        if not self.room_state_dir.joinpath(f'{dt_now.year}').exists():
            self.room_state_dir.joinpath(f'{dt_now.year}').mkdir(parents=True)
        if not self.room_state_dir.joinpath(f'{dt_now.year}/{dt_now.date()}.csv').exists():
            self.room_state_dir.joinpath(f'{dt_now.year}/{dt_now.date()}.csv').touch()
            csvfile = self.room_state_dir.joinpath(f'{dt_now.year}/{dt_now.date()}.csv')
            with open(csvfile, 'w') as f:
                writer = csv.writer(f)
                writer.writerow(data.keys())

    def home_app_state_csv(self):
        """家電の状態を記録する
        """
        jtc = pytz.timezone('Asia/Tokyo')
        dt_now = datetime.now(jtc)
        # home_app_ctrl/logcsv/homeApp/{year}/{date}.csvの確認と作成
        if not self.home_app_state_dir.joinpath(f'{dt_now.year}').exists():
            self.home_app_state_dir.joinpath(f'{dt_now.year}').mkdir(parents=True)
        if not self.home_app_state_dir.joinpath(f'{dt_now.year}/{dt_now.date()}.csv').exists():
            self.home_app_state_dir.joinpath(f'{dt_now.year}/{dt_now.date()}.csv').touch()
            csvfile = self.home_app_state_dir.joinpath(f'{dt_now.year}/{dt_now.date()}.csv')
            ['brightness','created_at','firmware_version','humidity_offset','id','last_button','mac_address','name','nickname','power','serial_number','temperature_offset','type','updated_at']

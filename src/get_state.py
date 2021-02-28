import csv
import os
import datetime
import json
import time
from dataclasses import dataclass, asdict
from typing import List, Optional, Any, Dict, NoReturn, Literal
from pathlib import Path

import pytz
from remo import NatureRemoAPI
from influxdb import InfluxDBClient

import calc_di_tm
import settings


api = NatureRemoAPI(settings.API_HAKUSAN)
jst = pytz.timezone('Asia/Tokyo')

# def appliance_csv_writer():

# class NatureRemoGet(NatureRemoAPI)
def get_applience_state() -> List[Dict[str, Any]]:
    result = []
    for appliance in api.get_appliances():
        if appliance.aircon:
            aircon_setting = json.loads(appliance.settings.as_json_string())
            aircon = {
                'updated_at':  appliance.device.updated_at.astimezone(jst).isoformat(),
                'name': appliance.device.name,
                'mac_address': appliance.device.mac_address,
                **aircon_setting
            }
            result.append(aircon)

        elif appliance.light:
            light_state = json.loads(appliance.light.state.as_json_string()) 
            light = {
                'update_at': appliance.device.updated_at.astimezone(jst).isoformat(),
                'name': appliance.device.name,
                'mac_address': appliance.device.mac_address,
                **light_state
            }
            result.append(light)
        elif appliance.tv:
            tv_state = json.loads(appliance.tv.state.as_json_string())
            tv = {
                'update_at': appliance.device.updated_at.astimezone(jst).isoformat(),
                'name': appliance.device.name,
                'mac_address': appliance.device.mac_address,
                **tv_state
            }
            result.append(tv)
    return result

class GetHakusanNatureRemo(NatureRemoAPI):
    def get_appliances_state(self) -> List[Dict[str, Any]]:
        result = []
        for appliance in self.get_appliances():
            if appliance.aircon:
                aircon_setting = json.loads(appliance.settings.as_json_string())
                aircon = {
                    'updated_at':  appliance.device.updated_at.astimezone(jst).isoformat(),
                    'name': appliance.device.name,
                    'mac_address': appliance.device.mac_address,
                    'type': appliance.type,
                    'id': appliance.id,
                    **aircon_setting
                }
                result.append(aircon)
            elif appliance.light:
                light_state = json.loads(appliance.light.state.as_json_string()) 
                light = {
                    'updated_at': appliance.device.updated_at.astimezone(jst).isoformat(),
                    'name': appliance.device.name,
                    'mac_address': appliance.device.mac_address,
                    'type': appliance.type,
                    'id': appliance.id,
                    **light_state
                }
                result.append(light)
            elif appliance.tv:
                tv_state = json.loads(appliance.tv.state.as_json_string())
                tv = {
                    'updated_at': appliance.device.updated_at.astimezone(jst).isoformat(),
                    'name': appliance.device.name,
                    'mac_address': appliance.device.mac_address,
                    'type': appliance.type,
                    'id': appliance.id,
                    **tv_state
                }
                result.append(tv)
        return result
    
    def appliance_settings_csv_writer(self, state: Dict[str, Any]) -> NoReturn:
        dt = datetime.datetime.now(jst)
        app_type = state['type']
        csvfile = Path(__file__).parent / 'logcsv' / 'home_app' / f'{app_type}' / f'{dt.date()}.csv'
        if not csvfile.parent.is_dir():
            csvfile.parent.mkdir(parents=True)
        if not csvfile.exists():
            csvfile.touch()
            with open(csvfile, 'w') as f:
                writer = csv.writer(f)
                writer.writerow(state.keys())
        with open(csvfile, 'a') as f:
            writer = csv.writer(f)
            writer.writerow(state.values())
            
    
    def get_hu_il_te(self) -> List[Dict[str, Any]]:
        """Nature Remo API から室内環境情報を取得
        Returns:
            time: datetime
                時刻
            name: str
                NatureRemoの名前
            mac_address: str 
                NatureRemoのmac address
            te: float | int 
                温度
            il: float | int
                照度
            hu: float | int
                湿度
            tm: float | int
                体感温度
            di: float | int
                不快指数
            di_lebel: float | int
                不快指数から温度の増減値
        """
        result = []
        for device in self.get_devices():
            result.append({
                'time': datetime.datetime.now(tz=pytz.timezone('Asia/Tokyo')).isoformat(),
                'name': device.name,
                'mac_address': device.mac_address,
                'te': device.newest_events['te'].val,
                'il': device.newest_events['il'].val,
                'hu': device.newest_events['hu'].val,
                'tm': calc_di_tm.calc_tm(device.newest_events['te'].val, device.newest_events['hu'].val),
                'di': calc_di_tm.calc_di(device.newest_events['te'].val, device.newest_events['hu'].val),
                'di_lebel': calc_di_tm.di_lebel(calc_di_tm.calc_di(device.newest_events['te'].val, device.newest_events['hu'].val))
            })
        return result

    def room_state_csv_writer(self, room_state: List[Dict[str, Any]]) -> NoReturn:
        """室内環境データのCSV記録
        Args:
            room_state: self.get_hu_il_te() Returns
        """
        dt = datetime.datetime.now(jst)
        for state in room_state:
            # 室内環境データ用のcsvファイルの確認と作成
            csvfile = Path(__file__).parent / 'logcsv' / 'room' / f'{dt.date()}.csv'
            if not csvfile.parent.is_dir():
                csvfile.parent.mkdir(parents=True)
            if not csvfile.exists():
                csvfile.touch()
                with open(csvfile, 'w') as f:
                    writer = csv.writer(f)
                    writer.writerow(state.keys())
            with open(csvfile, 'a') as f:
                writer = csv.writer(f)
                writer.writerow(state.values())


if __name__ == '__main__':
    api = GetHakusanNatureRemo(settings.API_HAKUSAN)
    ap = api.get_appliances_state()
    api.appliance_settings_csv_writer(ap)
    print(api.get_hu_il_te())
    api.record_room_state()
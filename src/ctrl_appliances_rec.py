import os
import csv
import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Any

import pytz
from remo import NatureRemoAPI

import calc_di_tm
import settings


jst = pytz.timezone('Asia/Tokyo')


class HakusanAppliancesCtrl(NatureRemoAPI):
    def get_appliances_state(self) -> List[Dict[str, Any]]:
        result = []
        for appliance in self.get_appliances():
            if appliance.aircon:
                aircon_setting = json.loads(appliance.settings.as_json_string())
                aircon = {
                    'updated_at':  appliance.device.updated_at.astimezone(jst).isoformat(),
                    'name': appliance.device.name,
                    'type': appliance.type,
                    'id': appliance.id,
                    'nickname': appliance.nickname,
                    **aircon_setting
                }
                result.append(aircon)
            elif appliance.light:
                light_state = json.loads(appliance.light.state.as_json_string()) 
                light = {
                    'updated_at': appliance.device.updated_at.astimezone(jst).isoformat(),
                    'name': appliance.device.name,
                    'type': appliance.type,
                    'id': appliance.id,
                    'nickname': appliance.nickname,
                    **light_state
                }
                result.append(light)
            elif appliance.tv:
                tv_state = json.loads(appliance.tv.state.as_json_string())
                tv = {
                    'updated_at': appliance.device.updated_at.astimezone(jst).isoformat(),
                    'name': appliance.device.name,
                    'type': appliance.type,
                    'id': appliance.id,
                    'nickname': appliance.nickname,
                    **tv_state
                }
                result.append(tv)
        return result
    
    def get_aircon_settings(self, appliance: str) -> Dict[str, Any]:
        """
        Args:
            appliance: aircon id
        Returns:
            Aircon settings
        """
        for app in self.get_appliances():
            if app.id == appliance:
                aircon_settings = {
                    'update_at': app.device.updated_at.astimezone(jst),
                    'id': app.id,
                    'nickname': app.nickname,
                    'type': app.type,
                    'button': app.settings.button,
                    'dir': app.settings.dir,
                    'mode': app.settings.mode,
                    'vol': app.settings.vol,
                    'temp': app.settings.temp
                }
                return aircon_settings

    def update_aircon_settings_rec(
        self, appliance: str, operation_mode: str=None, temperature: str=None, air_volume: str=None, air_direction: str=None, button: str=None
    ) -> None:
        """param appliance: str
        Update air conditioner settings.
        Args:
            appliance: Appliance ID.
            operation_mode: AC operation mode.
            temperature: Temperature.
            air_volume: AC air volume.
            air_direction: AC air direction.
            button: Button.
        """
        self.update_aircon_settings()
        self.update_aircon_settings(appliance, operation_mode, temperature, air_volume, air_direction, button)
        aircon_settings = self.get_aircon_settings(appliance)
        dt = datetime.now(tz=jst).date()
        nickname = aircon_settings['nickname']
        csvfile = Path(__file__).parent / 'appliances' / f'{nickname}' / f'{dt}.csv'
        if not csvfile.is_dir():
            csvfile.mkdir(parents=True)
        if not csvfile.exists():
            csvfile.touch()
            with open(csvfile, 'w') as f:
                writer = csv.writer(f)
                writer.writerow(aircon_settings.keys)
        with open(csvfile, 'a') as f:
            writer = csv.writer(f)
            writer.writerow(aircon_settings.values())

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
                'time': datetime.datetime.now(tz=jst).isoformat(),
                'name': device.name,
                'te': device.newest_events['te'].val,
                'il': device.newest_events['il'].val,
                'hu': device.newest_events['hu'].val,
                'tm': calc_di_tm.calc_tm(device.newest_events['te'].val, device.newest_events['hu'].val),
                'di': calc_di_tm.calc_di(device.newest_events['te'].val, device.newest_events['hu'].val),
                'di_lebel': calc_di_tm.di_lebel(calc_di_tm.calc_di(device.newest_events['te'].val, device.newest_events['hu'].val))
            })
        return result
    
    def room_state_csv_writer(self, room_state: List[Dict[str, Any]]) -> None:
        """室内環境データのCSV記録
        Args:
            room_state: self.get_hu_il_te() Returns
        """
        dt = datetime.datetime.now(jst)
        for state in room_state:
            # 室内環境データ用のcsvファイルの確認と作成
            csvfile = Path(__file__).parent / 'room_state' / f'{state["name"]}' / f'{dt.date()}.csv'
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

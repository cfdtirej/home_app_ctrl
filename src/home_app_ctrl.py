import csv
import json
from datetime import datetime
from pathlib import Path
from pprint import pprint
from typing import List, Dict, Optional, Any, Literal, NoReturn
from dataclasses import dataclass, asdict

import pytz
from remo import NatureRemoAPI
import remo

import calc_di_tm
import settings
from get_state import GetHakusanNatureRemo

# api = NatureRemoAPI(API_KEY.API_HAKUSAN)
# api = NatureRemoAPI(API_KEY.API_MYHOME)


# devices = api.get_devices()
# appliances = api.get_appliances()
# for dev in api.get_devices():
#     print(dev.newest_events)
#     print()

# with open('./devices.json', 'w') as f:
#     json.dump(appliances_dict, f, indent=4)

# エアコンの設定温度変える
# api.update_aircon_settings(
#     appliance=appliances[0].id,
#     operation_mode='warm',
#     temperature='23',
# )

# api.update_aircon_settings(
#     appliances[0].id, operation_mode='hot', temperature=26)
# print(appliances[0].type)
# api.update_aircon_settings(appliance=)

# print(appliances[0].aircon)
# print(devices)


class HakusanHomeAppCtrl(GetHakusanNatureRemo):
    def homeapp_auto_ctrl(self):
        room_state = self.get_hu_il_te()
        app_state = self.get_appliances_state()
        for app in app_state:
            for room in room_state:
                if (app['name'] == room['name']) and (app['type'] == 'AC'):
                    'h04 102 living'
                    
    def homeapp_auto_ctrl_ac_winter(self, floor: Literal[1, 2]) -> NoReturn:
        """エアコンを調整
        """
        if floor == 1:
            name = settings.CONFIG['NatureRemoName']['1F']
        elif floor == 2:
            name = settings.CONFIG['NatureRemoName']['2F']
        else:
            raise 'Args is not 1 or 2'
        room_state = self.get_hu_il_te()
        app_state = self.get_appliances_state()
        for app in app_state:
            for room in room_state:
                if (app['name'] and room['name'] == name) and (app['type'] == 'AC'):
                    if room['di_lebel'] != 0:
                        self.update_aircon_settings(
                            appliance=app['id'],
                            operation_mode='warm',
                            temperature=int(app['temp'])+room['di_lebel'])
                        self.appliance_settings_csv_writer(self.get_appliances_state())

    def homeapp_auto_ctrl_2f_ac_winter(self, ):
        """2Fのエアコンを調整
        """
        room_state = self.get_hu_il_te()
        app_state = self.get_appliances_state()
        for app in app_state:
            for room in room_state:
                if (app['name'] and room['name'] == 'h06 102 2f') and (app['type'] == 'AC'):
                    if room['di_lebel'] != 0:
                        self.update_aircon_settings(
                            appliance=app['id'],
                            operation_mode='warm',
                            temperature=int(app['temp'])+room['di_lebel'])
                        self.appliance_settings_csv_writer(self.get_appliances_state())


class MyHomeAppCtrl(NatureRemoAPI):
    
    def get_devices_dict(self) -> List[Dict]:
        devices_dict = [
            json.loads(device.as_json_string()) for device in self.get_devices()
        ]
        return devices_dict

    def get_appliances_dict(self) -> List[Dict]:
        appliances_dict = [
            json.loads(app.as_json_string()) for app in self.get_appliances()
        ]
        return appliances_dict

    def stop_aircon(self, aircon_id: int = 1) -> None:
        self.update_aircon_settings(
            appliance=self.get_appliances[aircon_id].id, button='power-off')


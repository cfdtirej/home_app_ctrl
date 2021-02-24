import csv
import json
from datetime import datetime
from pathlib import Path
from pprint import pprint
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict

from remo import NatureRemoAPI
import remo

import API_KEY
import schemas


# api = NatureRemoAPI(API_KEY.API_HAKUSAN)
api = NatureRemoAPI(API_KEY.API_MYHOME)

devices = api.get_devices()
appliances = api.get_appliances()
for dev in api.get_devices():
    print(dev.newest_events)
    print()

# with open('./devices.json', 'w') as f:
#     json.dump(appliances_dict, f, indent=4)

# エアコンの設定温度変える
api.update_aircon_settings(
    appliance=appliances[0].id,
    operation_mode='warm',
    temperature='23',
)

# api.update_aircon_settings(
#     appliances[0].id, operation_mode='hot', temperature=26)
# print(appliances[0].type)
# api.update_aircon_settings(appliance=)

# print(appliances[0].aircon)
# print(devices)


class MyHomeAppCtrl(NatureRemoAPI):

    def get_appliances_state(self) -> List[Dict[str, str]]:
        result = []
        for appliance in self.get_appliances():
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
    def get_hu_il_te(self) -> List[List[Any]]:
        result = []
        dtnow = datetime.datetime.now(tz=pytz.timezone('Asia/Tokyo')).isoformat()
        for device in self.get_devices():
            result.append({
                'timenow': dtnow,
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
    
    def write_csv(self):


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



    
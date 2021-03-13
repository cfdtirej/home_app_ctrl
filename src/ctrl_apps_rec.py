import os
import csv
import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Any

import pytz
from remo import NatureRemoAPI

import settings

jst = pytz.timezone('Asia/Tokyo')

class HakusanAppliancesCtrl(NatureRemoAPI):
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
        self, appliance: str, operation_mode: str=None, temperature: str=None, air_volume: str=None, air_direction: str=None, button: str=None):
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

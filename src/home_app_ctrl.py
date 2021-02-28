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


class HakusanHomeAppCtrl(GetHakusanNatureRemo):
    def homeapp_auto_ctrl(self):
        room_state = self.get_hu_il_te()
        app_state = self.get_appliances_state()
        for app in app_state:
            for room in room_state:
                if (app['name'] == room['name']) and (app['type'] == 'AC'):
                    'h04 102 living'
                    
    def homeapp_auto_ctrl_ac_winter(self, floor: Literal[1, 2]) -> NoReturn:
        """エアコンの設定を修正
        設定を変更したらCSVに記録する
        """
        if floor == 1:
            idx = 0
            aircon_id = settings.CONFIG['NatureRemoName']['Aircon1F']['id']
            app_state = self.get_appliances_state()[0]
            room_state = self.get_hu_il_te()[0]
        elif floor == 2:
            idx = 1
            aircon_id = settings.CONFIG['NatureRemoName']['Aircon2F']['id']
            room_state = self.get_hu_il_te()[1]
            app_state = self.get_appliances_state()[1]
        else:
            raise 'Args is not 1 or 2'
        
        # エアコンの設定温度見直し
        if room_state['di_lebel'] != 0:
            te = int(app_state['temp'])+room_state['di_lebel']
            if te > 30:
                # te = int(app_state['temp'])
                # self.update_aircon_settings(
                #     appliance=aircon_id, operation_mode='warm', temperature=te, air_volume='3',button='')
                pass
            elif te < 18:
                # te = int(app_state['temp'])
                # self.update_aircon_settings(
                #     appliance=aircon_id, operation_mode='warm', temperature=te, air_volume='3',button='')
                pass
            else:
                self.update_aircon_settings(
                    appliance=aircon_id, operation_mode='warm', temperature=te, air_volume='4',button='')
                # 設定変更の記録
                self.appliance_settings_csv_writer(self.get_appliances_state()[idx])
        # for app in app_state:
        #     for room in room_state:
        #         if (app['name'] and room['name'] == name) and (app['type'] == 'AC'):
        #             if room['di_lebel'] != 0:
        #                 self.update_aircon_settings(
        #                     appliance=app['id'],
        #                     operation_mode='warm',
        #                     temperature=int(app['temp'])+room['di_lebel'])
        #                 self.appliance_settings_csv_writer(self.get_appliances_state())

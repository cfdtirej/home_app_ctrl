import time
from datetime import datetime

import pytz
from influxdb import InfluxDBClient

import settings
from home_app_ctrl import HakusanHomeAppCtrl

jst = pytz.timezone('Asia/Tokyo')

api = HakusanHomeAppCtrl(settings.API_HAKUSAN)
aircon_1F_id = settings.CONFIG['NatureRemoName']['Aircon1F']['id']
tv_id = settings.CONFIG['NatureRemoName']['TV']['id']
light_id = settings.CONFIG['NatureRemoName']['SubRoomLight']['id']



# はじめにエアコンつける
# api.update_aircon_settings(
#     appliance=aircon_1F_id, operation_mode='warm', temperature='24', air_volume='4', button='')
# first_app_state = api.get_appliances_state()
# api.appliance_settings_csv_writer(first_app_state[0])      

day_now = datetime.now(jst).day
while True:
    dt_now = datetime.now(jst)
    if dt_now.minute == 0:
        api.homeapp_auto_ctrl_ac_winter(1)
        time.sleep(60*10)
    if day_now != dt_now.day:
        break
# api.homeapp_auto_ctrl_ac_winter(1)

# １Fエアコンの自動設定
# api.homeapp_auto_ctrl_ac_winter(1)

# latest_app_state = api.get_appliances_state()

# client = InfluxDBClient(**settings.CONFIG['InfluxDB'])
# client.close()

import time
from datetime import datetime

import pytz
from influxdb import InfluxDBClient

import settings
from home_app_ctrl import HakusanHomeAppCtrl

jst = pytz.timezone('Asia/Tokyo')

api = HakusanHomeAppCtrl(settings.API_HAKUSAN)
aircon_1F_id = settings.CONFIG['NatureRemoName']['Aircon1F']['id']
# aircon_2F_id = settings.CONFIG['NatureRemoName']['Aircon2F']['id']
tv_id = settings.CONFIG['NatureRemoName']['TV']['id']
light_id = settings.CONFIG['NatureRemoName']['SubRoomLight']['id']


print(api.get_appliances_state()[0])
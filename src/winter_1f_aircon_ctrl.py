import time
from datetime import datetime

from influxdb import InfluxDBClient

import settings
from home_app_ctrl import HakusanHomeAppCtrl


api = HakusanHomeAppCtrl(settings.API_HAKUSAN)
living_name = settings.CONFIG['NatureRemoName']['1F']


# はじめにエアコンつける
# api.update_aircon_settings(
#     appliance=, operation_mode='warm', temperature='23.2', air_volume='2', air_direction='2')

# エアコンのID取得
for appliance in api.get_appliances_state():
    if (appliance['name'] == living_name) and (appliance['type'] == 'AC'):
        nr_id = appliance['id']


prev_app_state = api.get_appliances_state()

# api.homeapp_auto_ctrl_ac_winter(1)

latest_app_state = api.get_appliances_state()

client = InfluxDBClient(**settings.CONFIG['InfluxDB'])
client.close()


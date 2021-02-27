import time
from datetime import datetime

from influxdb import InfluxDBClient

import settings
from get_state import GetHakusanNatureRemo

# Connect Hakusan Nature Remo API
api = GetHakusanNatureRemo(settings.API_HAKUSAN)
# Connect InfluxDB
client = InfluxDBClient(**settings.CONFIG['InfluxDB'])


while True:
    room_state = api.get_hu_il_te()
    api.room_state_csv_writer(room_state)
    for state in room_state:
       
        line_protocol = [{
            'measurement': 'room_state',
            'time': state['time'],
            'tags': {
                'name': state['name'],
                'mac_address': state['mac_address'],
                'di_lebel': state['di_lebel']
            },
            'fields': {
                'te': state['te'],
                'il': state['il'],
                'hu': state['hu'],
                'tm': state['tm'],
                'di': state['di'],
            }
        }]
        try:
            client.write_points(line_protocol)
        except:
            pass
    time.sleep(60)

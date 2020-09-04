import logging
from bluepy.btle import DefaultDelegate, Peripheral, Scanner
import requests
import json

from scanner import ScanDelegate
from parser import BLEParser

try:
    s = ScanDelegate()
    scanner = Scanner().withDelegate(s)
    value = {}
    headers = {'Content-type': 'application/json'}
    logging.basicConfig(filename='data.log', level=logging.INFO)

    mapping_value = {
        'oximiter':
        {
            'char': '2A5F',
            'serv': '1822'
        },
        'bloodpressure':
        {
            'char': '2A35',
            'serv': '1810'
        },
        'glucose': {
            'char': '2A18',
            'serv': '1808'
        }
    }

    mapping_name = {
            'nonin3230': 'oximiter',
            'blesmart': 'bloodpressure',
            'mi band 2': 'heart_rate'
            }

    while True:
        devices = scanner.scan(5.0)
        if s.knowdevice:
            connector = Peripheral(s.UUID, "public")
            _type = mapping_name[s.name]
            value = BLEParser(connector, _type=_type, servUUID=mapping_value[_type]['serv'],
                              charactUUID=mapping_value[_type]['char']).notify()
            requests.post('http://localhost:5000/devices/scan',
                          data=json.dumps(value), headers=headers)
            connector.disconnect()
except Exception as e:
    print(str(e))

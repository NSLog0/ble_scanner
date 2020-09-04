import logging
import binascii
import time
import sys
import time

from bluepy.btle import DefaultDelegate, Peripheral, Scanner
from sfloat import to_int

try:
    import queue
except ImportError:
    import Queue as queue


class BLEParser():
    __device = None
    __serv = None
    __charact = None
    __buffer_holder = queue.Queue()

    class NotificationDelegate(DefaultDelegate):
        def __init__(self, buffer_holder):
            DefaultDelegate.__init__(self)
            self.buffer_holder = buffer_holder

        def handleNotification(self, cHandle, data):
            decoded = binascii.b2a_hex(data).decode('utf-8')
            self.buffer_holder.put(decoded)

    def __init__(self, device, _type, connect_type="public", servUUID="1822", charactUUID="2a5f", sending_pkg=b"\x01\x00"):
        self.__device = device
        self.__device.setDelegate(
            BLEParser.NotificationDelegate(self.__buffer_holder))
        self.connect_type = connect_type
        self.servUUID = servUUID
        self.charactUUID = charactUUID
        self.sending_pkg = sending_pkg
        self._type = _type

    def set_up(self):
        self.get_service()
        self.get_characteristics()
        self.sending()

    def get_service(self):
        self.__serv = self.__device.getServiceByUUID(self.servUUID)

    def get_characteristics(self):
        self.__charact = self.__serv.getCharacteristics(self.charactUUID)[0]

    def sending(self):
        self.__device.writeCharacteristic(
            self.__charact.getHandle() + 1, self.sending_pkg, withResponse=True)

    def notify(self):
        self.set_up()
        counter = 0
        while counter <= 5:
            if self.__device.waitForNotifications(1.0):
                counter += 1

                continue

        self.__device.disconnect()
        return self.parser()

    def parser(self):
        data = self.__buffer_holder.get_nowait()
        return self.template(data)

    def template(self, data):
        result = ''
        if self._type is 'oximiter':
            oxi = int(to_int(int(data[4:6] + data[2:4], 16)))
            h_rate = int(to_int(int(data[8:10] + data[6:8], 16)))
            result = {'device': 'oximiter', 'value': {
                'heart_rate': int(h_rate), 'spo2': int(oxi)}}

        if self._type is 'glucose':
            lv = int(to_int(int(data[4:6] + data[2:4], 16)))
            result = {'device': 'glucose', 'value': int(lv)}

        if self._type is 'bloodpressure':
            normal = int(to_int(int(data[4:6] + data[2:4], 16)))
            result = {'device': 'bloodPressure', 'value': {
                normal: int(normal), low: int(normal)}}

        return result

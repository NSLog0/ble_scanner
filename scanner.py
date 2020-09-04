import sys
import time
import binascii
import logging
from bluepy.btle import DefaultDelegate, Peripheral, Scanner


class ScanDelegate(DefaultDelegate):

    UUID = ''
    knowdevice = False
    name = ''

    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        for (adtype, desc, value) in dev.getScanData():
            self.knowdevice = False
            self.name = ''
            if ("nonin3230" in value.lower()):
                self.name = 'nonin3230'
                self.knowdevice = True

            if self.knowdevice == True:
                self.UUID = dev.addr

                break

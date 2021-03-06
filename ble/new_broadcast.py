#!/usr/bin/env python

import dbus.exceptions
import dbus.service
import sys
import dbus, dbus.mainloop.glib
from gi.repository import GObject
from example_advertisement import Advertisement
from example_advertisement import register_ad_cb, register_ad_error_cb
from example_gatt_server import Service, Characteristic
from example_gatt_server import register_app_cb, register_app_error_cb

import json
import sqlite3
import array
import time

import mysql.connector

try:
  from gi.repository import GObject
except ImportError:
  import gobject as GObject
import sys

from random import randint
connection = sqlite3.connect("sensor_data.sql")
cursor = connection.cursor()

BLUEZ_SERVICE_NAME = 'org.bluez'
GATT_MANAGER_IFACE = 'org.bluez.GattManager1'
DBUS_OM_IFACE =      'org.freedesktop.DBus.ObjectManager'
DBUS_PROP_IFACE =    'org.freedesktop.DBus.Properties'
LE_ADVERTISING_MANAGER_IFACE = 'org.bluez.LEAdvertisingManager1'
GATT_SERVICE_IFACE = 'org.bluez.GattService1'
GATT_CHRC_IFACE =    'org.bluez.GattCharacteristic1'
GATT_DESC_IFACE =    'org.bluez.GattDescriptor1'

LOCAL_NAME =         'PiZero_TTPMS'

TTPMS_SERVICE_UUID =            '6e400001-b5a3-f393-e0a9-e50e24dcca9e'
TTPMS_DATA_CHARACTERISTIC_UUID =  '1708ca6e-513e-4806-acfa-e66bf9455dee'
TTPMS_INTERVAL_CHARACTERISTIC_UUID =  'c9d9466d-cc38-47b2-89d1-22e970b1717d'

hostname = 'localhost'
username = 'root'
password = 'mynewpassword'
database = 'hubDB'

version="0.1-dev"
log_file = "../log.txt"
error_file = "../error.txt"

myConnection = mysql.connector.connect(host=hostname, user=username, passwd=password, db=database)
myCursor = myConnection.cursor()

class SensorInfoCharacteristic(Characteristic):
    def __init__(self, bus, index, service):
        Characteristic.__init__(self, bus, index, TTPMS_DATA_CHARACTERISTIC_UUID,
                                ['read'], service)
        #f = open('file.json', 'r').read()
        #self.value = bytearray(f, 'utf-8')

    def ReadValue(self, options):
        print("I got a READ on Sensor Data")
        tstamp = time.strftime('%m/%d/%Y %H:%M:%S')
        logg = tstamp+" READ on Sensor Data [Informational]\n"
        l = open(log_file, 'a+')
        l.write(logg)
        l.close()

        myCursor.execute("SELECT * from tpms ORDER BY counter DESC LIMIT 1")
        myresult = myCursor.fetchall()
		if(myresult is not None):
	        counter = str(myresult[0][0])
	        tire_id = str(myresult[0][1])
	        firmware    = str(myresult[0][2])
	        pressure = str(myresult[0][3])
	        z_axis = str(myresult[0][4])
	        x_axis = str(myresult[0][5])
	        voltage = str(myresult[0][6])
	        temp = str(myresult[0][7])
	        datax = {"counter":counter, "tire_id":tire_id, "firmware": firmware, "pressure": pressure, "z_axis": z_axis, "x_axis": x_axis, "voltage": voltage, "temp": temp}
	        str_data = json.dumps(datax)
	        valz = bytearray(str_data, 'utf-8')
	        return valz
        #return self.value

class UnderpressureService(Service):
    def __init__(self, bus, index):
        Service.__init__(self, bus, index, TTPMS_SERVICE_UUID, True)
        self.add_characteristic(SensorInfoCharacteristic(bus, 0, self))

class Application(dbus.service.Object):
    def __init__(self, bus):
        self.path = '/'
        self.services = []
        dbus.service.Object.__init__(self, bus, self.path)

    def get_path(self):
        return dbus.ObjectPath(self.path)

    def add_service(self, service):
        self.services.append(service)

    @dbus.service.method(DBUS_OM_IFACE, out_signature='a{oa{sa{sv}}}')
    def GetManagedObjects(self):
        response = {}
        print('GetManagedObjects')

        for service in self.services:
            response[service.get_path()] = service.get_properties()
            chrcs = service.get_characteristics()
            for chrc in chrcs:
                response[chrc.get_path()] = chrc.get_properties()
                descs = chrc.get_descriptors()
                for desc in descs:
                    response[desc.get_path()] = desc.get_properties()

        return response

class UnderpressureApplication(Application):
    def __init__(self, bus):  #def __init__(self, bus, display):
        Application.__init__(self, bus)
        self.add_service(UnderpressureService(bus, 0))


# I am not sure about this entirely
class UnderpressureAdvertisement(Advertisement):
    def __init__(self, bus, index):
        Advertisement.__init__(self, bus, index, 'peripheral')
        self.add_service_uuid(TTPMS_SERVICE_UUID)
        self.add_local_name(LOCAL_NAME)
        self.include_tx_power = True


def find_adapter(bus):
    remote_om = dbus.Interface(bus.get_object(BLUEZ_SERVICE_NAME, '/'),
                               DBUS_OM_IFACE)
    objects = remote_om.GetManagedObjects()
    for o, props in objects.items():
        for iface in (LE_ADVERTISING_MANAGER_IFACE, GATT_MANAGER_IFACE):
            if iface not in props:
                continue
        return o
    return None

def main():
    global mainloop
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    bus = dbus.SystemBus()
    adapter = find_adapter(bus)
    if not adapter:
        tstamp = time.strftime('%m/%d/%Y %H:%M:%S')
        logg = tstamp+" Error on Adapter BLE [Critical]\n"
        l = open(error_file, 'a+')
        l.write(logg)
        l.close()
        print('BLE adapter not found')
        return
    service_manager = dbus.Interface(
                                bus.get_object(BLUEZ_SERVICE_NAME, adapter),
                                GATT_MANAGER_IFACE)
    ad_manager = dbus.Interface(bus.get_object(BLUEZ_SERVICE_NAME, adapter),
                                LE_ADVERTISING_MANAGER_IFACE)

    app = UnderpressureApplication(bus)
    adv = UnderpressureAdvertisement(bus, 0)
    mainloop = GObject.MainLoop()

    service_manager.RegisterApplication(app.get_path(), {},
                                        reply_handler=register_app_cb,
                                        error_handler=register_app_error_cb)
    ad_manager.RegisterAdvertisement(adv.get_path(), {},
                                     reply_handler=register_ad_cb,
                                     error_handler=register_ad_error_cb)
    try:
        mainloop.run()
    except KeyboardInterrupt:
        adv.Release()

if __name__ == '__main__':
    main()

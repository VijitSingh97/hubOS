# Bluetooth_files_TPCaps
Python library for Bluetooth connectivity from the IOS app to the Raspberry PI Zero

# SETUP

Pre-Requisite: Raspberry Pi, Ubuntu on Native Machine

### Setup on Raspberry Pi (Mostly using [this](https://github.com/EnableTech/raspberry-bluetooth-demo))


```
sudo apt-get install bluetooth bluez
sudo apt-get install bluez python-bluez
sudo apt-get install libbluetooth-dev
sudo hciconfig hci0 piscan
sudo python /usr/share/doc/python-bluez/examples/simple/inquiry.py
```

### An Good example on GATT 

[Use this](https://stackoverflow.com/questions/56461087/programming-a-ble-server-and-a-client-both-in-a-raspberry-pi)

### A Good Demo which I referred first of all

[Use this](https://scribles.net/creating-ble-gatt-server-uart-service-on-raspberry-pi/)

### Some random examples, I feel they maybe useful later on (To Integrate Notify for constant reading between time intervals)

[Use this](https://github.com/ykasidit/bluez-gatt-server)

[And this](https://github.com/ARMmbed/ble-examples/tree/master/BLE_Thermometer)

### Helpful for Integration with MySQL Later
[Use this](https://www.instructables.com/id/Monitor-and-Record-Temperature-With-Bluetooth-LE-a/)

[And this](https://drive.google.com/file/d/10vOeEAbS7mi_eXn_gi_EjiGVKkSJndLA/view)

### Helpful Project for how to define characteristics

[Use this](https://github.com/prabhv/BLE-V2V-V2I/blob/30842e3e8f54950b370575217ad25fcdfa57d0b3/peripheral/infra_server.py)


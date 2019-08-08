#!/bin/bash
echo "" > /home/pi/hub_os/log/sql_wait.log
echo "starting hub_os" >> /home/pi/hub_os/log/sql_wait.log

while !(mysqladmin ping -u root --password=mynewpassword > /dev/null 2>&1)
do
	sleep 3
	echo "waiting for mysql ..." >> /home/pi/hub_os/log/sql_wait.log
done
echo "starting sensor read" >> /home/pi/hub_os/log/sql_wait.log
/home/pi/hub_os/read_rf_data &
#echo $! >/home/pi/hub_os/log/pid/read_rf_data.pid

# TODO CHECK HOW TO DELAY FOR BLE TO START
#sleep 15

echo "starting ble service" >> /home/pi/hub_os/log/sql_wait.log
/home/pi/hub_os/ble/new_broadcast &
#echo $! >/home/pi/hub_os/log/pid/new_broadcast.pid

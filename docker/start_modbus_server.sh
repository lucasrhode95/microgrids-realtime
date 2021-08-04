#!/bin/bash
set -e

# CPU_ARCHITECTURE=arm-linux-gnueabihf # raspberry
CPU_ARCHITECTURE=x86_64-linux-gnu # PC

MODBUS_ROOT=/modbus
DIAGSLAVE_PATH=$MODBUS_ROOT/diagslave

SERIAL_CLIENT_PORT=0 # port that our application will use to send messages
SERIAL_SERVER_PORT=1 # port that our server will use to receive messages

SERIAL_MOUNT_PATH=$MODBUS_ROOT/virtual_serial_ports
SERIAL_SERVER=$SERIAL_MOUNT_PATH/$SERIAL_SERVER_PORT
SERIAL_CLIENT=$SERIAL_MOUNT_PATH/$SERIAL_CLIENT_PORT

mkdir -p $SERIAL_MOUNT_PATH

# this short-circuits the two ports:
socat pty,raw,echo=0,link=$SERIAL_SERVER pty,raw,echo=0,link=$SERIAL_CLIENT &

mkdir -p $MODBUS_ROOT/logs/

cd "$DIAGSLAVE_PATH/$CPU_ARCHITECTURE"
./diagslave -m rtu -a 1 $SERIAL_SERVER >> $MODBUS_ROOT/logs/diagslave_rtu.txt &
./diagslave -m tcp -a 1 >> $MODBUS_ROOT/logs/diagslave_tcp.txt &

tail -f $MODBUS_ROOT/logs/diagslave_tcp.txt

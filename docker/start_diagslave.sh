#!/bin/bash
set -e

source /etc/os-release

if [[ "$PRETTY_NAME" == *"Raspbian"* ]]; then
  CPU_ARCHITECTURE=arm-linux-gnueabihf
elif [[ "$PRETTY_NAME" == *"Ubuntu"* || "$PRETTY_NAME" == *"Debian"* ]]; then
#  CPU_ARCHITECTURE=i686-linux-gnu  # ubuntu 32
  CPU_ARCHITECTURE=x86_64-linux-gnu
elif [[ "$PRETTY_NAME" == *"Arch"* ]]; then
  CPU_ARCHITECTURE=aarch64-linux-gnu
else
  echo ">>>>>>>UNKNOWN CPU ARCHITECTURE<<<<<<<"
  echo "$PRETTY_NAME"
  CPU_ARCHITECTURE=x86_64-linux-gnu
fi

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

echo " _________________________________________________________ "
echo "|                                                         |"
echo "|              MODBUS TCP + RTU SERVER                    |"
echo "| Author: CERTI FOUNDATION                                |"
echo "| TCP @ port 502                                          |"
echo "| RTU @ /modbus/virtual_serial_ports/1, 19200, 8, 1, even |"
echo "|_________________________________________________________|"

./diagslave -m rtu -a 1 $SERIAL_SERVER &
./diagslave -m tcp -a 1 &

tail -f /dev/null

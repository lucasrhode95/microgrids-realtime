#!/bin/bash
set -e

DIAGSLAVE_PATH=$MODBUS_LIBS_PATH/diagslave
mkdir -p $DIAGSLAVE_PATH

cd $DIAGSLAVE_PATH
wget https://www.modbusdriver.com/downloads/diagslave.tgz
tar xzf diagslave.tgz -C $DIAGSLAVE_PATH --strip-components=1

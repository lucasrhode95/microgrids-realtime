#!/bin/bash
set -e

SOCAT_VERSION=1.7.4.1
SOCAT_PATH=$MODBUS_LIBS_PATH/socat
mkdir -p $SOCAT_PATH

# download, compile and install socat
cd $SOCAT_PATH
wget http://www.dest-unreach.org/socat/download/socat-$SOCAT_VERSION.tar.gz
tar -zxvf socat-$SOCAT_VERSION.tar.gz
cd socat-$SOCAT_VERSION
./configure
make
make install

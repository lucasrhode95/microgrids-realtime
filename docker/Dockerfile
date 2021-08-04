FROM python:3.9

# pymodbus
RUN python -m pip install pymodbus==2.5.2

ENV MODBUS_SCRIPTS_PATH=/modbus_scripts
ENV MODBUS_LIBS_PATH=/modbus

# The two scripts below take a long time to finish, so is preferrable to cache
# them separately
COPY ./install_socat.sh ${MODBUS_SCRIPTS_PATH}/install_socat.sh
RUN ${MODBUS_SCRIPTS_PATH}/install_socat.sh

COPY ./install_diagslave.sh ${MODBUS_SCRIPTS_PATH}/install_diagslave.sh
RUN ${MODBUS_SCRIPTS_PATH}/install_diagslave.sh

EXPOSE 502
COPY start_diagslave.sh ${MODBUS_SCRIPTS_PATH}/start_diagslave.sh
ENTRYPOINT ${MODBUS_SCRIPTS_PATH}/start_diagslave.sh
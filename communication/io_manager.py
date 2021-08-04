from dataclasses import dataclass
from enum import Enum

from pymodbus.client.sync import BaseModbusClient
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadBuilder, BinaryPayloadDecoder


class ModbusType(Enum):
    COIL = 1
    DISCRETE_INPUT = 2
    INPUT_REGISTER = 3
    HOLDING_REGISTER = 4


class DataType(Enum):
    BOOLEAN = 1
    FLOAT32 = 2


@dataclass
class IOAddress:
    name: str
    address: int
    register_type: ModbusType
    data_type: DataType


class IOManager:
    def __init__(self, io_driver: BaseModbusClient, unit_id, byte_order=Endian.Big,
                 word_order=Endian.Little):
        super().__init__()

        self.addresses = {}
        self.io_driver = io_driver
        self.unit_id = unit_id
        self.io_driver.connect()

        self.byte_order = byte_order
        self.word_order = word_order

    def add_address(self, address: IOAddress) -> None:
        self.addresses[address.name] = address

    def get_address(self, address_id: str) -> IOAddress:
        return self.addresses[address_id]

    def write(self, address_name: str, value: any):
        mb_address = self.get_address(address_name)
        if mb_address.data_type == DataType.BOOLEAN:
            self._write_boolean(mb_address, value)
        elif mb_address.data_type == DataType.FLOAT32:
            self._write_float32(mb_address, value)
        else:
            raise NotImplementedError()

    def read(self, address_name: str) -> any:
        mb_address = self.get_address(address_name)
        if mb_address.data_type == DataType.FLOAT32:
            return self._read_float32(mb_address)
        elif mb_address.data_type == DataType.BOOLEAN:
            return self._read_boolean(mb_address)
        else:
            raise NotImplementedError()

    def _read_float32(self, mb_address: IOAddress):
        if mb_address.register_type == ModbusType.HOLDING_REGISTER:
            result = self.io_driver.read_holding_registers(
                address=mb_address.address,
                count=2,
                unit=self.unit_id
            )
        elif mb_address.register_type == ModbusType.INPUT_REGISTER:
            result = self.io_driver.read_input_registers(
                address=mb_address.address,
                count=2,
                unit=self.unit_id
            )
        else:
            raise AttributeError()

        decoder = BinaryPayloadDecoder.fromRegisters(result.registers,
                                                     byteorder=self.byte_order,
                                                     wordorder=self.word_order)
        return decoder.decode_32bit_float()

    def _read_boolean(self, mb_address: IOAddress):
        if mb_address.register_type == ModbusType.COIL:
            return self.io_driver.read_coils(
                address=mb_address.address,
                count=2,
                unit=self.unit_id
            ).bits[0]
        elif mb_address.register_type == ModbusType.DISCRETE_INPUT:
            return self.io_driver.read_discrete_inputs(
                address=mb_address.address,
                count=2,
                unit=self.unit_id
            ).bits[0]
        else:
            raise AttributeError()

    def _write_float32(self, mb_address: IOAddress, value: float):
        if mb_address.register_type != ModbusType.HOLDING_REGISTER:
            raise AttributeError()

        builder = BinaryPayloadBuilder(byteorder=self.byte_order,
                                       wordorder=self.word_order)
        builder.add_32bit_float(value)
        value = builder.build()

        self.io_driver.write_registers(mb_address.address, value,
                                       skip_encode=True,
                                       unit=self.unit_id)

    def _write_boolean(self, mb_address: IOAddress, value: bool):
        if mb_address.register_type != ModbusType.COIL:
            raise AttributeError()

        self.io_driver.write_coil(mb_address.address, value,
                                  unit=self.unit_id)

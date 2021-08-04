from pymodbus.client.sync import ModbusTcpClient

from communication.io_manager import DataType, IOAddress, IOManager, ModbusType
from components.example_component import ExampleComponent
from managers.base_manager import BaseManager

io_client = IOManager(ModbusTcpClient('127.0.0.1', port=502), unit_id=1)

io_client.add_address(IOAddress(
    name='power_output',
    data_type=DataType.FLOAT32,
    register_type=ModbusType.HOLDING_REGISTER,
    address=1000
))
io_client.add_address(IOAddress(
    name='power_setpoint',
    data_type=DataType.FLOAT32,
    register_type=ModbusType.HOLDING_REGISTER,
    address=1001
))

manager = BaseManager()
manager.add_component(ExampleComponent(
    io_client=io_client
))
manager.simulate()

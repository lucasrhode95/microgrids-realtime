from dataclasses import dataclass

from components.base_component import BaseComponent
from utils.math import limit


@dataclass
class ExampleComponent(BaseComponent):
    max_power: float = 15000

    def next_step(self, t: float, previous_output: any) -> any:
        # reads value from modbus
        power_setpoint = self.io_client.read('power_setpoint')
        # limits it between 0 and MAX_POWER
        power_setpoint = limit(power_setpoint, 0, self.max_power)
        # writes the output on modbus
        self.io_client.write('power_output', power_setpoint)

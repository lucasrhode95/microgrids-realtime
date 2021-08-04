import asyncio
import time

from components.base_component import BaseComponent


class BaseManager:
    def __init__(self):
        self.t0 = 0
        self.dt = 1

        self._t = 0

        self._components: list[BaseComponent] = []
        self._previous_outputs = []
        self._warned_about_lag = False
        self._is_running = False

    async def simulate_async(self):
        try:
            await self._run()
        except:
            self.stop()

    def simulate(self):
        asyncio.run(self.simulate_async())

    async def _run(self):
        self._is_running = True

        if self.dt <= 0:
            raise ValueError("`dt` must be a positive number")

        self.trigger_initialize()

        self._t = self.t0
        while self._is_running:
            start_time = time.time()
            self.trigger_next_step()
            await self._wait_for_next_step(start_time)
            self._t += self.dt

    def trigger_initialize(self):
        for i in range(len(self._components)):
            component = self._components[i]
            self._previous_outputs[i] = component.initialize(t0=self.t0)

    async def _wait_for_next_step(self, start_time):
        elapsed_time = time.time() - start_time
        sleep_time = self.dt - elapsed_time

        if sleep_time > 0:
            try:
                await asyncio.sleep(sleep_time)
            except KeyboardInterrupt:
                self.stop()
        else:
            print(f'Simulation is lagging behind by {-1000 * sleep_time} ms.')

    def trigger_next_step(self):
        for i in range(len(self._components)):
            component = self._components[i]
            self._previous_outputs[i] = component.next_step(
                t=self._t,
                previous_output=self._previous_outputs[i],
            )

    def add_component(self, component: BaseComponent):
        component.rt_manager = self
        self._previous_outputs.append(None)
        self._components.append(component)

    def stop(self):
        self._is_running = False

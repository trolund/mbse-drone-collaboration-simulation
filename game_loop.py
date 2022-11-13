import time
from collections.abc import Callable
from typing import Union
import math


class GameLoop(object):
    def __init__(
            self,
            on_tick: Callable[[float], None],
            on_frame: Callable[[float], None],
            simulation_speed: Callable[[int], None],
            on_counter_update: Callable[[int, int], None],

    ):

        self.on_tick = on_tick
        self.on_frame = on_frame
        self.on_counter_update = on_counter_update

        self.max_TPS = 500
        self.max_FPS = 60
        self.min_FPS = 50

        # if TPS_scale = max_TPS then it is real-time
        self.TPS_scale = 30
        self.simulation_speed = simulation_speed
        self.max_TPS = self.TPS_scale * (self.simulation_speed if self.simulation_speed is not None else 1)
        self.RTC_start: Union[None, float] = None
        self.is_running = False

    def scale_simulation(self, factor: float):
        self.max_TPS = math.floor(self.TPS_scale * factor)

    @property
    def max_TPS(self):
        return self._max_TPS

    @max_TPS.setter
    def max_TPS(self, value: int):
        self._max_TPS = value

        self._total_ticks = 0
        self._delta_tick = 1.0 / self._max_TPS
        self._max_TPS_update_time = time.time()

    def start(self):
        self.RTC_start = time.time()
        self.is_running = True

        next_second = next_tick = next_forced_frame = next_frame = self.RTC_start
        ticks = frames = 0

        while (self.is_running):
            t = time.time()

            # update ticks and frames per second counter.
            if t >= next_second:
                self.on_counter_update(ticks, frames)

                next_second += 1.0
                ticks = 0
                frames = 0

            # is it time for the next tick?
            if next_tick <= t <= next_forced_frame:
                ticks += 1
                self._total_ticks += 1

                next_tick = self._max_TPS_update_time + self._delta_tick * self._total_ticks
                self.on_tick(1.0 / self.TPS_scale)

            # is it time for the next frame?
            elif t >= next_frame:
                frames += 1
                self.on_frame(time.time() - (next_tick - self._delta_tick))

                next_frame = next_second - 1 + (1.0 / self.max_FPS) * frames
                next_forced_frame = time.time() + (1.0 / self.min_FPS)

            # program is running ahead
            else:
                sleepTime = max(next_tick, next_frame) - time.time()
                # time.sleep(sleepTime)

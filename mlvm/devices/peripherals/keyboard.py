import os

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

from collections import deque

import pygame as pg

from mlvm.devices import Peripheral
from mlvm.const import READ, CPU_GOAL_CLOCK

REG_ML_KB_KEY = 0x00

POLL_INTERVAL_CYCLES = CPU_GOAL_CLOCK // 200

KEY_UP_BIT = 0x80

_EXTRA_KEYS = {
    pg.K_LSHIFT: 0x01,
    pg.K_RSHIFT: 0x02,
}

ML_KB_IRQ_ID = 0x12


def _key_code(key):
    if key < 0x80:
        return key
    return _EXTRA_KEYS.get(key)


class MLVMKeyboard(Peripheral):
    def __init__(self, bus, peripheral_id):
        super().__init__(bus, peripheral_id)
        self.key_queue = deque()
        self.next_poll_cycle = bus.cycle + POLL_INTERVAL_CYCLES

    def _poll_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()

            elif event.type in (pg.KEYDOWN, pg.KEYUP):
                code = _key_code(event.key)
                if code is not None:
                    self.key_queue.append(code | (KEY_UP_BIT if event.type == pg.KEYUP else 0))
                    self.bus.irq(ML_KB_IRQ_ID)

    def clock_neg(self):
        if self.bus.cycle >= self.next_poll_cycle:
            self._poll_events()
            self.next_poll_cycle = self.bus.cycle + POLL_INTERVAL_CYCLES

        if self.bus.address in self.addr_range and self.bus.intent == READ:
            reg = self.unoffset_addr(self.bus.address)

            if reg == REG_ML_KB_KEY:
                if self.key_queue:
                    self.bus.respond(self.key_queue.popleft())
                    if self.key_queue:
                        self.bus.irq(ML_KB_IRQ_ID)
                else:
                    self.bus.respond(0)

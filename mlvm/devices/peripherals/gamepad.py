import os

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

import pygame as pg

from mlvm.devices import Peripheral
from mlvm.const import READ

REG_BUTTONS = 0x00

BUTTON_L = 0b00000001
BUTTON_R = 0b00000010
BUTTON_U = 0b00000100
BUTTON_D = 0b00001000
BUTTON_A = 0b00010000
BUTTON_S = 0b00100000
BUTTON_Z = 0b01000000
BUTTON_X = 0b10000000

KEY_BUTTONS = {
    pg.K_LEFT: BUTTON_L,
    pg.K_RIGHT: BUTTON_R,
    pg.K_UP: BUTTON_U,
    pg.K_DOWN: BUTTON_D,
    pg.K_a: BUTTON_A,
    pg.K_s: BUTTON_S,
    pg.K_z: BUTTON_Z,
    pg.K_x: BUTTON_X,
}


class MLVMGamepad(Peripheral):
    """
    Gamepad peripheral

    Returns bit pack of 8 different keyboard keys pressed status
    """

    def clock_neg(self):
        if self.bus.address in self.addr_range and self.bus.intent == READ:
            reg = self.unoffset_addr(self.bus.address)

            if reg == REG_BUTTONS:
                keys = pg.key.get_pressed()
                buttons = 0
                for key, button in KEY_BUTTONS.items():
                    if keys[key]:
                        buttons |= button

                self.bus.respond(buttons)

from mlvm.device import Peripheral
from mlvm.const import *

import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

import pygame as pg

REG_BUTTONS = 0x00

BUTTON_L = 0b00000001
BUTTON_R = 0b00000010
BUTTON_U = 0b00000100
BUTTON_D = 0b00001000
BUTTON_A = 0b00010000
BUTTON_S = 0b00100000
BUTTON_Z = 0b01000000
BUTTON_X = 0b10000000

class MLVMGamepad(Peripheral):
    """
    Gamepad peripheral

    Returns bit pack of 8 different keyboard keys pressed status
    """

    def __init__(self, bus, peripheral_id):
        super().__init__(bus, peripheral_id)

    def clock_neg(self):
        if self.bus.address in self.addr_range and self.bus.intent == READ:
            reg = self.unoffset_addr(self.bus.address)
            
            if reg == REG_BUTTONS:
                buttons = 0
                keys = pg.key.get_pressed()
                if keys[pg.K_LEFT]: buttons |= BUTTON_L
                if keys[pg.K_RIGHT]: buttons |= BUTTON_R
                if keys[pg.K_UP]: buttons |= BUTTON_U
                if keys[pg.K_DOWN]: buttons |= BUTTON_D
                if keys[pg.K_a]: buttons |= BUTTON_A
                if keys[pg.K_s]: buttons |= BUTTON_S
                if keys[pg.K_z]: buttons |= BUTTON_Z
                if keys[pg.K_x]: buttons |= BUTTON_X
                self.bus.respond(buttons)

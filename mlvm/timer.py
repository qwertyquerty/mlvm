from mlvm.device import Peripheral
from mlvm.const import *

import time

REG_OSC_MS = 0x00
REG_OSC_DMS = 0x01
REG_OSC_HMS = 0x02
REG_RESET_TIMER = 0x0F

class MLVMTimer(Peripheral):
    def __init__(self, bus, peripheral_id):
        super().__init__(bus, peripheral_id)
        self.cycle_counter = 0

    def clock_neg(self):
        self.cycle_counter += 1
        
        if self.bus.address in self.addr_range:
            reg = self.unoffset_addr(self.bus.address)
            
            if self.bus.intent == READ:
                if reg == REG_OSC_MS:
                    ms = int(self.cycle_counter / CPU_GOAL_CLOCK * 1000)
                    self.bus.respond(ms & 0xFF)

                elif reg == REG_OSC_DMS:
                    dms = int(self.cycle_counter / CPU_GOAL_CLOCK * 10000)
                    self.bus.respond(dms & 0xFF)

                elif reg == REG_OSC_HMS:
                    hms = int(self.cycle_counter / CPU_GOAL_CLOCK * 100000)
                    self.bus.respond(hms & 0xFF)

            elif self.bus.intent == WRITE:
                if reg == REG_RESET_TIMER:
                    self.cycle_counter = 0

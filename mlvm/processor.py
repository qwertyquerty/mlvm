from mlvm.const import *
from mlvm.device import Device
from mlvm.instructions import INSTRUCTIONS

class MLVMProcessor(Device):
    def __init__(self, bus):
        super().__init__(bus)
        self.reg_p = ROM_START
        self.reg_a = 0x00
        self.reg_b = 0x00
        self.reg_c = 0x00
        self.reg_l = 0x00
        self.reg_h = 0x00
        self.reg_s = 0x00
        self.reg_t = 0x0000
    
        self.cur_instruction = None
        self.cur_step = 0

    def reset(self):
        self.bus.read(self.reg_p)

    def clock_pos(self):
        #print(self.bus.data, INSTRUCTIONS[self.bus.data])
        if self.cur_instruction is None:
            self.cur_instruction = INSTRUCTIONS[self.bus.data]
            self.cur_step = 0

        if self.cur_instruction is not None:
            step = self.cur_instruction[self.cur_step]
            if step: step(self)

            self.cur_step += 1
            if self.cur_step == len(self.cur_instruction):
                self.cur_instruction = None

        if self.cur_instruction is None:
            self.reg_p = (self.reg_p + 1) & 0xFFFF
            self.bus.read(self.reg_p)

        #print("STEP:", self.cur_step, "S:", hex(self.reg_s), "A:", hex(self.reg_a), "B:", hex(self.reg_b), "C:", hex(self.reg_c), "P:", hex(self.reg_p), "D:", hex(self.reg_l | (self.reg_h << 8)), "Data:", hex(self.bus.data), "Addr:", hex(self.bus.address), "Intent:", self.bus.intent)
        #import time; time.sleep(0.1)

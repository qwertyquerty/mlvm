from mlvm.const import *
from mlvm.devices import Device
from mlvm.instructions import INSTRUCTIONS

class MLVMProcessor(Device):
    """
    MLVM Processor
    """
    
    def __init__(self, bus):
        super().__init__(bus)
        self.reg_p = ROM_START  # Program counter register
        self.reg_a = 0x00       # A register, usually left hand operand or general util
        self.reg_b = 0x00       # B register, usually right hand operand or general util
        self.reg_c = 0x00       # C register, usually the result of an operation
        self.reg_l = 0x00       # L register, low byte of the D (address) register
        self.reg_h = 0x00       # H register, high byte of the D (address) register
        self.reg_s = 0x00       # S register, cpu status flags
        self.reg_t = 0x0000     # T register, stack pointer
    
        # Stores the current instruction
        self.cur_instruction = None

        # Stores what clock cycle of the current instruction we are currently on
        self.cur_step = 0

    def reset(self):
        # On reset we read the program counter from the bus so that on the first positive edge
        # of the clock, an instruction is already waiting for us on the data lines
        self.bus.read(self.reg_p)

    def clock_pos(self):
        # CPU is halted, do nothing
        if self.reg_s & STATUS_HALT:
            return
        
        # If there is no current instruction, assume we read an instruction from the bus on the last
        # positive edge and it is waiting for us on the data lines now, so load it in as an instruction
        if self.cur_instruction is None:
            self.cur_instruction = INSTRUCTIONS[self.bus.data]
            self.cur_step = 0

        if self.cur_instruction is not None:
            # Step through the instruction each clock cycle
            step = self.cur_instruction[self.cur_step]
            if step: step(self)

            self.cur_step += 1
            if self.cur_step == len(self.cur_instruction):
                # We reached the end of the instruction so set the current instruction to none
                self.cur_instruction = None

        if self.cur_instruction is None:
            # If We have no current instruction then increment the program counter and read it from the bus
            # to load in our next instruction
            self.reg_p = (self.reg_p + 1) & 0xFFFF
            self.bus.read(self.reg_p)

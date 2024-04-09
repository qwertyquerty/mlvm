from mlvm.devices import MLVMProcessor, Device, MLVMMemoryRW
from mlvm.const import *
from mlvm.instructions import *

class MLVMDebugger(Device):
    def __init__(self, bus):
        super().__init__(bus)

        self.cpu = None
        self.ram = None
        for device in bus.devices:
            if isinstance(device, MLVMProcessor):
                self.cpu = device
            if isinstance(device, MLVMMemoryRW) and device.addr_range.start == RAM_START:
                self.ram = device
        
        assert self.cpu is not None, "Could not find CPU, make sure you add debugger after it"
        assert self.cpu is not None, "Could not find RAM, make sure you add debugger after it"

        print(self.ram, self.ram.size)

    def clock_neg(self):
        ...

    def clock_pos(self):
        debug_string = ""

        debug_string += "[BUS]\t"
        debug_string += f"DATA: 0x{self.bus.data:02x}  ADDR: 0x{self.bus.address:04x}  INTENT: {self.bus.intent}  CYCLE: {self.bus.cycle}\n"

        debug_string += f"[CPU]\tINST: {name_from_instruction(self.cpu.cur_instruction) if self.cpu.cur_instruction else None}  STEP: {self.cpu.cur_step}\n"

        debug_string += f"[REG]\tS: 0x{self.cpu.reg_s:02x}  P: 0x{self.cpu.reg_p:04x}  T: 0x{self.cpu.reg_t:04x}  D: 0x{((self.cpu.reg_h << 8) | self.cpu.reg_l):04x} "
        debug_string += f"A: 0x{self.cpu.reg_a:02x}  B: 0x{self.cpu.reg_b:02x}  C: 0x{self.cpu.reg_c:02x}\n"

        debug_string += f"[STK]\t"

        for i in range(self.cpu.reg_t):
            debug_string += f"0x{self.ram.memory[STACK_START_ADDR + i]:02x} "

        print(debug_string)
        input()

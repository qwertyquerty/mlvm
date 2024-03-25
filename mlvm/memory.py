from mlvm.device import Device
from mlvm.const import *

class MLVMMemoryRW(Device):
    def __init__(self, bus, start_addr, size):
        self.bus = bus
        self.size = size
        self.addr_range = range(start_addr, start_addr+size)
        self.memory = [0x00 for i in self.addr_range]

    def unoffset_addr(self, addr):
        return addr - self.addr_range.start

    def clock_neg(self):
        if self.bus.address in self.addr_range:
            if self.bus.intent == READ:
                self.bus.respond(self.memory[self.unoffset_addr(self.bus.address)])
            elif self.bus.intent == WRITE:
                self.memory[self.unoffset_addr(self.bus.address)] = self.bus.data
        
    def load_file(self, file):
        for i in self.addr_range:
            b = file.read(1)
            self.memory[self.unoffset_addr(i)] = ord(b) if b else 0x00

class MLVMMemoryRO(MLVMMemoryRW):
    def clock_neg(self):
        if self.bus.address in self.addr_range and self.bus.intent == READ:
            self.bus.respond(self.memory[self.unoffset_addr(self.bus.address)])
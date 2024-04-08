from mlvm.device import AddressedDevice
from mlvm.const import *

class MLVMMemoryRW(AddressedDevice):
    """
    Read/write memory
    """

    def __init__(self, bus, start_addr, size):
        super().__init__(bus)
        self.size = size
        self.addr_range = range(start_addr, start_addr+size)
        self.memory = [0x00 for i in self.addr_range] # Initialize memory to all 0x00

    def clock_neg(self):
        if self.bus.address in self.addr_range: # If the current bus address is in our address range, we are being addressed
            if self.bus.intent == READ:
                self.bus.respond(self.memory[self.unoffset_addr(self.bus.address)]) # Respond on the bus if a read
            elif self.bus.intent == WRITE:
                self.memory[self.unoffset_addr(self.bus.address)] = self.bus.data # Write data lines to memory if a write
        
    def load_file(self, file, offset=0):
        """
        Load a bin file into the memory
        """

        for i in self.addr_range:
            b = file.read(1)
            self.memory[offset + self.unoffset_addr(i)] = ord(b) if b else 0x00

class MLVMMemoryRO(MLVMMemoryRW):
    """
    Read only memory
    """

    def clock_neg(self):
        # ROM only responds to reads, ignores writes
        if self.bus.address in self.addr_range and self.bus.intent == READ:
            self.bus.respond(self.memory[self.unoffset_addr(self.bus.address)])

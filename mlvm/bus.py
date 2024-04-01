from mlvm.const import *
from mlvm.device import Device

class MLVMBus():
    READ = False
    WRITE = True

    def __init__(self):
        self.devices: list[Device] = []
        self.address = self.next_address = 0x0000
        self.data = self.next_data = 0x00
        self.intent = self.next_intent = READ
        self.cycle = 0

    def reset(self):
        for device in self.devices:
            device.reset()

    def tick(self) -> None:
        self.clock_neg()
        self.clock_pos()
        self.cycle += 1

    def clock_pos(self) -> None:
        self.latch()
        
        for device in self.devices:
            device.clock_pos()
    
    def clock_neg(self) -> None:
        self.latch()

        for device in self.devices:
            device.clock_neg()

    def read(self, addr) -> None:
        self.next_address = addr & 0xFFFF
        self.next_intent = READ

    def respond(self, data) -> None:
        self.next_data = data

    def write(self, addr, data) -> None:
        self.next_address = addr & 0xFFFF
        self.next_data = data & 0xFF
        self.next_intent = WRITE

    def latch(self):
        self.address = self.next_address
        self.data = self.next_data
        self.intent = self.next_intent


from mlvm.const import *

class Device():
    def __init__(self, bus):
        self.bus = bus
        self.bus.devices.append(self)

    def reset(self):
        ...

    def clock_pos(self):
        ...
    
    def clock_neg(self):
        ...

class AddressedDevice(Device):
    addr_range: range

    def unoffset_addr(self, addr):
        return addr - self.addr_range.start

class Peripheral(AddressedDevice):
    def __init__(self, bus, peripheral_id):
        super().__init__(bus)
        self.peripheral_id = peripheral_id
        self.size = PERIPH_SIZE
        self.addr_range = range(PERIPHS_START + self.peripheral_id * PERIPH_SIZE, PERIPHS_START + self.peripheral_id * PERIPH_SIZE + PERIPH_SIZE)

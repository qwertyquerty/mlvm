from mlvm.const import *

class Device():
    """
    A device that can be attached to the clock, reset, address, data, and intent lines of a bus
    """
    
    def __init__(self, bus):
        self.bus = bus
        self.bus.devices.append(self)

    def reset(self):
        """
        Called once on startup before the clock begins to tick
        """

    def clock_pos(self):
        """
        Called on every positive edge of the clock
        """
    
    def clock_neg(self):
        """
        Called on every negative edge of the clock
        """

class AddressedDevice(Device):
    """
    Device on the bus that can be addressed
    """
    
    addr_range: range

    def unoffset_addr(self, addr):
        """
        Convert a bus address to a device address by subtracting the device start address
        """
        return addr - self.addr_range.start

class Peripheral(AddressedDevice):
    """
    A device intended to largely encapsulate its own operation
    
    Gets authority over one PERIPH_SIZE block of memory for registers
    Start positioned at PERIPHS_START + PERIPH_SIZE * peripheral_id
    """
    
    def __init__(self, bus, peripheral_id):
        super().__init__(bus)
        self.peripheral_id = peripheral_id
        self.size = PERIPH_SIZE
        self.addr_range = range(PERIPHS_START + self.peripheral_id * PERIPH_SIZE, PERIPHS_START + self.peripheral_id * PERIPH_SIZE + PERIPH_SIZE)

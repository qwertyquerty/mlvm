from mlvm.const import *
from mlvm.device import Device

class MLVMBus():
    def __init__(self):
        # List of devices connected to this bus
        self.devices: list[Device] = []

        # Current address on the address lines
        self.address = self.next_address = 0x0000

        # Current value on the data lines
        self.data = self.next_data = 0x00

        # Current intent on the intent line
        self.intent = self.next_intent = READ

        # Cycle counter
        self.cycle = 0

    def reset(self):
        """
        Called once on startup, resets all attached devices
        """

        for device in self.devices:
            device.reset()

    def tick(self) -> None:
        """
        Called at the bus cycle speed, clocks all attached devices
        """

        self.clock_neg()
        self.clock_pos()
        self.cycle += 1

    def clock_pos(self) -> None:
        """
        Positive edge of the clock, latches lines and clocks all devices
        """

        self.latch()
        
        for device in self.devices:
            device.clock_pos()
    
    def clock_neg(self) -> None:
        """
        Negative edge of the clock, latches lines and clocks all devices
        """

        self.latch()

        for device in self.devices:
            device.clock_neg()

    def read(self, addr) -> None:
        """
        Read from the bus by putting an address, will be latched on the next edge of the clock
        """
        
        self.next_address = addr & 0xFFFF
        self.next_intent = READ

    def respond(self, data) -> None:
        """
        Respond to a read/write from another device on the bus, will be latched on the next edge of the clock
        """

        self.next_data = data

    def write(self, addr, data) -> None:
        """
        Write to the clock by putting an address and data then setting the intent to write, latched on the edge of the clock
        """
        
        self.next_address = addr & 0xFFFF
        self.next_data = data & 0xFF
        self.next_intent = WRITE

    def latch(self):
        """
        Called on each clock edge to finalize the address, data, and intent lines for each clock so that
        they will not change again until the next edge of the clock
        """
        
        self.address = self.next_address
        self.data = self.next_data
        self.intent = self.next_intent


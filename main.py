from mlvm.bus import MLVMBus
from mlvm.memory import MLVMMemoryRO, MLVMMemoryRW
from mlvm.processor import MLVMProcessor
from mlvm.const import *

bus = MLVMBus()
ram = MLVMMemoryRW(bus, RAM_START, RAM_SIZE)
rom = MLVMMemoryRO(bus, ROM_START, ROM_SIZE)
cpu = MLVMProcessor(bus)

rom.load_file(open("rom.bin", "rb"))

bus.devices.append(ram)
bus.devices.append(rom)
bus.devices.append(cpu)

bus.reset()

i = 0
while True:
    bus.tick()
    i += 1

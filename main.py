from mlvm.bus import MLVMBus
from mlvm.memory import MLVMMemoryRO, MLVMMemoryRW
from mlvm.processor import MLVMProcessor
from mlvm.video import MLVMVideoInterface
from mlvm.const import *

import time

bus = MLVMBus()
cpu = MLVMProcessor(bus)
ram = MLVMMemoryRW(bus, RAM_START, RAM_SIZE)
rom = MLVMMemoryRO(bus, ROM_START, ROM_SIZE)
gpu = MLVMVideoInterface(bus, PERIPH_ID_VIDEO)

rom.load_file(open("rom.bin", "rb"))

bus.reset()

start_time = time.time()

i = 0
while True:
    bus.tick()
    i += 1
    if i % 100_000 == 0:
        print(f"{i / (time.time() - start_time):,.0f} cycles/s")

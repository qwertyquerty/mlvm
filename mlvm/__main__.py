from mlvm.bus import MLVMBus
from mlvm.memory import MLVMMemoryRO, MLVMMemoryRW
from mlvm.processor import MLVMProcessor
from mlvm.video import MLVMVideoInterface
from mlvm.gamepad import MLVMGamepad
from mlvm.const import *

import sys
import time

if len(sys.argv) < 2:
    print("You must specify an input rom!")
    exit(1)

input_file = sys.argv[1]

bus = MLVMBus()
cpu = MLVMProcessor(bus)
ram = MLVMMemoryRW(bus, RAM_START, RAM_SIZE)
rom = MLVMMemoryRO(bus, ROM_START, ROM_SIZE)
try:
    with open(input_file, "rb") as input_stream:
        rom.load_file(input_stream)
except:
    print(f"Failed to open {input_file}!")
    exit(1)

gpu = MLVMVideoInterface(bus, PERIPH_ID_VIDEO)
pad = MLVMGamepad(bus, PERIPH_ID_GAMEPAD)

bus.reset()

start_time = time.time()

i = 0
while True:
    bus.tick()
    i += 1
    if i % 1_000_000 == 0:
        print(f"{i / (time.time() - start_time):,.0f} cycles/s")

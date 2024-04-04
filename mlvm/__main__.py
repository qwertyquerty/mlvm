from mlvm.bus import MLVMBus
from mlvm.memory import MLVMMemoryRO, MLVMMemoryRW
from mlvm.processor import MLVMProcessor
from mlvm.video import MLVMVideoInterface
from mlvm.gamepad import MLVMGamepad
from mlvm.timer import MLVMTimer
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
osc = MLVMTimer(bus, PERIPH_ID_TIMER)

bus.reset()

start_time = time.perf_counter()
last_tick_time = time.perf_counter()
cur_tick_time = time.perf_counter()

perf_cycle_offset = 0
perf_time_offset = 0

sleep_interval = 10_000

i = 0
while True:
    bus.tick()
    i += 1
    if i % CPU_GOAL_CLOCK == 0:
        print(f"{(i-perf_cycle_offset) / (time.perf_counter() - perf_time_offset):,.0f} cycles/s")
        perf_cycle_offset = i
        perf_time_offset = time.perf_counter()

    if i % sleep_interval == 0:
        cur_tick_time = time.perf_counter()
        while ((sleep_interval/CPU_GOAL_CLOCK) - (time.perf_counter()-last_tick_time)) > 0:
            pass
        
        last_tick_time = time.perf_counter()

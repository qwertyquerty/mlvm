"""
MLVM Virtual Machine
"""

from mlvm.bus import MLVMBus
from mlvm.devices import MLVMProcessor, MLVMMemoryRO, MLVMMemoryRW, MLVMVideoInterface, MLVMGamepad, MLVMTimer
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

while True:
    bus.tick() # Tick the bus

    if bus.cycle % CPU_GOAL_CLOCK == 0:
        # Output the current bus clock speed
        print(f"{(bus.cycle-perf_cycle_offset) / (time.perf_counter() - perf_time_offset):,.0f} cycles/s")
        perf_cycle_offset = bus.cycle
        perf_time_offset = time.perf_counter()

    if bus.cycle % CPU_SLEEP_INTERVAL == 0:
        # Sleep to make up for the cpu running faster than it should
        cur_tick_time = time.perf_counter()
        while ((CPU_SLEEP_INTERVAL/CPU_GOAL_CLOCK) - (time.perf_counter()-last_tick_time)) > 0:
            pass
        
        last_tick_time = time.perf_counter()

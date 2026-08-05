"""
MLVM Virtual Machine
"""

import time

from mlvm.bus import MLVMBus
from mlvm.devices import (
    MLVMProcessor,
    MLVMMemoryRO,
    MLVMMemoryRW,
    MLVMVideoInterface,
    MLVMGamepad,
    MLVMTimer,
    MLVMKeyboard,
    MLVMStorage,
)
from mlvm.const import (
    RAM_START,
    RAM_SIZE,
    ROM_START,
    ROM_SIZE,
    PERIPH_ID_VIDEO,
    PERIPH_ID_GAMEPAD,
    PERIPH_ID_TIMER,
    PERIPH_ID_KEYBOARD,
    PERIPH_ID_STORAGE,
    CPU_GOAL_CLOCK,
    CPU_SLEEP_INTERVAL,
)


def build_machine(rom_path, storage_path="storage.img"):
    bus = MLVMBus()

    MLVMProcessor(bus)
    MLVMMemoryRW(bus, RAM_START, RAM_SIZE)
    rom = MLVMMemoryRO(bus, ROM_START, ROM_SIZE)

    with open(rom_path, "rb") as rom_file:
        rom.load_file(rom_file)

    MLVMVideoInterface(bus, PERIPH_ID_VIDEO)
    MLVMGamepad(bus, PERIPH_ID_GAMEPAD)
    MLVMTimer(bus, PERIPH_ID_TIMER)
    MLVMKeyboard(bus, PERIPH_ID_KEYBOARD)
    MLVMStorage(bus, PERIPH_ID_STORAGE, storage_path)

    return bus


def run(bus):
    bus.reset()

    last_tick_time = time.perf_counter()
    perf_cycle_offset = 0
    perf_time_offset = time.perf_counter()

    while True:
        bus.tick()

        if bus.cycle % CPU_SLEEP_INTERVAL == 0:
            if bus.cycle % (CPU_SLEEP_INTERVAL * 100) == 0:
                print(f"{(bus.cycle - perf_cycle_offset) / (time.perf_counter() - perf_time_offset):,.0f} cycles/s")
                perf_cycle_offset = bus.cycle
                perf_time_offset = time.perf_counter()

            # Sleep to make up for the cpu running faster than it should
            while (CPU_SLEEP_INTERVAL / CPU_GOAL_CLOCK) - (time.perf_counter() - last_tick_time) > 0:
                pass

            last_tick_time = time.perf_counter()

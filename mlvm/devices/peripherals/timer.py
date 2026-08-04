from mlvm.devices import Peripheral
from mlvm.const import READ, WRITE, CPU_GOAL_CLOCK

REG_TIME_MS_LO = 0x00
REG_TIME_MS_HI = 0x01

REG_TIME_US_LO = 0x02
REG_TIME_US_HI = 0x03

REG_IRQ1_INTERVAL = 0x04
REG_IRQ2_INTERVAL = 0x05

REG_RESET_TIMER = 0x0F

TIMER_IRQ1_ID = 0x10
TIMER_IRQ2_ID = 0x11


class MLVMTimer(Peripheral):
    """
    Timer peripheral

    Counts bus cycles at different modulos, makes counter values available in registers, and can
    fire a periodic IRQ at a configurable interval (used for preemptive scheduling)
    """

    def __init__(self, bus, peripheral_id):
        super().__init__(bus, peripheral_id)
        self.cycle_counter = 0

        # 0 means disarmed, otherwise holds the cycle count converted from milliseconds
        self.irq1_interval_cycles = 0
        self.next_irq1_cycle = 0
        self.irq2_interval_cycles = 0
        self.next_irq2_cycle = 0

    def clock_neg(self):
        self.cycle_counter += 1

        if self.irq1_interval_cycles and self.cycle_counter >= self.next_irq1_cycle:
            self.bus.irq(TIMER_IRQ1_ID)
            self.next_irq1_cycle = self.cycle_counter + self.irq1_interval_cycles

        if self.irq2_interval_cycles and self.cycle_counter >= self.next_irq2_cycle:
            self.bus.irq(TIMER_IRQ2_ID)
            self.next_irq2_cycle = self.cycle_counter + self.irq2_interval_cycles

        if self.bus.address in self.addr_range:
            reg = self.unoffset_addr(self.bus.address)

            if self.bus.intent == READ:
                if reg == REG_TIME_MS_LO:  # Timer milliseconds low byte
                    ms = int(self.cycle_counter / CPU_GOAL_CLOCK * 1e3)
                    self.bus.respond(ms & 0xFF)

                if reg == REG_TIME_MS_HI:  # Timer milliesconds high byte
                    ms = int(self.cycle_counter / CPU_GOAL_CLOCK * 1e3)
                    self.bus.respond((ms >> 8) & 0xFF)

                if reg == REG_TIME_US_LO:  # Timer microseconds low byte
                    ms = int(self.cycle_counter / CPU_GOAL_CLOCK * 1e6)
                    self.bus.respond(ms & 0xFF)

                if reg == REG_TIME_US_HI:  # Timer microseconds low byte
                    ms = int(self.cycle_counter / CPU_GOAL_CLOCK * 1e6)
                    self.bus.respond((ms >> 8) & 0xFF)

            elif self.bus.intent == WRITE:
                if reg == REG_RESET_TIMER:  # Reset timers to 0
                    self.cycle_counter = 0

                elif reg == REG_IRQ1_INTERVAL:  # Arm (period in milliseconds) / disarm (0) periodic IRQ1
                    self.irq1_interval_cycles = int(self.bus.data / 1e3 * CPU_GOAL_CLOCK)
                    self.next_irq1_cycle = self.cycle_counter + self.irq1_interval_cycles

                elif reg == REG_IRQ2_INTERVAL:  # Arm (period in milliseconds) / disarm (0) periodic IRQ2
                    self.irq2_interval_cycles = int(self.bus.data / 1e3 * CPU_GOAL_CLOCK)
                    self.next_irq2_cycle = self.cycle_counter + self.irq2_interval_cycles

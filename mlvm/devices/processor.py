from mlvm.const import (
    ROM_START,
    ROM_NMI_HANDLER_ADDR,
    ROM_IRQ_HANDLER_ADDR,
    STATUS_HALT,
    STATUS_CLI,
    STATUS_IN_IRQ,
    STATUS_IN_NMI,
)
from mlvm.devices import Device
from mlvm.instructions import INSTRUCTIONS


class MLVMProcessor(Device):
    """
    MLVM Processor
    """

    def __init__(self, bus):
        super().__init__(bus)
        self.reg_p = ROM_START  # P register, 16-bit, program counter register
        self.reg_a = 0x0000     # A register, 16-bit, usually left hand operand or general util
        self.reg_b = 0x0000     # B register, 16-bit, usually right hand operand or general util
        self.reg_c = 0x0000     # C register, 16-bit, result of the last operation and memory/jump address
        self.reg_d = 0x0000     # D register, 16-bit, compiler-only scratch for deferred expression sub-results
        self.reg_s = 0x00       # S register, 8-bit, cpu status flags
        self.reg_t = 0x0000     # T register, 16-bit, stack pointer

        # Internal scratch byte/buffer, used by instructions that need to build 16 bit values without using registers
        self.scratch = 0x00
        self.frame_scratch = []

        # Stores the current instruction
        self.cur_instruction = None

        # Stores what clock cycle of the current instruction we are currently on
        self.cur_step = 0

        # Stack of saved register states, one per interrupt currently being serviced, so an NMI
        # taken while inside an IRQ restores back into that IRQ's state rather than clobbering it
        self.interrupt_stack = []

    def enter_interrupt(self, in_nmi):
        self.interrupt_stack.append(
            (self.reg_p, self.reg_a, self.reg_b, self.reg_c, self.reg_d, self.reg_s, self.reg_t)
        )
        self.reg_s |= STATUS_IN_NMI if in_nmi else STATUS_IN_IRQ

    def exit_interrupt(self):
        assert self.reg_s & (STATUS_IN_NMI | STATUS_IN_IRQ)
        self.reg_p, self.reg_a, self.reg_b, self.reg_c, self.reg_d, self.reg_s, self.reg_t = self.interrupt_stack.pop()

    def reset(self):
        # On reset we read the program counter from the bus so that on the first positive edge
        # of the clock, an instruction is already waiting for us on the data lines
        self.bus.read(self.reg_p)

    def clock_pos(self):
        # CPU is halted, do nothing
        if self.reg_s & STATUS_HALT:
            return

        # If there is no current instruction, assume we read an instruction from the bus on the last
        # positive edge and it is waiting for us on the data lines now, so load it in as an instruction
        if self.cur_instruction is None:
            self.cur_instruction = INSTRUCTIONS[self.bus.data]
            self.cur_step = 0

        if self.cur_instruction is not None:
            # Step through the instruction each clock cycle
            step = self.cur_instruction[self.cur_step]
            if step:
                step(self)

            self.cur_step += 1
            if self.cur_step == len(self.cur_instruction):
                # We reached the end of the instruction so set the current instruction to none
                self.cur_instruction = None

        if self.cur_instruction is None:
            # NMIs may interrupt an in-progress IRQ, but not another NMI. IRQs are additionally
            # blocked while inside an NMI or another IRQ. Both are gated by the enable flag.
            if not (self.reg_s & STATUS_CLI) and not (self.reg_s & STATUS_IN_NMI) and self.bus.nmi_status:
                self.bus.nmi_status = 0
                self.enter_interrupt(in_nmi=True)
                self.reg_a = self.bus.nmi_id
                self.reg_p = ROM_NMI_HANDLER_ADDR
            elif (
                not (self.reg_s & STATUS_CLI)
                and not (self.reg_s & (STATUS_IN_IRQ | STATUS_IN_NMI))
                and self.bus.irq_status
            ):
                self.bus.irq_status = 0
                self.enter_interrupt(in_nmi=False)
                self.reg_a = self.bus.irq_id
                self.reg_p = ROM_IRQ_HANDLER_ADDR
            else:
                # If We have no current instruction then increment the program counter and
                # read it from the bus to load in our next instruction
                self.reg_p = (self.reg_p + 1) & 0xFFFF

            self.bus.read(self.reg_p)

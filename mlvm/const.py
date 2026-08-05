# Intent line enum
READ = 0
WRITE = 1

# Status register flags
STATUS_WAIT = 1 << 0
STATUS_CARRY = 1 << 1
STATUS_HALT = 1 << 2
STATUS_CLI = 1 << 3  # Interrupt enable: gates both IRQs and NMIs
STATUS_IN_IRQ = 1 << 4  # Set while servicing an IRQ, cleared on RTI
STATUS_IN_NMI = 1 << 5  # Set while servicing an NMI, cleared on RTI

# Types of processor errors
ERR_HALT = 0
ERR_STACK_OVERFLOW = 1
ERR_STACK_UNDERFLOW = 2

# Start of the ram
RAM_START = 0x0000
RAM_SIZE = 0x6000

# Memory layout, interrupt tables
NMI_TABLE_START_ADDR = 0x400
NMI_TABLE_END_ADDR = 0x5FF
IRQ_TABLE_START_ADDR = 0x600
IRQ_TABLE_END_ADDR = 0x7FF

# Memory layout, stack
STACK_START_ADDR = 0x800
STACK_POINTER_MAX = 0xFFF

# Memory layout, program memory
PROG_MEM_START_ADDR = 0x1000
PROG_MEM_END_ADDR = 0x5FFF

# Start of the peripherals block
PERIPHS_START = 0x6000
PERIPH_SIZE = 0x0080
PERIPHS_SIZE = 0x2000

# Standard positions of common peripherals
PERIPH_ID_VIDEO = 0x00
PERIPH_ID_GAMEPAD = 0x01
PERIPH_ID_TIMER = 0x02
PERIPH_ID_KEYBOARD = 0x03
PERIPH_ID_STORAGE = 0x04

# Start of the rom
ROM_START = 0x8000
ROM_SIZE = 0x8000

ROM_IRQ_HANDLER_ADDR = 0xFFC0
ROM_NMI_HANDLER_ADDR = 0xFFE0

# The goal clock speed to maintain
CPU_GOAL_CLOCK = 4_000_000

# How many cycles should pass before we sleep to maintain clock speed
CPU_SLEEP_INTERVAL = 100_000

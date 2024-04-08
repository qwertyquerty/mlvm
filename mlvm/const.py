# Intent line enum
READ = 0
WRITE = 1

# Status register flags
STATUS_WAIT = 1 << 0
STATUS_CARRY = 1 << 1
STATUS_HALT = 1 << 2

# Types of processor errors
ERR_HALT = 0
ERR_STACK_OVERFLOW = 1
ERR_STACK_UNDERFLOW = 2

# Start of the ram
RAM_START = 0x0000
RAM_SIZE = 0x6000

# Memory layout, stack
STACK_START_ADDR = 0x0000
STACK_POINTER_MAX = 0x3FF

# Memory layout, program memory
PROG_MEM_START_ADDR = 0x0400
PROG_MEM_END_ADDR = 0x7FFF

# Start of the peripherals block
PERIPHS_START = 0x6000
PERIPH_SIZE = 0x0080
PERIPHS_SIZE = 0x2000

# Standard positions of common peripherals
PERIPH_ID_VIDEO = 0x00
PERIPH_ID_GAMEPAD = 0x01
PERIPH_ID_TIMER = 0x02

# Start of the rom
ROM_START = 0x8000
ROM_SIZE = 0x8000

# The goal clock speed to maintain
CPU_GOAL_CLOCK = 3_000_000

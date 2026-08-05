import mmap
import os

from mlvm.devices import Peripheral
from mlvm.const import READ, WRITE

REG_BLOCK_LO = 0x00
REG_BLOCK_HI = 0x01
REG_OFFSET = 0x02
REG_DATA = 0x03
REG_STREAM = 0x04

BLOCK_SIZE = 256
BLOCK_COUNT = 0x10000
STORAGE_FILE_SIZE = BLOCK_SIZE * BLOCK_COUNT


class MLVMStorage(Peripheral):
    """
    Block storage peripheral

    BLOCK_COUNT blocks of BLOCK_SIZE bytes each, backed by a real file on disk
    """

    def __init__(self, bus, peripheral_id, storage_path="storage.img"):
        super().__init__(bus, peripheral_id)

        if not os.path.exists(storage_path) or os.path.getsize(storage_path) != STORAGE_FILE_SIZE:
            with open(storage_path, "wb") as f:
                f.truncate(STORAGE_FILE_SIZE)

        self.storage_file = open(storage_path, "r+b")
        self.blocks = mmap.mmap(self.storage_file.fileno(), STORAGE_FILE_SIZE)

        self.block_lo = 0
        self.block_hi = 0
        self.offset = 0

    def _block_base(self):
        return ((self.block_hi << 8) | self.block_lo) * BLOCK_SIZE

    def clock_neg(self):
        if self.bus.address not in self.addr_range:
            return
        reg = self.unoffset_addr(self.bus.address)

        if self.bus.intent == READ:
            if reg == REG_DATA:
                self.bus.respond(self.blocks[self._block_base() + self.offset])
            elif reg == REG_STREAM:
                self.bus.respond(self.blocks[self._block_base() + self.offset])
                self.offset = (self.offset + 1) % BLOCK_SIZE

        elif self.bus.intent == WRITE:
            if reg == REG_BLOCK_LO:
                self.block_lo = self.bus.data
                self.offset = 0
            elif reg == REG_BLOCK_HI:
                self.block_hi = self.bus.data
                self.offset = 0
            elif reg == REG_OFFSET:
                self.offset = self.bus.data
            elif reg == REG_DATA:
                self.blocks[self._block_base() + self.offset] = self.bus.data
            elif reg == REG_STREAM:
                self.blocks[self._block_base() + self.offset] = self.bus.data
                self.offset = (self.offset + 1) % BLOCK_SIZE

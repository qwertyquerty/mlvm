import os

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

import colorsys
import pygame as pg

from mlvm.devices import Peripheral
from mlvm.const import WRITE, CPU_GOAL_CLOCK

VIDEO_WIDTH = 0x100
VIDEO_HEIGHT = 0x100

TEXRAM_WIDTH = 0x100
TEXRAM_HEIGHT = 0x100

REG_X = 0x00
REG_Y = 0x01
REG_W = 0x02
REG_H = 0x03

REG_PIXEL = 0x04
REG_FILL = 0x05
REG_RECT = 0x06

REG_FPS = 0xA

REG_TEXRAM_PIXEL = 0xC
REG_TEXRAM_SRC_X = 0xD
REG_TEXRAM_SRC_Y = 0xE
REG_TEXRAM_BLIT = 0xF

BLEND_MODES = [0, pg.BLEND_ADD, pg.BLEND_SUB, pg.BLEND_MULT, pg.BLEND_MIN, pg.BLEND_MAX]

DISPLAY_SCALE = 3

FLIP_NMI_ID = 0x40


def byte_to_rgb(color_byte):
    """
    Convert a pseudo-HSV byte to RGB
    """

    hn = color_byte & 0b00001111
    vn = (color_byte >> 4) & 0b00000011
    sn = (color_byte >> 6) & 0b00000011

    h = hn / 16
    v = (0, 0.25, 0.5, 1)[vn]
    s = (0, 1 / 3, 2 / 3, 1)[sn]

    r, g, b = colorsys.hsv_to_rgb(h, s, v)

    return (r * 255, g * 255, b * 255)


class MLVMVideoInterface(Peripheral):
    """
    Video peripheral

    Opens up a display that can be drawn to and updated
    """

    def __init__(self, bus, peripheral_id):
        super().__init__(bus, peripheral_id)
        self.video_ram = [0x00 for i in range(VIDEO_WIDTH * VIDEO_HEIGHT)]

        self.reg_x = 0
        self.reg_y = 0
        self.reg_w = 0
        self.reg_h = 0
        self.reg_fps = 60

        self.reg_texram_src_x = 0
        self.reg_texram_src_y = 0

        self.screen = pg.display.set_mode(
            (VIDEO_WIDTH * DISPLAY_SCALE, VIDEO_HEIGHT * DISPLAY_SCALE),
            pg.DOUBLEBUF | pg.HWACCEL | pg.HWSURFACE,
        )
        pg.display.set_caption("MLVM")
        pg.display.set_icon(pg.Surface((1, 1)))

        self.surface = pg.Surface((VIDEO_WIDTH, VIDEO_HEIGHT))
        self.texram = pg.Surface((TEXRAM_WIDTH, TEXRAM_HEIGHT))

        self.clock = pg.time.Clock()

        self.next_frame_cycle = 0
        self._set_fps(self.reg_fps)

    def _set_x(self, value):
        self.reg_x = value % VIDEO_WIDTH

    def _set_y(self, value):
        self.reg_y = value % VIDEO_HEIGHT

    def _set_w(self, value):
        self.reg_w = value % VIDEO_WIDTH

    def _set_h(self, value):
        self.reg_h = value % VIDEO_HEIGHT

    def _write_pixel(self, value):
        self.surface.set_at((self.reg_x, self.reg_y), byte_to_rgb(value))

    def _write_fill(self, value):
        self.surface.fill(byte_to_rgb(value))

    def _write_rect(self, value):
        pg.draw.rect(self.surface, byte_to_rgb(value), (self.reg_x, self.reg_y, self.reg_w, self.reg_h))

    def _set_fps(self, value):
        self.reg_fps = value
        self.next_frame_cycle = self.bus.cycle + (CPU_GOAL_CLOCK // self.reg_fps)

    def _write_texram_pixel(self, value):
        self.texram.set_at((self.reg_x, self.reg_y), byte_to_rgb(value))

    def _set_texram_src_x(self, value):
        self.reg_texram_src_x = value % TEXRAM_WIDTH

    def _set_texram_src_y(self, value):
        self.reg_texram_src_y = value % TEXRAM_HEIGHT

    def _texram_blit(self, value):
        self.surface.blit(
            self.texram,
            (self.reg_x, self.reg_y),
            area=(self.reg_texram_src_x, self.reg_texram_src_y, self.reg_w, self.reg_h),
            special_flags=BLEND_MODES[value] if value < len(BLEND_MODES) else 0,
        )

    _REGISTER_WRITE_HANDLERS = {
        REG_X: _set_x,
        REG_Y: _set_y,
        REG_W: _set_w,
        REG_H: _set_h,
        REG_PIXEL: _write_pixel,
        REG_FILL: _write_fill,
        REG_RECT: _write_rect,
        REG_FPS: _set_fps,
        REG_TEXRAM_PIXEL: _write_texram_pixel,
        REG_TEXRAM_SRC_X: _set_texram_src_x,
        REG_TEXRAM_SRC_Y: _set_texram_src_y,
        REG_TEXRAM_BLIT: _texram_blit,
    }

    def _present_frame(self):
        self.bus.nmi(FLIP_NMI_ID)

        pg.transform.scale_by(self.surface, DISPLAY_SCALE, self.screen)
        pg.display.flip()
        self.clock.tick(-1)
        pg.display.set_caption(f"MLVM FPS: {int(self.clock.get_fps())}")

    def clock_neg(self):
        if self.bus.address in self.addr_range and self.bus.intent == WRITE:
            handler = self._REGISTER_WRITE_HANDLERS.get(self.unoffset_addr(self.bus.address))
            if handler is not None:
                handler(self, self.bus.data)

        if self.bus.cycle >= self.next_frame_cycle:
            self._present_frame()
            self.next_frame_cycle = self.bus.cycle + (CPU_GOAL_CLOCK // self.reg_fps)

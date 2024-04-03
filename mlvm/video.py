from mlvm.device import Peripheral
from mlvm.const import *

import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

import pygame as pg
import colorsys

REG_X_POS = 0x00
REG_Y_POS = 0x01
REG_COLOR = 0x02
REG_FLIP = 0x03
REG_FILL = 0x04

EVENT_CYCLE_INTERVAL = 1000

DISPLAY_SCALE = 8

def byte_to_rgb(color_byte):
    hv = color_byte & 0b11111000

    if hv == 0b00111000:
        return (255, 255, 255)
    
    if hv == 0:
        return (0, 0, 0)

    hn = color_byte & 0b00000111
    vn = (color_byte >> 3) & 0b00000111
    sn = (color_byte >> 6) & 0b00000011
    
    h = hn / 8
    v = (vn+1) / 8
    s = (sn+1) / 4

    r,g,b = colorsys.hsv_to_rgb(h, s, v)

    return (r*255, g*255, b*255)


class MLVMVideoInterface(Peripheral):
    def __init__(self, bus, peripheral_id):
        super().__init__(bus, peripheral_id)
        self.video_ram = [0x00 for i in range(VIDEO_WIDTH*VIDEO_HEIGHT)]

        self.reg_x = 0
        self.reg_y = 0
        self.reg_c = 0

        self.screen = pg.display.set_mode((VIDEO_WIDTH*DISPLAY_SCALE, VIDEO_HEIGHT*DISPLAY_SCALE), pg.DOUBLEBUF|pg.HWACCEL|pg.HWSURFACE)
        pg.display.set_caption("MLVM")
        pg.display.set_icon(pg.Surface((1,1)))

        self.surface = pg.Surface((VIDEO_WIDTH, VIDEO_HEIGHT))
        self.clock = pg.time.Clock()
    
    def set_pixel(self, x: int, y: int, c: int):
        self.video_ram[y*VIDEO_WIDTH + x] = c
        self.surface.set_at((self.reg_x, self.reg_y), byte_to_rgb(self.reg_c))
    
    def get_pixel(self, x: int, y: int):
        return self.video_ram[y*VIDEO_WIDTH + x]

    def fill(self, c: int):
        for i in range(len(self.video_ram)):
            self.video_ram[i] = c
        
        self.surface.fill(byte_to_rgb(c))

    def clock_neg(self):
        if self.bus.address in self.addr_range and self.bus.intent == WRITE:
            reg = self.unoffset_addr(self.bus.address)
            
            if reg == REG_X_POS:
                self.reg_x = self.bus.data % VIDEO_WIDTH

            elif reg == REG_Y_POS:
                self.reg_y = self.bus.data % VIDEO_HEIGHT

            elif reg == REG_COLOR:
                self.reg_c = self.bus.data
                self.set_pixel(self.reg_x, self.reg_y, self.reg_c)

            elif reg == REG_FLIP:
                pg.transform.scale_by(self.surface, DISPLAY_SCALE, self.screen)
                pg.display.flip()
                self.clock.tick(-1)
                pg.display.set_caption(f"MLVM FPS: {int(self.clock.get_fps())}")
            
            elif reg == REG_FILL:
                self.fill(self.bus.data)
        
        if self.bus.cycle % EVENT_CYCLE_INTERVAL == 0:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    exit()

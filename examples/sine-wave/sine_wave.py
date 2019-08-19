# Fun with sine waves

# VCC GND STM32F407ZGT6
from machine import Pin, SPI
spi = SPI(2)
spi.init(baudrate=2000000, polarity=0, phase=0)
cs = Pin('B12', Pin.OUT)
rst = Pin('B11', Pin.OUT)
bl = Pin('B1', Pin.OUT)
bl(1)

# with framebuffer
import hx1230_fb
lcd = hx1230_fb.HX1230_FB_SPI(spi, cs, rst)

import time
import math

def draw_sin(amplitude, freq, phase, yoffset=hx1230_fb.HEIGHT//2):
    for i in range(freq):
        y = int((math.sin((i + phase) * 0.017453) * amplitude) + yoffset)
        x = int((hx1230_fb.WIDTH / freq) * i)
        lcd.pixel(x, y, 1)
    lcd.show()

def draw_cos(amplitude, freq, phase, yoffset=hx1230_fb.HEIGHT//2):
    for i in range(freq):
        y = int((math.cos((i + phase) * 0.017453) * amplitude) + yoffset)
        x = int((hx1230_fb.WIDTH / freq) * i)
        lcd.pixel(x, y, 1)
    lcd.show()

# big wave
lcd.fill(0)
draw_sin(20, 360, 0)

# little wave
lcd.fill(0)
draw_sin(10, 5*360, 0)

# tiny wave
draw_sin(5, 10*360, 0)

# two waves
lcd.fill(0)
draw_sin(10, 4*360, 0, 12*1)
draw_cos(10, 4*360, 0, 12*3)

# three waves
lcd.fill(0)
draw_sin(20, 360, 0)
draw_sin(15, 2*360, 30)
draw_sin(10, 4*360, 60)

# lots of waves
lcd.fill(0)
for i in range(0,360,30):
    draw_sin(20, 360, i)

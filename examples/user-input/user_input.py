# Capture user input and print to lcd, character by character

# WeMos D1 Mini ESP8266
from machine import Pin, SPI, freq
spi = SPI(1)
spi.init(baudrate=4000000, polarity=0, phase=0)
cs = Pin(2)
rst = Pin(0)
bl = Pin(4, Pin.OUT, value=1)

# with framebuffer
import hx1230_fb
lcd = hx1230_fb.HX1230_FB_SPI(spi, cs, rst)

import sys

x = 0
y = 0
while True:
    chr = sys.stdin.read(1)
    if x == 0 and y == 0:
        lcd.clear()
    lcd.text(chr, x*8, y*8, 1)
    lcd.show()
    if x == 12:
        x = 0
        if y == 7:
            y = 0
        else:
            y += 1
    else:
        x = x + 1

# Based on MicroPython-ESP8266-Nokia-5110-Conways-Game-of-Life
# https://github.com/mcauser/MicroPython-ESP8266-Nokia-5110-Conways-Game-of-Life/blob/master/conways_game_of_life.py

# Both hardware SPI and bit-bang SPI are pretty slow with this write heavy example
# Examples using both below

# WeMos D1 Mini -- HX1230 LCD
# D3 (GPIO0) ----- 1 RST
# D4 (GPIO2) ----- 2 CE
# n/a ------------ 3 N/C
# D7 (GPIO13) ---- 4 DIN
# D5 (GPIO14) ---- 5 CLK
# 3V3 ------------ 6 VCC
# D2 (GPIO4) ----- 7 BL
# G -------------- 8 GND

# WeMos D1 Mini ESP8266
# Hardware SPI
from machine import Pin, SPI, freq
spi = SPI(1)
spi.init(baudrate=4000000, polarity=0, phase=0)
cs = Pin(2)
rst = Pin(0)
bl = Pin(4, Pin.OUT, value=1)

# with framebuffer
import hx1230_fb
lcd = hx1230_fb.HX1230_FB_SPI(spi, cs, rst)

# max speed
freq(160000000)

# play
from conways import ConwaysGameOfLife
game = ConwaysGameOfLife(lcd)
game.intro()

# 4x4 pixels, no delay (the refresh rate is pretty slow)
game.begin(4,0)


#######################################

# WeMos D1 Mini ESP8266
# Bit-bang SPI
from machine import Pin, freq
mosi = Pin(13, Pin.OUT)
sck = Pin(14, Pin.OUT)
cs = Pin(2)
rst = Pin(0)
bl = Pin(4, Pin.OUT, value=1)

# with framebuffer
import hx1230_fb
lcd = hx1230_fb.HX1230_FB_BBSPI(mosi, sck, cs, rst)

# max speed
freq(160000000)

# play
from conways import ConwaysGameOfLife
game = ConwaysGameOfLife(lcd)
game.intro()

# 4x4 pixels, no delay (the refresh rate is pretty slow)
game.begin(4,0)

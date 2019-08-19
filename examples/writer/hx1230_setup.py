# Demo using Peter Hinch's Writer class
# See https://github.com/peterhinch/micropython-font-to-py
from machine import Pin, SPI
from hx1230_fb import HX1230_FB_SPI, HX1230_FB_BBSPI, WIDTH, HEIGHT

# VCC GND STM32F407ZGT6
cs = Pin('B12', Pin.OUT)
rst = Pin('B11', Pin.OUT)
bl = Pin('B1', Pin.OUT)
bl(1)

def setup(hardware_spi=True):
    if hardware_spi:
        spi = SPI(2)
        spi.init(baudrate=2000000, polarity=0, phase=0)
        lcd = HX1230_FB_SPI(spi, cs, rst)
    else:
        mosi = Pin('B15', Pin.OUT)
        sck = Pin('B13', Pin.OUT)
        lcd = HX1230_FB_BBSPI(mosi, sck, cs, rst)
    return lcd

# Pins
# VCC GND ZGT6  | HX1230 LCD
# ------------- | ----------
# B11           | 1 RST
# B12 SPI2 CS   | 2 CE
# n/a           | 3 N/C
# B15 SPI2 MOSI | 4 DIN
# B13 SPI2 SCK  | 5 CLK
# 3V3           | 6 VCC
# B1            | 7 BL
# GND           | 8 GND

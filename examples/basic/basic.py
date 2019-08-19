# Basic functions of the display

# VCC GND STM32F407ZGT6
from machine import Pin, SPI
spi = SPI(2)
spi.init(baudrate=2000000, polarity=0, phase=0)
cs = Pin('B12', Pin.OUT)
rst = Pin('B11', Pin.OUT)
bl = Pin('B1', Pin.OUT, value=1)  # backlight on

# without framebuffer
import hx1230
lcd = hx1230.HX1230_SPI(spi, cs, rst)

# provide power to the display module
lcd.power(True)
lcd.power(False)

# set the contrast
lcd.contrast(0) # dim
lcd.contrast(16)
lcd.contrast(31) # dark

# invert pixels
lcd.invert(False)
lcd.invert(True)

# in test mode, all pixels are on
lcd.test(True)
lcd.test(False)

# disable the display output
# ram is not cleared
lcd.display(True)
lcd.display(False)

# fill the display with a colour
lcd.clear(1)
lcd.clear(0)

# draw a F
lcd.position(0,0)
lcd.data(255)
lcd.data(255)
lcd.data(27)
lcd.data(27)
lcd.data(27)

# flip and rotate
lcd.orientation(False,False) # normal
lcd.orientation(True,False)  # flip horizontal
lcd.orientation(False,True)  # flip vertical
lcd.orientation(True,True)   # flip vertical and horizontal - rotate 180 deg
lcd.orientation(False,False) # normal
lcd.clear()

# write pixels on the first page
lcd.position(0,0)
lcd.data(255)
lcd.position(8,0)
lcd.data(255)
lcd.position(16,0)
lcd.data(255)
# write pixels on the next page
lcd.position(4,1)
lcd.data(255)
lcd.position(12,1)
lcd.data(255)
lcd.position(20,1)
lcd.data(255)

# data is a column of 1x8 pixels, LSB at the top
lcd.clear()
lcd.data(1)
lcd.data(3)
lcd.data(7)
lcd.data(15)
lcd.data(31)
lcd.data(63)
lcd.data(127)
lcd.data(255)

# write some characters - same font as the framebuffer
font_0 = b'\x00>\x7fIE\x7f>'
font_1 = b'\x00@D\x7f\x7f@@'
font_2 = b'\x00bsQIOF'
font_3 = b'\x00"cII\x7f6'
font_4 = b'\x00\x18\x18\x14\x16\x7f\x7f'
font_5 = b"\x00'gEE}9"
font_6 = b'\x00>\x7fII{2'
font_7 = b'\x00\x03\x03y}\x07\x03'
font_8 = b'\x006\x7fII\x7f6'
font_9 = b'\x00&oII\x7f>'
lcd.clear()
lcd.position(0,0)
lcd.data(font_1)
lcd.position(8,1)
lcd.data(font_2)
lcd.position(16,2)
lcd.data(font_3)
lcd.position(24,3)
lcd.data(font_4)
lcd.position(32,4)
lcd.data(font_5)
lcd.position(40,5)
lcd.data(font_6)
lcd.position(48,6)
lcd.data(font_7)
lcd.position(56,7)
lcd.data(font_8)
lcd.position(64,8)
lcd.data(font_9)

# offset the display vertically by pushing the display up this many pixels
lcd.start_line(4)  # half of 1 at top
lcd.start_line(8)  # 2 at top
lcd.start_line(16) # 3 at top
lcd.start_line(56) # 8 at top
lcd.start_line(63) # half of 9 at top
lcd.start_line(0)  # 1 at top

# animation showing start line offset
from time import sleep_ms
for i in range(64):
    lcd.start_line(i)
    sleep_ms(100)
lcd.start_line(0)

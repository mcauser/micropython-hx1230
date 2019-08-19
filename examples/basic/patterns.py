# Basic patterns without the framebuffer

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

# vertical lines
lcd.position(0,0)
for i in range(4):
    lcd.data(255)
    lcd.data(0)

# checkers
for i in range(4):
    lcd.data(170)
    lcd.data(85)

# horizontal lines
for i in range(8):
    lcd.data(85)

# rect
lcd.data(255)
for i in range(6):
    lcd.data(129)
lcd.data(255)

# filled rect
for i in range(8):
    lcd.data(255)

# circle
lcd.clear()
lcd.data(b'<B\x81\x81\x81\x81B<')

# lots of vertical lines
lcd.clear()
for i in range(432):
    lcd.data([0xff,0x00])

# lots of horizontal lines
lcd.clear()
for i in range(864):
    lcd.data(0x55)

# slashes
lcd.clear()
bck = [73,146,292,73,146,292,73,146]
fwd = [292,146,73,292,146,73,292,146]
for i in range(108):
    lcd.data(bck if (i & 1) else fwd)

# circles
lcd.clear()
for i in range(108):
    lcd.data([60,66,129,129,129,129,66,60])

# squares - 12 across, 9 down
lcd.clear()
for i in range(108):
    lcd.data([255,129,129,129,129,129,129,255])

# triangles
lcd.clear()
for i in range(9):
    for j in range(12):
        for k in range(8):
            lcd.data(255 >> k)

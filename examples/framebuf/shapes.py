# Drawing shapes using the Framebuffer

# VCC GND STM32F407ZGT6
from machine import Pin, SPI
spi = SPI(2)
spi.init(baudrate=2000000, polarity=0, phase=0)
cs = Pin('B12', Pin.OUT)
rst = Pin('B11', Pin.OUT)
bl = Pin('B1', Pin.OUT, value=1)  # backlight on

# with framebuffer
import hx1230_fb
lcd = hx1230_fb.HX1230_FB_SPI(spi, cs, rst)

# 8x8 circles, repeated using blit
# ..####..
# .#....#.
# #......#
# #......#
# #......#
# #......#
# .#....#.
# ..####..
import framebuf
lcd.clear()
circle_buf = bytearray(8)
circle_fbuf = framebuf.FrameBuffer(circle_buf, 8, 8, framebuf.MONO_VLSB)
circle_fbuf.hline(2,0,4,1)
circle_fbuf.pixel(1,1,1)
circle_fbuf.pixel(6,1,1)
circle_fbuf.vline(0,2,4,1)
circle_fbuf.vline(7,2,4,1)
circle_fbuf.pixel(1,6,1)
circle_fbuf.pixel(6,6,1)
circle_fbuf.hline(2,7,4,1)
for x in range(12):
    for y in range(9):
        lcd.blit(circle_fbuf,x*8,y*8)
lcd.show()

# 8x8 squares
lcd.clear()
for x in range(12):
    for y in range(9):
        lcd.rect(x*8,y*8,8,8,1)
lcd.show()

# centered squares
lcd.clear()
for i in range(17):
    lcd.rect(2*i, 2*i, 95-(4*i), 67-(4*i), 1)
lcd.show()

# checker board
lcd.clear()
for a in range(5):
    for b in range(6):
        for c in range(2):
            lcd.fill_rect(c*8+16*b, a*16+8*c, 8, 8, 1)
lcd.show()

# triangles
lcd.clear()
w = lcd.width
h = lcd.height
lcd.line(w//2-1, 0, 0, h-1, 1)
lcd.line(w//2-1, 0, w-1, h-1, 1)
lcd.line(0, h-1, w-1, h-1, 1)
lcd.show()
lcd.line(w//2-1, h-1, 0, 0, 1)
lcd.line(w//2-1, h-1, w, 0, 1)
lcd.line(0, 0, w-1, 0, 1)
lcd.show()
lcd.line(0, 0, 0, h-1, 1)
lcd.line(w-1, 0, w-1, h-1, 1)
lcd.line(0, h//2-1, w-1, h//2-1, 1)
lcd.show()
lcd.line(w//4-1, 0, w//4-1, h-1, 1)
lcd.line(w//2-1, 0, w//2-1, h-1, 1)
lcd.line(w//4*3-1, 0, w//4*3-1, h-1, 1)
lcd.show()

# big x
lcd.fill(0)
lcd.line(0, 0, 95, 67, 1)
lcd.line(95, 0, 0, 67, 1)
lcd.show()

# hourglass lines
lcd.clear()
for i in range(0,96,4):
    lcd.line(0+i, 0, 95-i, 67, 1)
    lcd.show()

# random pixels
import urandom
lcd.clear()
for i in range(50):
    for j in range(50):
        x = urandom.randrange(96)
        y = urandom.randrange(68)
        lcd.pixel(x, y, 1)
    lcd.show()

# random lines
import urandom
lcd.clear()
for i in range(20):
    for j in range(20):
        x1 = urandom.randrange(96)
        y1 = urandom.randrange(68)
        x2 = urandom.randrange(96)
        y2 = urandom.randrange(68)
        lcd.line(x1, y1, x2, y2, 1)
    lcd.show()

# MicroPython logo 32x32 - see micropython_32x32.gif
lcd.clear()
x = (96-32)//2
y = (68-32)//2
lcd.fill_rect(x+0, y+0, 32, 32, 1)
lcd.fill_rect(x+2, y+2, 28, 28, 0)
lcd.vline(x+9, y+8, 22, 1)
lcd.vline(x+16, y+2, 22, 1)
lcd.vline(x+23, y+8, 22, 1)
lcd.fill_rect(x+26, y+24, 2, 4, 1)
lcd.show()

# MicroPython logo 48x48 - see micropython_48x48.gif
lcd.clear()
x = (96-48)//2
y = (68-48)//2
lcd.fill_rect(x+0, y+0, 48, 48, 1)
lcd.fill_rect(x+2, y+2, 44, 44, 0)
lcd.fill_rect(x+11, y+12, 2, 34, 1)
lcd.fill_rect(x+23, y+2, 2, 34, 1)
lcd.fill_rect(x+35, y+12, 2, 34, 1)
lcd.fill_rect(x+40, y+38, 3, 4, 1)
lcd.show()

# MicroPython logo 64x64 - see micropython_64x64.gif
lcd.clear()
x = (96-64)//2
y = (68-64)//2
lcd.fill_rect(x+0, y+0, 64, 64, 1)
lcd.fill_rect(x+2, y+2, 60, 60, 0)
lcd.fill_rect(x+15, y+15, 3, 47, 1)
lcd.fill_rect(x+30, y+2, 4, 47, 1)
lcd.fill_rect(x+46, y+15, 3, 47, 1)
lcd.fill_rect(x+54, y+50, 4, 7, 1)
lcd.show()

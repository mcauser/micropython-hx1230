# Smiley Screen Saver
# Move a bitmap around, bounce it off walls like an old screensaver

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

# smiley 15x15 col major msb first - see smiley.gif
import framebuf
smiley = bytearray(b'\xE0\x38\xE4\x22\xA2\xE1\xE1\x61\xE1\x21\xA2\xE2\xE4\x38\xE0\x03\x0C\x10\x21\x21\x41\x48\x48\x48\x49\x25\x21\x10\x0C\x03')
smiley_w = 15
smiley_h = 15
smiley_fbuf = framebuf.FrameBuffer(smiley, smiley_w, smiley_h, framebuf.MONO_VLSB)

# area the smiley can move in
bounds_w = lcd.width - smiley_w
bounds_h = lcd.height - smiley_h

# direction smiley is moving
move_x = 1
move_y = 1

# pause between displaying frames
from time import sleep_ms
pause = 100

# start position
x = 1
y = 1

def render():
    global x
    global y
    global move_x
    global move_y
    # Draw the bitmap
    lcd.fill(0)
    lcd.blit(smiley_fbuf, x, y, 0)
    lcd.show()

    sleep_ms(pause)

    # Move down right until hit bounds
    # Then flip increment to decrement to bounce off the wall
    x = x + move_x
    y = y + move_y
    if (x <= 0 or x >= bounds_w):
        move_x = -move_x
    if (y <= 0 or y >= bounds_h):
        move_y = -move_y

while(True):
    render()

# Drawing text using the Framebuffer

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

# Hello World!
lcd.fill(0)
lcd.text('Hello World!',0,0,1)
lcd.show()

# using the standard framebuffer monospace font
# there are 12 characters across, 8.5 down
lcd.fill(0)
lcd.text('123456789012', 0, 0, 1)
lcd.text('2',0,8,1)
lcd.text('3',0,8*2,1)
lcd.text('4',0,8*3,1)
lcd.text('5',0,8*4,1)
lcd.text('6',0,8*5,1)
lcd.text('7',0,8*6,1)
lcd.text('8',0,8*7,1)
lcd.text('9',0,8*8,1)
lcd.show()

# 96 chars in total (excluding the bottom row)
lcd.fill(0)
for i in range(8):
    lcd.text('123456789012', 0, 8*i, 1)
lcd.show()

# 62% larger than the Nokia 5110 LCD
lcd.fill_rect(84,0,95,67,1)
lcd.fill_rect(0,48,95,48,1)
lcd.show()

# centered text
# set the x offset to (96 - (len(text) * 8)) / 2
# i set the line height here to 12 for readability
lcd.fill(0)
lcd.show()
lcd.text('MicroPython',4,0,1)
lcd.text('HX1230',24,12,1)
lcd.text('96x68',28,24,1)
lcd.text('Mono LCD',16,36,1)
lcd.text('9-bit SPI',12,48,1)
lcd.text('Framebuffer',4,60,1)
lcd.show()

# Show a bitmap of the Google dinosaur

# WeMos D1 Mini ESP8266
# Hardware SPI
from machine import Pin, SPI, freq
spi = SPI(1)
spi.init(baudrate=4000000, polarity=0, phase=0)
cs = Pin(2)
rst = Pin(0)
bl = Pin(4, Pin.OUT, value=1)

# with framebuffer
import hx1230
lcd = hx1230.HX1230_SPI(spi, cs, rst)

# draw the Google dinosaur
lcd.data(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
lcd.data(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xC0\xC0\xF0\xF0\x70\x70\xF0\xF0\xF0\xF0\xF0\xF0\xF0\xF0\xF0\xF0\xF0\xF0\xC0\xC0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
lcd.data(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xFF\xFF\xFF\xFF\xFE\xFE\xFF\xFF\xFF\xFF\x7F\x7F\x7F\x7F\x7F\x7F\x7F\x7F\x7F\x7F\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x80\x80\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
lcd.data(b'\x00\x00\x00\x00\x00\x00\xF8\xF8\x80\x80\x00\x00\x00\x00\x00\x00\x00\x00\x80\x80\x80\xE0\xE0\xE0\xF8\xF8\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\x87\x87\x86\x86\x06\x06\x06\x06\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x80\x00\x00\x00\xFF\xFF\xFF\xFF\xFF\x00\x00\xF0\xF8\xF0\x00\x00\x00\x00\x00\x00')
lcd.data(b'\x00\x00\x00\x00\x00\x00\x7F\x7F\xFF\xFF\xFE\xFE\xF8\xF8\xF8\xF8\xFE\xFE\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\x01\x01\x07\x07\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xFF\xFF\xFF\x00\x00\xFF\xFF\xFF\xFF\xFF\xC0\xC0\xFF\xFF\x7F\x00\x00\x00\x00\x00\x00')
lcd.data(b'\x00\x00\x00\x00\x00\x00\x00\x00\x01\x01\x07\x07\x1F\x1F\x7F\x7F\xFF\xFF\xFF\xFF\xFF\xFF\x7F\x7F\x7F\x7F\xFF\xFF\x9F\x9F\x87\x07\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x07\x0F\x1F\x1C\x1C\xFF\xFF\xFF\xFF\xFF\x01\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00')
lcd.data(b'\x01\x01\x01\x01\x01\x01\x01\x01\x41\x41\x01\x01\x00\x00\x00\x00\x7F\x7F\x67\x67\x01\x01\x00\x00\x00\x00\x01\x01\x01\x01\x01\x00\x00\x00\x00\x21\x01\x01\x01\x01\x01\x11\x11\x11\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x11\x01\x01\x01\x01\x41\x41\x41\x41\x01\x01\x01\x01\x01\x01\x00\xFF\xFF\xFF\xFF\xFF\x00\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01')
lcd.data(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
lcd.data(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')

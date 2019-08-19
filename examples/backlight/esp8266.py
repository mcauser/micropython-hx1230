# ESP8266 Backlight Example

from machine import Pin, SPI
spi = SPI(1)
spi.init(baudrate=2000000, polarity=0, phase=0)
cs = Pin(2)
rst = Pin(0)

import hx1230
lcd = hx1230.HX1230_SPI(spi, cs, rst)

# draw a triangle pattern
for i in range(108):
    lcd.data([255,127,63,31,15,7,3,1])

# backlight on
bl = Pin(4, Pin.OUT, value=1)

# backlight off
bl(0)

# PWM dimming
# on the ESP8266 port there is a machine.PWM
from machine import PWM

# off
bl_pwm = PWM(bl, freq=500, duty=0)

# dim
bl_pwm = PWM(bl, freq=500, duty=512)

# bright
bl_pwm = PWM(bl, freq=500, duty=1024)

# return to logic level output
bl_pwm.deinit()
bl.mode(b1.OUT)
bl(0)
bl(1)

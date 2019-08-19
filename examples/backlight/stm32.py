# STM32 Backlight Example

from machine import Pin, SPI
spi = SPI(2)
spi.init(baudrate=2000000, polarity=0, phase=0)
cs = Pin('B12', Pin.OUT)
rst = Pin('B11', Pin.OUT)

import hx1230
lcd = hx1230.HX1230_SPI(spi, cs, rst)

# draw a triangle pattern
for i in range(108):
	lcd.data([255,127,63,31,15,7,3,1])

# backlight on
bl = Pin('B1', Pin.OUT, value=1)

# backlight off
bl(0)

# PWM dimming
# On the VCC GND STM32F407VGT6 board, Pin B1 has a few timer alternate functions:
# https://github.com/mcauser/VCC_GND_F407ZG/blob/master/docs/STM32F4-AF-mapping.pdf
# Timer 1, Channel 3
# Timer 3, Channel 4
# Timer 8, Channel 3

# This port does not have a machine.PWM, so revert to using pyb
import pyb

# blink at 2Hz, timer 1, channel 3
tim = pyb.Timer(1, freq=2)
ch = tim.channel(3, pyb.Timer.PWM, pin=bl)
ch.pulse_width_percent(50)

# faster blink 8Hz, timer 3, channel 4
tim = pyb.Timer(3, freq=8)
ch = tim.channel(4, pyb.Timer.PWM, pin=bl)
ch.pulse_width_percent(50)

# bright, no flicker 1000Hz
tim = pyb.Timer(8, freq=1000)
ch = tim.channel(3, pyb.Timer.PWM, pin=bl, pulse_width_percent=10)

# dim, no flicker 1000Hz
tim = pyb.Timer(8, freq=1000)
ch = tim.channel(3, pyb.Timer.PWM, pin=bl, pulse_width_percent=90)

# return to logic level output
tim.deinit()
bl.init(mode=Pin.OUT)
bl(0)
bl(1)

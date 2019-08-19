# Based on MicroPython-ESP8266-Nokia-5110-Bitcoin
# https://github.com/mcauser/MicroPython-ESP8266-Nokia-5110-Bitcoin/blob/master/bitcoin_ticker_test.py

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
from machine import Pin, SPI
spi = SPI(1)
spi.init(baudrate=2000000, polarity=0, phase=0)
cs = Pin(2)
rst = Pin(0)
bl = Pin(4, Pin.OUT, value=1)

# with framebuffer
import hx1230_fb
lcd = hx1230_fb.HX1230_FB_SPI(spi, cs, rst)

# setup wifi
import network

def connect_to_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        lcd.text('Connecting',0,0,1)
        lcd.show()
        wlan.connect('ssid','pass')
        while not wlan.isconnected():
            pass
    lcd.clear()
    lcd.text('Connected',0,0,1)
    lcd.text(wlan.ifconfig()[0],0,10,1)
    lcd.show()

connect_to_wifi()

# if you dont have urequests
# import upip
# upip.install('micropython-urequests')

import time
from bitcoin_ticker import BitcoinTicker

ticker = BitcoinTicker(lcd)

# new price displayed every 96 seconds
# the bottom 2 rows of pixels is a progress bar, incremented once per second
ticker.refresh()

# get new price immediately
# ticker.update()

# you can draw your own value using:
# ticker.draw("99999")
# ticker.draw("9999")
# ticker.draw("123")
# ticker.draw("44")
# ticker.draw("2")

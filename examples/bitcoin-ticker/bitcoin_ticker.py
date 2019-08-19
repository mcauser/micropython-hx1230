# Based on MicroPython-ESP8266-Nokia-5110-Bitcoin
# https://github.com/mcauser/MicroPython-ESP8266-Nokia-5110-Bitcoin/blob/master/bitcoin_ticker.py

from micropython import const

from framebuf import FrameBuffer, MONO_VLSB
from time import sleep
import urequests

SPACE = const(2)    # between characters
YPOS = const(22)    # roughly (lcd height - font height - progress bar height) / 2

# bitcoin symbol (2px taller than the other chars)
btc = FrameBuffer(bytearray(b'\x18\x18\xf8\xf8\xff\xff\x18\x1f\x1f8x\xf8\xf0\xe0\x00\x00\x00\xff\xff\xff\xff\x06\x06\x06\x06\x8f\xdf\xff\xfd\xf8\x03\x03\x03\x03\x1f\x1f\x03\x1f\x1f\x03\x03\x03\x03\x01\x00'), 15, 21, MONO_VLSB)

# digits (0-9, variable width)
b0 = FrameBuffer(bytearray(b'\xc0\xf0\xfc<\x0e\x07\x07\x07\x07\x0f\x1e>\xfc\xf0\xc0\x1f\x7f\xff\xe0\xc0\x80\x00\x00\x00\x00\x80\xe0\xff\x7f\x1f\x00\x00\x01\x03\x03\x07\x07\x07\x07\x07\x03\x01\x01\x00\x00'), 15, 19, MONO_VLSB)
b1 = FrameBuffer(bytearray(b'\x04\x0e\x0e\x0e\xff\xff\xff\x00\x00\x00\x00\xff\xff\xff\x00\x00\x00\x00\x07\x07\x07'), 7, 19, MONO_VLSB)
b2 = FrameBuffer(bytearray(b'\x00\x18<\x1e\x0e\x07\x07\x07\x07\x0f\xfe\xfc\xf8\x00\x80\x80\xc0\xe0\xf0x<\x1e\x0f\x07\x03\x00\x07\x07\x07\x07\x07\x07\x07\x07\x07\x07\x07\x07\x07'), 13, 19, MONO_VLSB)
b3 = FrameBuffer(bytearray(b'\x00\x07\x07\x07\x07\xc7\xe7\xf7\x7f?\x1f\x0f\x07\x80\xc0\xc0\x80\x03\x03\x03\x03\x07\x8f\xfe\xfe\xf8\x00\x01\x03\x03\x07\x07\x07\x07\x07\x03\x03\x01\x00'), 13, 19, MONO_VLSB)
b4 = FrameBuffer(bytearray(b'\x00\x00\x00\x00\x80\xc0\xe0\xf0|\x1e\xff\xff\xff\x00\x00\x00\x10x|\x7f\x7fsqppp\xff\xff\xffppp\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x07\x07\x07\x00\x00\x00'), 16, 19, MONO_VLSB)
b5 = FrameBuffer(bytearray(b'\x00\xff\xff\xff\x87\x87\x87\x87\x87\x07\x07\x07\x00\x80\xc3\x87\x83\x03\x03\x03\x03\x03\x87\xff\xfe|\x01\x03\x03\x07\x07\x07\x07\x07\x07\x03\x03\x01\x00'), 13, 19, MONO_VLSB)
b6 = FrameBuffer(bytearray(b'\xc0\xf0\xfc>\x0e\x87\x87\x87\x87\x0f\x1e\x06\x00?\xff\xff\x87\x03\x03\x03\x03\x03\x87\xff\xfex\x00\x00\x01\x03\x07\x07\x07\x07\x07\x03\x03\x01\x00'), 13, 19, MONO_VLSB)
b7 = FrameBuffer(bytearray(b'\x07\x07\x07\x07\x07\x07\x07\xc7\xf7\xff\x7f\x1f\x07\x00\x00\x00\xc0\xf0\xfc\x7f\x1f\x07\x01\x00\x00\x00\x00\x04\x07\x07\x07\x01\x00\x00\x00\x00\x00\x00\x00'), 13, 19, MONO_VLSB)
b8 = FrameBuffer(bytearray(b'\x00x\xfc\xfe\x8f\x07\x07\x07\x07\x8f\xfe\xfcx\x00\xf0\xf8\xfc\x8f\x0f\x07\x07\x07\x07\x0f\x8f\xfd\xf8\xf0\x00\x01\x03\x03\x07\x07\x07\x07\x07\x07\x03\x03\x01\x00'), 14, 19, MONO_VLSB)
b9 = FrameBuffer(bytearray(b'\xf0\xfc\xfe\x0e\x07\x07\x07\x07\x0f\x1e\xfc\xf8\xe0\x01\x87\x8f\x0f\x1e\x1c\x1c\x1c\x8e\xc7\xff\x7f\x1f\x01\x03\x03\x07\x07\x07\x07\x07\x03\x03\x01\x00\x00'), 13, 19, MONO_VLSB)

# characters (0-9, btc symbol)
characters = [b0,b1,b2,b3,b4,b5,b6,b7,b8,b9,btc]

# character widths (0-9, btc symbol)
widths = [15,7,13,13,16,13,13,13,14,13,15]

class BitcoinTicker:
    def __init__(self, lcd):
        self.lcd = lcd

    def refresh(self):
        while(True):
            # display results
            self.update()
            sleep(1)

            # increment progress bar
            for i in range(1,self.lcd.width,1):
                self.lcd.fill_rect(0,self.lcd.height-2,i,2,1)
                self.lcd.show()
                sleep(1)

    def update(self):
        try:
            # change AUD to the currency of your choice
            r = urequests.get("http://api.coindesk.com/v1/bpi/currentprice/AUD.json")
            # change this AUD too
            rate = '%d' % r.json()['bpi']['AUD']['rate_float']
            # it's mandatory to close response objects as soon as you finished working with them.
            r.close()
        except KeyError:
            rate = "0"
        self.draw(rate)

    def draw(self, string):
        # clear
        self.lcd.clear()

        # figure out bounding box
        xpos = widths[10] + SPACE
        for c in string:
            i = int(c)
            xpos += widths[i] + SPACE
        xpos = (self.lcd.width - xpos) // 2

        # draw symbol
        self.lcd.blit(btc, xpos, YPOS - 1)
        xpos += widths[10] + SPACE

        # draw each digit
        for c in string:
            i = int(c)
            self.lcd.blit(characters[i], xpos, YPOS)
            xpos += widths[i] + SPACE

        self.lcd.show()

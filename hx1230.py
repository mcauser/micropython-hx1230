"""
MicroPython HX1230 96x68 LCD driver
https://github.com/mcauser/micropython-hx1230

MIT License
Copyright (c) 2019 Mike Causer

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from micropython import const
from ustruct import pack
from utime import sleep_us

POWER_ON         = const(0x2F) # internal power supply on
POWER_OFF        = const(0x28) # internal power supply off

CONTRAST         = const(0x80) # 0x80 + (0~31)

SEG_NORMAL       = const(0xA0) # SEG remap normal
SEG_REMAP        = const(0xA1) # SEG remap reverse (flip horizontal)

DISPLAY_NORMAL   = const(0xA4) # display ram contents
DISPLAY_TEST     = const(0xA5) # all pixels on

INVERT_OFF       = const(0xA6) # not inverted
INVERT_ON        = const(0xA7) # inverted

DISPLAY_ON       = const(0XAF) # display on
DISPLAY_OFF      = const(0XAE) # display off

SCAN_START_LINE  = const(0x40) # 0x40 + (0~63)

COM_NORMAL       = const(0xC0) # COM remap normal
COM_REMAP        = const(0xC8) # COM remap reverse (flip vertical)

SW_RESET         = const(0xE2) # connect RST pin to GND to rely on software reset
#NOP              = const(0xE3) # no operation

DATA             = const(0x80) # the msb in the 9-bit spi mode, command = 0, data = 1

THREE_BITS       = const(0x07) # 0~7
FOUR_BIS         = const(0x0f) # 0~15
FIVE_BITS        = const(0x1f) # 0~31
SIX_BITS         = const(0x3f) # 0~63

# DDRAM addresses
COL_ADDR         = const(0x10) # x pos (0~95)
PAGE_ADDR        = const(0xB0) # y pos, 9 pages of 8 rows (0~8)

# Display dimensions
WIDTH            = const(0x60) # 96 cols
HEIGHT           = const(0x44) # 68 rows
PAGES            = const(9)    # 9 pages (68 / 8 = 8.5, rounded up to 9) the last page is only half visible

class HX1230:
    def __init__(self, cs, rst=None):
        self.cs     = cs   # chip enable, active LOW
        self.rst    = rst  # reset, active LOW

        self.height = HEIGHT
        self.width = WIDTH

        self.cs.init(self.cs.OUT, value=1)

        if self.rst:
            self.rst.init(self.rst.OUT, value=1)

        self.init()

    def init(self, contrast=15, seg_remap=False, com_remap=False, start=0):
        self.reset()
        self.power(True)
        self.contrast(contrast)
        self.invert(False)
        self.test(False)
        self.orientation(seg_remap, com_remap)
        self.display(True)
        self.start_line(start)
        self.clear()

    def reset(self, software=False):
        if software is False and self.rst:
            self.rst(0)
            sleep_us(50)  # recommended between 10 and 100 ms
            self.rst(1)
        else:
            self.command(SW_RESET)
        sleep_us(100)

    def power(self, on=True):
        self.command(POWER_ON if on else POWER_OFF)
        # when powering off, fill memory with zeros to save power

    def contrast(self, contrast=15):
        # contrast (0~31)
        self.command(CONTRAST | (contrast & FIVE_BITS))

    def invert(self, invert=True):
        self.command(INVERT_ON if invert else INVERT_OFF)

    def display(self, on=True):
        self.command(DISPLAY_ON if on else DISPLAY_OFF)

    def test(self, on=True):
        self.command(DISPLAY_TEST if on else DISPLAY_NORMAL)

    def orientation(self, seg_remap=False, com_remap=False):
        # for rotate 180, set both to True
        self.command(SEG_REMAP if seg_remap else SEG_NORMAL)
        self.command(COM_REMAP if com_remap else COM_NORMAL)

    def position(self, x, y):
        # set cursor to column x (0~95), page y (0~9)
        self.command(PAGE_ADDR | y)                       # set y pos (0~8)
        self.command(COL_ADDR | ((x >> 4) & THREE_BITS))  # set x pos high 3 bits
        self.command(x & FOUR_BIS)                        # set x pos low 4 bits

    def start_line(self, line=0):
        # line (0~63)
        self.command(SCAN_START_LINE + (line & SIX_BITS))

    def clear(self, color=0):
        for i in range(WIDTH * PAGES):
            self.data(color)
        self.position(0, 0)

    def command(self, command):
        self.hal_spi_write(0, command)

    def data(self, data):
        if isinstance(data, int):
            self.hal_spi_write(1, data)
        else:
            for b in data:
                self.hal_spi_write(1, b)

    def hal_spi_write(self, dc, value):
        """Writes to the LCD.
        It is expected that a derived HAL class will implement this function.
        """
        raise NotImplementedError


class HX1230_SPI(HX1230):
    """Implements a HX1230 using 16-bit SPI
    Bits are sent MSB first. DC is the MSB, followed by 8 bits of data.
    Remaining 7 bits are zeros and ignored by the display.
    """
    def __init__(self, spi, cs, rst=None):
        self.spi = spi           # max serial rate 4 MBit/s
        self.cmd = bytearray(2)  # 9-bit SPI, MSB = D/C, 8 data bits, 7 padding bits
        super().__init__(cs, rst)

    def hal_spi_write(self, dc, value):
        self.cs(0)
        self.cmd[0] = DATA if dc else 0    # MSB is D/C
        self.cmd[0] |= (value >> 1)        # high 7 bits of value
        self.cmd[1] = ((value & 1) << 7)   # low 1 bit of value
        self.spi.write(self.cmd)
        self.cs(1)


class HX1230_BBSPI(HX1230):
    """Implements a HX1230 using bit-bang 9-bit SPI"""
    def __init__(self, mosi, sck, cs, rst=None):
        self.mosi = mosi
        self.sck = sck
        self.mosi.init(self.mosi.OUT)
        self.sck.init(self.sck.OUT)
        super().__init__(cs, rst)

    def hal_spi_write(self, dc, value):
        self.cs(0)
        self.mosi(dc)  # MSB is D/C
        self.sck(1)
        self.sck(0)
        # 8 data bits sent MSB first
        for i in range(7, -1, -1):
            self.mosi((value >> i) & 1)
            self.sck(1)
            self.sck(0)
        self.cs(1)

# Draw a smiley without the framebuffer

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

# smiley 15x15 col major msb first - see smiley.gif
# .....#####......
# ...##.....##....
# ..#.........#...
# .#...........#..
# .#...........#..
# ###############.
# #.#..####..##.#.
# #.#.###.#.###.#.
# #..###...###..#.
# #.............#.
# .#........#..#..
# .#....####...#..
# ..#.........#...
# ...##.....##....
# .....#####......
# ................
# 0xE0, 0x38, 0xE4, 0x22, 0xA2, 0xE1, 0xE1, 0x61, 0xE1, 0x21, 0xA2, 0xE2, 0xE4, 0x38, 0xE0, 0x00
# 0x03, 0x0C, 0x10, 0x21, 0x21, 0x41, 0x48, 0x48, 0x48, 0x49, 0x25, 0x21, 0x10, 0x0C, 0x03, 0x00

# page 0
lcd.position(0, 0)
lcd.data(bytearray(b'\xE0\x38\xE4\x22\xA2\xE1\xE1\x61\xE1\x21\xA2\xE2\xE4\x38\xE0\x00'))

# page 1
lcd.position(0, 1)
lcd.data(bytearray(b'\x03\x0C\x10\x21\x21\x41\x48\x48\x48\x49\x25\x21\x10\x0C\x03\x00'))

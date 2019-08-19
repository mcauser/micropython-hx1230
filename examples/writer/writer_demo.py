# Demo using Peter Hinch's Writer class
# See https://github.com/peterhinch/micropython-font-to-py
from hx1230_setup import WIDTH, HEIGHT, setup
from writer import Writer

# Font
import font10

def test():
    lcd = setup(True)
    rhs = WIDTH -1
    lcd.line(rhs - 20, 0, rhs, 20, 1)
    square_side = 10
    lcd.fill_rect(rhs - square_side, 0, square_side, square_side, 1)

    wri = Writer(lcd, font10)
    Writer.set_textpos(lcd, 0, 0)  # verbose = False to suppress console output
    wri.printstring('Tuesday\n')
    wri.printstring('20 Aug 2019\n')
    wri.printstring('10.30pm')
    lcd.show()

print('Test assumes a 96*68 (w*h) HX1230 display.')
print('Issue:')
print('writer_demo.test(True) for a SPI connected device.')
print('writer_demo.test(False) for a bit-bang SPI connected device.')

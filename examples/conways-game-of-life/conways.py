# Based on MicroPython-ESP8266-Nokia-5110-Conways-Game-of-Life
# https://github.com/mcauser/MicroPython-ESP8266-Nokia-5110-Conways-Game-of-Life/blob/master/conways_game_of_life.py

from time import sleep_ms
from urandom import getrandbits

class ConwaysGameOfLife:
    def __init__(self, lcd):
        # High score
        self.best = 0
        # HX1230 LCD with framebuffer support
        self.lcd = lcd
        self.width = self.lcd.width
        self.height = self.lcd.height

    def intro(self):
        self.lcd.fill(0)
        self.lcd.text("Conway's", 16, 16, 1)
        self.lcd.text("Game", 32, 24, 1)
        self.lcd.text("of", 40, 32, 1)
        self.lcd.text("Life", 32, 40, 1)
        self.lcd.show()

    def end(self, score, best, size):
        # The 8x8 font is too wide to fit "Generations", so I called it "Score"
        self.lcd.fill(0)
        self.lcd.text("Score", 0, 4, 1)
        self.lcd.text(str(score), 0, 12, 1)
        self.lcd.text("Best score", 0, 24, 1)
        self.lcd.text(str(best), 0, 32, 1)
        self.lcd.text("Pixel size", 0, 44, 1)
        self.lcd.text(str(size), 0, 52, 1)
        self.lcd.show()

    def begin(self, size=4, delay=20):
        # Size of lifeforms in pixels
        self.size = size

        # Randomise initial pixels
        self.randomise()

        # Begin
        generations = 0
        try:
            while self.tick():
                generations = generations + 1
                self.lcd.show()
                if delay:
                    sleep_ms(delay)
        except KeyboardInterrupt:
            pass

        # New high score?
        if generations > self.best:
            self.best = generations

        # End
        self.end(generations, self.best, self.size)

    def randomise(self):
        self.lcd.fill(0)

        for x in range(0, self.width, self.size):
            for y in range(0, self.height, self.size):
                # random bit: 0 = pixel off, 1 = pixel on
                self.cell(x, y, getrandbits(1))

        self.lcd.show()

    def cell(self, x, y, colour):
        for i in range(self.size):
            for j in range(self.size):
                self.lcd.pixel(x + i, y + j, colour)

    def get(self, x, y):
        if not 0 <= x < self.width or not 0 <= y < self.height:
            return 0
        return self.lcd.pixel(x, y) & 1

    def tick(self):
        size = self.size
        get = self.get
        cell = self.cell

        # If no pixels are born or die, the game ends
        something_happened = False

        for x in range(0, self.width, size):
            for y in range(0, self.height, size):

                # Is the current cell alive
                alive = get(x, y)

                # Count number of neighbours
                neighbours = (
                    get(x - size, y - size) +
                    get(x, y - size) +
                    get(x + size, y - size) +
                    get(x - size, y) +
                    get(x + size, y) +
                    get(x + size, y + size) +
                    get(x, y + size) +
                    get(x - size, y + size)
                )

                # Apply the game rules
                if alive and not 2 <= neighbours <= 3:
                    # This pixel dies
                    cell(x, y, 0)
                    if not something_happened:
                        something_happened = True
                elif not alive and neighbours == 3:
                    # A new pixel is born
                    cell(x, y, 1)
                    if not something_happened:
                        something_happened = True

        return something_happened

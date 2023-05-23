from pyglet.window import Window
from pyglet.app import run
from pyglet.text import Label
from pyglet import font
from pyglet import clock
from pyglet.shapes import Line

class Renderer(Window):
    def __init__(self, game):
        self.game = game
        super().__init__()
        font.add_file("joystix monospace.otf")
        font.load("Joystix", 16)
        self.laser_x = self.width / 5
        self.laser = Line(self.laser_x, 0, self.laser_x, self.height, color=(214, 93, 177, 255))

    def start(self):
        self.game.new_round()
        self.characters = []
        x = self.width
        y = self.height / 2
        for t in self.game.word:
            self.characters.append(Label(t, font_size=24, x=x, y=y, font_name="Joystix", anchor_x="center", color=(255, 199, 95, 255)))
            x = x + 32

    def on_draw(self):
        self.clear()
        self.laser.draw()
        for c in self.characters:
            c.draw()

    def on_update(self, dt):
        for c in self.characters:
            c.x -= 100 * dt
        if self.characters[0].x < self.laser_x + 12:  # +12 for left alignment of the character
            self.start()

    def on_key_press(self, symbol, modifiers):
        key = chr(symbol).upper()
        if self.game.check_key(key):
            if self.game.word:
                self.characters = self.characters[1:]
            else:  # word complete
                self.start()

class Game:
    def __init__(self):
        self.words = ["SONNE", "MOND", "STERNE", "KOMET", "VENUS", "RAKETE", "STRAHLUNG", "ALIENS", "MILCHSTRASSE", "DISTANZ"]

    def new_round(self):
        self.word = self.words[0]

    def check_key(self, character):
        if character == self.word[0]:
            self.word = self.word[1:]
            return True
        return False

game = Game()
renderer = Renderer(game)
renderer.start()
clock.schedule(renderer.on_update)
run()

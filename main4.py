from pyglet.window import Window
from pyglet.app import run
from pyglet.text import Label
from pyglet import font
from pyglet import clock
from pyglet.shapes import Line
from pyglet.shapes import Rectangle
import random
import math

class Confetti:
    def __init__(self, x, y):
        self.confetti = [
            Rectangle(x, y, 10, 10, color=(132, 94, 194, 255)),
            Rectangle(x, y, 10, 10, color=(214, 93, 177, 255)),
            Rectangle(x, y, 10, 10, color=(255, 150, 113, 255)),
            Rectangle(x, y, 10, 10, color=(249, 248, 113, 255)),
        ]
        self.y = y + 50
        self.animation_time = -2
        self.directions_x = [random.random() * -10 for _ in self.confetti]
        self.speeds = [random.random() * 2 + 2 for _ in self.confetti]
    
    def draw(self):
        for c in self.confetti:
            c.draw()
            
    def update(self, dt):
        self.animation_time += dt * 20
        for c, d, s in zip(self.confetti, self.directions_x, self.speeds):
            c.y = self.y - self.animation_time ** 2 * s
            c.x += d * dt * 10

class Renderer(Window):
    def __init__(self, game):
        self.game = game
        super().__init__()
        font.add_file("joystix monospace.otf")
        font.load("Joystix", 16)
        self.laser_x = self.width / 5
        self.laser = Line(self.laser_x, 0, self.laser_x, self.height, color=(214, 93, 177, 255))
        self.shake_animation_time = 0
        
    def start(self):
        self.game.new_round()
        self.characters = []
        self.confetti = []
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
        for c in self.confetti:
            c.draw()
            
    def on_update(self, dt):
        for c in self.characters:
            c.x -= 100 * dt
        if self.characters[0].x < self.laser_x + 12:  # +12 for left alignment of the character
            self.start()
        for c in self.confetti:
            c.update(dt)
        if self.shake_animation_time > 0:
            self.shake_animation_time -= dt
            self.characters[0].rotation = math.sin(self.shake_animation_time * 50) * 20
        else:
            self.characters[0].rotation = 0
            
    def on_key_press(self, symbol, modifiers):
        key = chr(symbol).upper()
        if self.game.check_key(key):
            character = self.characters[0]
            if self.game.word:
                self.characters = self.characters[1:]
            else:  # word complete
                self.start()
            self.confetti.append(Confetti(character.x, character.y))
        else:
            self.shake_animation_time = .3  # 300 ms
            
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

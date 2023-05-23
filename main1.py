from pyglet.window import Window
from pyglet.app import run
from pyglet.text import Label
from pyglet import font

class Renderer(Window):
    def __init__(self):
        super().__init__()
        font.add_file("joystix monospace.otf")
        font.load("Joystix", 16)
        
    def start(self):
        self.characters = []
        x = self.width / 2
        y = self.height / 2
        for t in "ALIENS":
            self.characters.append(Label(t, font_size=24, x=x, y=y, font_name="Joystix", anchor_x="center", color=(255, 199, 95, 255)))
            x = x + 32
        
    def on_draw(self):
        self.clear()
        for c in self.characters:
            c.draw()

renderer = Renderer()
renderer.start()
run()
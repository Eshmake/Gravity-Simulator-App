from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse, Rectangle
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.core.image import Image as CoreImage
import math

WIDTH, HEIGHT = 800, 600

PLANET_MASSES = {
    "sun": 5238000,
    "jupiter": 5000,
    "saturn": 1495,
    "uranus": 229,
    "neptune": 270,
    "earth": 15.75,
    "venus": 12.8,
    "mars": 1.69,
    "mercury": 0.87,
    "moon": 0.19
}

PLANET_MASS = PLANET_MASSES["jupiter"]
SHIP_MASS = 5
G = 0.8
FPS = 60
PLANET_SIZE = 50
OBJ_SIZE = 5
VEL_SCALE = 40

"""
PLANET_MASS = 100
SHIP_MASS = 5
G = 5
FPS = 60
PLANET_SIZE = 50
OBJ_SIZE = 5
VEL_SCALE = 100
"""

Window.size = (WIDTH, HEIGHT)  # Optional for desktop preview

class Planet:
    def __init__(self, x, y, mass, radius, color=(0, 0, 1)):
        self.pos = [x, y]
        self.mass = mass
        self.radius = radius
        self.color = color

class Spaceship:
    def __init__(self, x, y, vx, vy, mass, radius, color=(1, 0, 0)):
        self.pos = [x, y]
        self.vel = [vx, vy]
        self.mass = mass
        self.radius = radius
        self.color = color

class GravitySimWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.planet = Planet(HEIGHT, WIDTH, mass=PLANET_MASS, radius=PLANET_SIZE)
        self.ship = None  # Start with no ship
        self.drag_start = None
        self.drag_line = None

        Clock.schedule_interval(self.update, 1.0 / 60.0)

    def on_touch_down(self, touch):
        self.drag_start = touch.pos
        return True

    def on_touch_move(self, touch):
        self.draw()  # Redraw planet
        with self.canvas:
            from kivy.graphics import Line, Color
            Color(1, 1, 1)
            self.drag_line = Line(points=[*self.drag_start, touch.x, touch.y], width=2)

    def on_touch_up(self, touch):
        if self.drag_start:
            dx = self.drag_start[0] - touch.x
            dy = self.drag_start[1] - touch.y
            vx = dx * 0.05  # scale down velocity
            vy = dy * 0.05
            self.ship = Spaceship(*self.drag_start, vx, vy, mass=1, radius=8)
            self.drag_start = None
            self.drag_line = None

    def update(self, dt):
        if not self.ship:
            self.draw()
            return
        
        offScreen = self.ship.pos[0] < 0 or self.ship.pos[0] > WIDTH or self.ship.pos[1] < 0 or self.ship.pos[1] > HEIGHT

        collided = math.sqrt((self.ship.pos[0] - self.planet.pos[0])**2 + (self.ship.pos[1] - self.planet.pos[1])**2) < PLANET_SIZE

        if offScreen or collided:
            self.ship = None
            self.draw()
            return

        # Gravity calculation
        dx = self.planet.pos[0] - self.ship.pos[0]
        dy = self.planet.pos[1] - self.ship.pos[1]
        dist = math.hypot(dx, dy)
        if dist == 0:
            return
        force = (G * self.planet.mass * self.ship.mass) / (dist ** 2)
        angle = math.atan2(dy, dx)
        fx = math.cos(angle) * force
        fy = math.sin(angle) * force

        self.ship.vel[0] += fx / self.ship.mass
        self.ship.vel[1] += fy / self.ship.mass
        self.ship.pos[0] += self.ship.vel[0]
        self.ship.pos[1] += self.ship.vel[1]

        self.draw()

    def draw(self):
        self.canvas.clear()
        with self.canvas:
            # Draw planet
            texture = CoreImage("images/jupiter.png").texture
            Rectangle(texture=texture,
                      pos=(self.planet.pos[0] - self.planet.radius,
                           self.planet.pos[1] - self.planet.radius),
                      size=(self.planet.radius * 2, self.planet.radius * 2))

            # Draw ship
            if self.ship:
                from kivy.graphics import Color, Ellipse
                Color(*self.ship.color)
                Ellipse(pos=(self.ship.pos[0] - self.ship.radius,
                             self.ship.pos[1] - self.ship.radius),
                        size=(self.ship.radius * 2, self.ship.radius * 2))

class GravitySimApp(App):
    def build(self):
        return GravitySimWidget()

if __name__ == '__main__':
    GravitySimApp().run()








#gravity_sim_widget.py

### Contains class defining the main widget with the gravity simulation functionality.
  
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse, Rectangle
from kivy.clock import Clock
from kivy.core.image import Image as CoreImage
from kivy.graphics import Line, Color
import math

from constants import *
from graphics.planet import Planet
from graphics.spaceship import Spaceship


class GravitySimWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.planet = Planet(WIDTH, HEIGHT, mass=PLANET_MASSES["jupiter"], radius=PLANET_SIZE, planet_name="jupiter")
        self.ships = []  # Start with no ships
        self.drag_start = None
        self.drag_line = None
        self.drag_end = None
        self.bind(size=self.on_size)

        self.bg_texture = CoreImage("images/background.jpg").texture

        Clock.schedule_interval(self.update, 1.0 / FPS)

    # sets position of planet to middle of window
    def on_size(self, *args):
        self.planet.pos = [self.width / 2, self.height / 2]

    # on mousedown, mouse position is recorded for the start of a mouse drag
    def on_touch_down(self, touch):
        self.drag_start = touch.pos
        return True

    # as mouse moves, planet is redrawn, and a white line is displayed between initial touch pos. and current mouse pos.
    def on_touch_move(self, touch):         
        self.draw()  # Redraw planet
        with self.canvas:
            Color(1, 1, 1)
            self.drag_line = Line(points=[*self.drag_start, touch.x, touch.y], width=2)

    # when mouse is lifted, if there was a drag in process, draw a new spaceship with initial vel. components
    def on_touch_up(self, touch):
        if self.drag_start:
            dx = self.drag_start[0] - touch.x
            dy = self.drag_start[1] - touch.y
            vx = dx * VEL_SCALE  # scale down velocity
            vy = dy * VEL_SCALE
            newShip = Spaceship(*self.drag_start, vx, vy, mass=SHIP_MASS, radius=OBJ_SIZE)
            self.ships.append(newShip)
            self.drag_start = None
            self.drag_line = None

    # update window display for every given frame interval
    def update(self, dt):

        # if there are no ships, then simply redraw window
        if len(self.ships) == 0:
            self.draw()
            return
        
        else:

            # iterate through each existing ship 
            for ship in self.ships[:]:
        
                offScreen = ship.pos[0] < 0 or ship.pos[0] > self.width or ship.pos[1] < 0 or ship.pos[1] > self.height

                collided = math.sqrt((ship.pos[0] - self.planet.pos[0])**2 + (ship.pos[1] - self.planet.pos[1])**2) < self.planet.radius

                # if current ship is out of bounds, then remove it and redraw window
                if offScreen or collided:
                    self.ships.remove(ship)
                    self.draw()
                    return

                # calculate effect of grav. force on spaceship velocity

                # obtain distance between planet and spaceship
                dx = self.planet.pos[0] - ship.pos[0]
                dy = self.planet.pos[1] - ship.pos[1]
                dist = math.hypot(dx, dy)

                if dist == 0:
                    return
                
                # calculate approx. grav. force
                force = (G * self.planet.mass * ship.mass) / (dist ** 2)

                # obtain hypot. angle
                angle = math.atan2(dy, dx)

                # obtain force components
                fx = math.cos(angle) * force
                fy = math.sin(angle) * force

                # update velocity components with calculated acc. components, resp.
                ship.vel[0] += fx / ship.mass
                ship.vel[1] += fy / ship.mass

                # use vel. components to obtain new pos. components, and update spaceship's position accordingly
                ship.pos[0] += ship.vel[0]
                ship.pos[1] += ship.vel[1]

                # redraw window
                self.draw()

    # update planet with given name
    def set_planet(self, planet_name):
        self.planet.update_planet(PLANET_MASSES[planet_name], planet_name)

    # draw window
    def draw(self):
        self.canvas.clear()
        with self.canvas:

            # Draw background
            Rectangle(texture=self.bg_texture, 
                      pos=(0, 0), 
                      size=(self.width, self.height))

            # Draw planet
            Rectangle(texture=self.planet.image,
                      pos=(self.planet.pos[0] - self.planet.radius,
                           self.planet.pos[1] - self.planet.radius),
                      size=(self.planet.radius * 2, self.planet.radius * 2))

            # Draw ship
            for ship in self.ships:
                Color(*ship.color)
                Ellipse(pos=(ship.pos[0] - ship.radius,
                             ship.pos[1] - ship.radius),
                        size=(ship.radius * 2, ship.radius * 2))
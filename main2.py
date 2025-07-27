from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse, Rectangle
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.core.image import Image as CoreImage
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty
from kivy.uix.spinner import Spinner
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
VEL_SCALE = 0.05

"""
PLANET_MASS = 100
SHIP_MASS = 5
G = 5
FPS = 60
PLANET_SIZE = 50
OBJ_SIZE = 5
VEL_SCALE = 100
"""

class MainMenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.dropdown import DropDown
        from kivy.uix.button import Button
        from kivy.uix.label import Label

        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        
        self.planet_options = list(PLANET_MASSES.keys())
        self.selected_planet = self.planet_options[1]

        self.spinner = Spinner(
            text=self.selected_planet,
            values=self.planet_options,
            size_hint=(1, 0.2)
        )

        self.spinner.bind(text=self.select_planet)

        start_btn = Button(text="Start Simulation", size_hint=(1, 0.2))
        start_btn.bind(on_press=self.start_simulation)

        quit_btn = Button(text="Quit", size_hint=(1, 0.2))
        quit_btn.bind(on_press=App.get_running_app().stop)

        layout.add_widget(Label(text="Select a Planet", size_hint=(1, 0.1)))
        layout.add_widget(self.spinner)
        layout.add_widget(start_btn)
        layout.add_widget(quit_btn)

        self.add_widget(layout)

    def select_planet(self, spinner, text):
        self.selected_planet = text

    def start_simulation(self, instance):
        sim_screen = self.manager.get_screen("sim")
        sim_screen.set_planet(self.selected_planet)

        self.manager.current = "sim"


        
class SimulationScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.sim_widget = GravitySimWidget()
        self.add_widget(self.sim_widget)

    def set_planet(self, name):
        self.sim_widget.set_planet(name)


Window.size = (WIDTH, HEIGHT)  # Optional for desktop preview

class Planet:
    def __init__(self, x, y, mass, radius, planet_name, color=(0, 0, 1)):
        self.pos = [x, y]
        self.mass = mass
        self.radius = radius
        self.color = color
        self.name = planet_name
        self.image = CoreImage(f"images/{self.name}.png").texture

    def update_planet(self, newMass, newName):
        self.mass = newMass
        self.name = newName
        self.image = CoreImage(f"images/{newName}.png").texture

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
        self.planet = Planet(WIDTH, HEIGHT, mass=PLANET_MASS, radius=PLANET_SIZE, planet_name="jupiter")
        self.ships = []  # Start with no ships
        self.drag_start = None
        self.drag_line = None
        self.drag_end = None
        self.bind(size=self.on_size)

        self.bg_texture = CoreImage("images/background.jpg").texture

        Clock.schedule_interval(self.update, 1.0 / FPS)

    def on_size(self, *args):
        self.planet.pos = [self.width / 2, self.height / 2]

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
            vx = dx * VEL_SCALE  # scale down velocity
            vy = dy * 0.05
            newShip = Spaceship(*self.drag_start, vx, vy, mass=SHIP_MASS, radius=OBJ_SIZE)
            self.ships.append(newShip)
            self.drag_start = None
            self.drag_line = None

    def update(self, dt):
        if len(self.ships) == 0:
            self.draw()
            return
        
        else:

            for ship in self.ships[:]:
        
                offScreen = ship.pos[0] < 0 or ship.pos[0] > self.width or ship.pos[1] < 0 or ship.pos[1] > self.height

                collided = math.sqrt((ship.pos[0] - self.planet.pos[0])**2 + (ship.pos[1] - self.planet.pos[1])**2) < self.planet.radius

                if offScreen or collided:
                    self.ships.remove(ship)
                    self.draw()
                    return

                # Gravity calculation
                dx = self.planet.pos[0] - ship.pos[0]
                dy = self.planet.pos[1] - ship.pos[1]
                dist = math.hypot(dx, dy)

                if dist == 0:
                    return
                
                force = (G * self.planet.mass * ship.mass) / (dist ** 2)
                angle = math.atan2(dy, dx)
                fx = math.cos(angle) * force
                fy = math.sin(angle) * force

                ship.vel[0] += fx / ship.mass
                ship.vel[1] += fy / ship.mass
                ship.pos[0] += ship.vel[0]
                ship.pos[1] += ship.vel[1]

                self.draw()

    def set_planet(self, planet_name):
        self.planet.update_planet(PLANET_MASSES[planet_name], planet_name)

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

class GravitySimApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainMenuScreen(name="menu"))
        sm.add_widget(SimulationScreen(name="sim"))
        return sm

if __name__ == '__main__':
    GravitySimApp().run()








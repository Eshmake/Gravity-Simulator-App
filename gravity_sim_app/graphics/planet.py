
from kivy.core.image import Image as CoreImage

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

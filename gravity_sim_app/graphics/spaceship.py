
class Spaceship:
    def __init__(self, x, y, vx, vy, mass, radius, color=(1, 0, 0)):
        self.pos = [x, y]
        self.vel = [vx, vy]
        self.mass = mass
        self.radius = radius
        self.color = color
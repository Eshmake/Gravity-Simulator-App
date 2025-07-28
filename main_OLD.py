
import pygame
import math

pygame.init()

WIDTH, HEIGHT = 800, 600

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gravitational Slingshot Effect")


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


BG = pygame.transform.scale(pygame.image.load("images/background.jpg"), (WIDTH, HEIGHT))
PLANET = pygame.transform.scale(pygame.image.load("images/jupiter.png"), (PLANET_SIZE*2, PLANET_SIZE*2))

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)


class Planet:
    
    def __init__(self, x, y, mass):
        self.x = x
        self.y = y
        self.mass = mass
        
    def draw(self):
        win.blit(PLANET, (self.x - PLANET_SIZE, self.y - PLANET_SIZE))

class Spacecraft:

    def __init__(self, x, y, velX, velY, mass):
        self.x = x
        self.y = y
        self.velX = velX
        self.velY = velY
        self.mass = mass

    def draw(self):
        pygame.draw.circle(win, RED, (int(self.x), int(self.y)), OBJ_SIZE)

    def move(self, planet=None):
        distance = math.sqrt((self.x - planet.x)**2 + (self.y - planet.y)**2)
        force = (G * self.mass * planet.mass) / distance**2
        acc = force / self.mass

        #angle obtained from displacement components
        angle = math.atan2(planet.y - self.y, planet.x - self.x)

        #angle then used to obtain x and y components of acceleration
        accX = acc * math.cos(angle)
        accY = acc * math.sin(angle)

        #apply acceleration to velocity
        self.velX += accX
        self.velY += accY
         
        #apply new velocity to current position (to obtain new position)
        self.x += self.velX
        self.y += self.velY


def createShip(location, mouse):
    tempX, tempY = location
    mouseX, mouseY = mouse

    velX = (mouseX - tempX) / VEL_SCALE
    velY = (mouseY - tempY) / VEL_SCALE

    obj = Spacecraft(tempX, tempY, velX, velY, SHIP_MASS)

    return obj

def main():
    running = True
    clock = pygame.time.Clock()

    objects = []

    temp_obj_pos = None

    while(running):
        clock.tick(FPS)

        planet = Planet(WIDTH // 2, HEIGHT // 2, PLANET_MASS)

        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if temp_obj_pos:
                    obj = createShip(temp_obj_pos, mouse_pos)
                    objects.append(obj)
                    temp_obj_pos = None
                else:
                    temp_obj_pos = mouse_pos
            
        win.blit(BG, (0, 0))

        if temp_obj_pos:
            pygame.draw.line(win, WHITE, temp_obj_pos, mouse_pos, 2)
            pygame.draw.circle(win, RED, temp_obj_pos, OBJ_SIZE)

        for obj in objects[:]:
            obj.draw()
            obj.move(planet)

            offScreen = obj.x < 0 or obj.x > WIDTH or obj.y < 0 or obj.y > HEIGHT

            collided = math.sqrt((obj.x - planet.x)**2 + (obj.y - planet.y)**2) < PLANET_SIZE

            if offScreen or collided:
                objects.remove(obj)
        
        planet.draw()

        pygame.display.update()
    
    pygame.quit()



if __name__ == "__main__":
    main()
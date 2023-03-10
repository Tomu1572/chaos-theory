import random
import pygame

class Lorenz:
    def __init__(self):
        self.xMin, self.xMax = -30, 30
        self.yMin, self.yMax = -30, 30
        self.zMin, self.zMax = 0, 50
        self.X, self.Y, self.Z = 0.1, 0.0, 0.0
        self.oX, self.oY, self.oZ = self.X, self.Y, self.Z
        self.dt = 0.01
        self.a, self.b, self.c = 10, 28, 8/3
        self.pixelColour = (255, 0, 0)

    def step(self):
        self.oX, self.oY, self.oZ = self.X, self.Y, self.Z
        self.X = self.X + (self.dt * self.a * (self.Y - self.X))                #dx/dt = alpha*(y-x)
        self.Y = self.Y + (self.dt * (self.X * (self.b - self.Z) - self.Y))     #dy/dt = x(p-z)-y
        self.Z = self.Z + (self.dt * (self.X * self.Y - self.c * self.Z))       #dz/dt = xy - Bz

    def draw(self, displaySurface):
        width, height = displaySurface.get_size()
        oldPos = self.ConvertToScreen(self.oX, self.oY, self.xMin, self.xMax, self.yMin, self.yMax, width, height)
        newPos = self.ConvertToScreen(self.X, self.Y, self.xMin, self.xMax, self.yMin, self.yMax, width, height)

        # Draw the current line
        newRect = pygame.draw.line(displaySurface, self.pixelColour, oldPos, newPos, 2)
        
        return newRect

    def ConvertToScreen(self, x, y, xMin, xMax, yMin, yMax, width, height):
        newX = width * ((x - xMin) / (xMax - xMin))
        newY = height * ((y - yMin) / (yMax - yMin))
        
        return int(newX), int(newY)

class Application:
    def __init__(self):
        self.isRunning = True
        self.displaySurface = None
        self.fpsClock = None
        self.attractors = []
        self.size = self.width, self.height = 1920, 1080
        self.count = 0
        self.outputCount = 1

    def on_init(self):
        pygame.init()
        pygame.display.set_caption("Lorenz Attractor")
        self.displaySurface = pygame.display.set_mode(self.size)
        self.isRunning = True
        self.fpsClock = pygame.time.Clock()

        #Config attractor
        self.attractors = Lorenz()

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self.isRunning = False

    def on_loop(self):
        self.attractors.step()

    def on_render(self):
        newRect = self.attractors.draw(self.displaySurface)
        pygame.display.update(newRect)

    def on_execute(self):
        if self.on_init() == False:
            self.isRunning = False
        
        while self.isRunning:
            for event in pygame.event.get():
                self.on_event(event)

            self.on_loop()
            self.on_render()
            
            self.fpsClock.tick(60)
            self.count += 1

        pygame.quit()

if __name__ == "__main__":
    t = Application()
    t.on_execute()

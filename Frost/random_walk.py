import random
import pygame
import numpy as np

class Application:
    def __init__(self):
        self.size = self.width, self.height = 640, 480
        self.startX, self.startY = round(self.width/2), round(self.height/2)
        self.X, self.Y = self.startX, self.startY
        self.displaySurface = None
        self.pixelArray = None
        self.pixelColour = None
        self.updateFlag = False

    def on_init(self):
        pygame.init()
        pygame.display.set_caption("Random Walk")
        self.displaySurface = pygame.display.set_mode(self.size)
        self.pixelArray = pygame.PixelArray(self.displaySurface)
        self.pixelColour = (255, 0, 0)
        self.isRunning = True

        # Set the speed point.
        self.pixelArray[self.startX, self.startY + 10] = 0xFF0000
        pygame.display.update()

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self.isRunning = False

    def on_loop(self):
        # Choose random direction.
        newDir = random.choice(((0,1), (0,-1), (1,0), (-1,0)))
        
        # Extract dX and dY.
        dX, dY = newDir

        # Apply these to X and Y coordinates.
        newX = self.X + dX
        newY = self.Y + dY

        if (newX < 0):
            newX = 0

        if (newX > self.width-1):
            newX = self.width-1

        if (newY < 0):
            newY = 0

        if (newY > self.height-1):
            newY = self.height-1

        # Check if the pixel has already been set.
        if (self.pixelArray[newX, newY] == 0xFF0000):
            self.updateFlag = True
        else:
            self.updateFlag = False
            self.X, self.Y = newX, newY

    def on_render(self):
        # Update pixel array.
        if self.updateFlag:
            self.pixelArray[self.X, self.Y] = 0xFF0000

            # Update display.
            pygame.display.update()

            # Reset the updated flag and random walk.
            self.updateFlag = False
            self.X, self.Y = self.startX, self.startY

    def on_execute(self):
        if self.on_init() == False:
            self.isRunning = False

        while self.isRunning:
            for event in pygame.event.get():
                self.on_event(event)

            self.on_loop()
            self.on_render()

        pygame.quit()

if __name__ == "__main__":
    t = Application()
    t.on_execute()
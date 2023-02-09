import random
import pygame
import numpy as np

class Application:
    def __init__(self):
        self.size = self.width, self.height = 640, 480
        self.startX, self.startY = round(self.width/2), round(self.height/2)
        self.X, self.Y = self.startX, self.startY

        self.minX, self.minY = self.X, self.Y
        self.maxX, self.maxY = self.X, self.Y
        self.padSize = 20

        self.domainMinX = self.startX - self.padSize
        self.domainMaxX = self.startX + self.padSize
        self.domainMinY = self.startY - self.padSize
        self.domainMaxY = self.startY + self.padSize

        self.crystalColour = 0x808080

        self.displaySurface = None
        self.pixelArray = None
        self.updateFlag = False

    def on_init(self):
        pygame.init()
        pygame.display.set_caption("Frost - With Simulation Domain")
        self.displaySurface = pygame.display.set_mode(self.size)
        self.pixelArray = pygame.PixelArray(self.displaySurface)
        self.pixelColour = (255, 0, 0)
        self.isRunning = True

        # Set the speed point.
        self.pixelArray[self.startX, self.startY + 10] = self.crystalColour
        pygame.display.update()

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self.isRunning = False

    def on_loop(self):
        # Choose random direction.
        newDir = random.choice(((0,1), (0,-1), (1,0), (-1,0), (1,-1), (-1,1), (1,1), (-1,-1)))
        
        # Extract dX and dY.
        dX, dY = newDir

        # Apply these to X and Y coordinates.
        newX = self.X + dX
        newY = self.Y + dY

        if (newX < self.domainMinX):
            newX = self.domainMaxX

        if (newX > self.domainMaxX):
            newX = self.domainMinX

        if (newY < self.domainMinY):
            newY = self.domainMaxY

        if (newY > self.domainMaxY):
            newY = self.domainMinY

        # Check if the pixel has already been set.
        if (self.pixelArray[newX, newY] == self.crystalColour):
            self.updateFlag = True

            # Modify the extent of the simulation domain, if necessary.
            if (self.X < self.minX):
                self.minX = self.X

            if (self.X > self.maxX):
                self.maxX = self.X

            if (self.Y > self.minY):
                self.maxY = self.Y

            # Modify the domain.
            self.domainMinX = max([self.minX - self.padSize, 1])
            self.domainMaxX = min([self.maxX + self.padSize, self.width - 1])

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
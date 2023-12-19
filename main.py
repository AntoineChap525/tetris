import pygame
import random
import numpy

SCREEN_COLOR = (255, 255, 255)
SCREEN_WIDTH = 200
SCREEN_HEIGHT = 400
CLOCK_FREQUENCY = 5

TILES_SIZE = 20
TILES_COLOR = (245, 245, 245)

PIECES = [[[1,1,1,1]], 
          [[1,0,0], [1,1,1]], 
          [[0,0,1], [1,1,1]], 
          [[1,1], [1,1]], 
          [[0,1,1], [1,1,0]],
          [[0,1,0], [1,1,1]],
          [[1,1,0], [0,1,1]]]

class Game:
    def __init__(self, screen):
        self.piece = Piece()
        self.screen = screen
    
    def display_checkerboard(self):
        self.screen.fill(SCREEN_COLOR)
        k, l = int(SCREEN_HEIGHT / TILES_SIZE), int(SCREEN_WIDTH / TILES_SIZE)
        for i in range(k):
            for j in range(l):
                if (i + j) % 2 == 1:
                    rect = pygame.Rect(
                        j * TILES_SIZE, i * TILES_SIZE, TILES_SIZE, TILES_SIZE
                    )
                    pygame.draw.rect(self.screen, TILES_COLOR, rect)

class Piece:
    def __init__(self):
        self.shape = random.choice(PIECES)
        self.position = [0,0]


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    game = Game(screen)
    while True:
        clock.tick(CLOCK_FREQUENCY)
        game.display_checkerboard()
        pygame.display.update()

        

main()
import pygame
import random
import numpy

SCREEN_COLOR = (100, 100, 100)
SCREEN_WIDTH = 200
SCREEN_HEIGHT = 400
CLOCK_FREQUENCY = 5

TILES_SIZE = 20
TILES_COLOR = (50, 50, 50)

PIECES = [
    [[1, 1, 1, 1]],
    [[1, 0, 0], [1, 1, 1]],
    [[0, 0, 1], [1, 1, 1]],
    [[1, 1], [1, 1]],
    [[0, 1, 1], [1, 1, 0]],
    [[0, 1, 0], [1, 1, 1]],
    [[1, 1, 0], [0, 1, 1]],
]

PIECES_COLOURS = [
    (255, 192, 203),
    (173, 216, 230),  # Bleu ciel pastel
    (255, 255, 153),  # Jaune pâle
    (144, 238, 144),  # Vert clair
    (230, 230, 250),  # Lavande pastel
    (255, 218, 185),  # Pêche clair
    (255, 165, 79),
]


class Game:
    def __init__(self, screen):
        self.piece = Piece()
        self.screen = screen
        self.is_running = True

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

    def update(self):
        self.piece.update()

    def display(self):
        self.display_checkerboard()
        self.piece.display(self.screen)


class Piece:
    def __init__(self):
        self.shape = random.choice(PIECES)
        self.position = [0, 0]  # coin en haut à gauche de la pièce ou shape[0,0]
        self.colour = random.choice(PIECES_COLOURS)
        self.horizontal_direction = 0

    def update(self):
        width = len(self.shape[0])
        max_width = SCREEN_WIDTH // TILES_SIZE
        new_position = self.position[1] + self.horizontal_direction
        if (new_position >= 0) and (new_position + width <= max_width):
            self.position[1] = new_position
        self.horizontal_direction = 0
        self.position[0] += 1

    def display(self, screen):
        for i in range(len(self.shape)):
            for j in range(len(self.shape[i])):
                if self.shape[i][j] == 1:
                    x = (self.position[0] + i) * TILES_SIZE
                    y = (self.position[1] + j) * TILES_SIZE
                    rect = pygame.Rect(y, x, TILES_SIZE, TILES_SIZE)
                    pygame.draw.rect(screen, self.colour, rect)


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    game = Game(screen)
    while game.is_running:
        clock.tick(CLOCK_FREQUENCY)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:  # quit the game
                    game.is_running = False
                # Control
                if event.key == pygame.K_LEFT:
                    game.piece.horizontal_direction = -1
                if event.key == pygame.K_RIGHT:
                    game.piece.horizontal_direction = 1

            if event.type == pygame.QUIT:  # quit the game
                game.is_running = False

        game.update()
        game.display()
        pygame.display.update()


main()

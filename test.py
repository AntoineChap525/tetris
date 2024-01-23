
import pygame
import random
import numpy as np
import pandas as pd
from username import get_username

SCREEN_COLOR = (100, 100, 100)
SCREEN_WIDTH = 200
SCREEN_HEIGHT = 500
CLOCK_FREQUENCY = 5

TILES_SIZE = 20
TILES_COLOR = (50, 50, 50)

NUMBER_OF_TILES_HEIGHT = SCREEN_HEIGHT // TILES_SIZE
NUMBER_OF_TILES_WIDGHT = SCREEN_WIDTH // TILES_SIZE

LINE_POSITION = 4 * TILES_SIZE
LINE_COLOR = (230, 0, 0)

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
    (255, 192, 203),  # couleur 0
    (173, 216, 230),  # couleur 1
    (255, 255, 153),  # etc..
    (144, 238, 144),  # Vert clair
    (230, 230, 250),  # Lavande pastel
    (255, 218, 185),  # Pêche clair
    (255, 165, 79),
]

# Welcome text
welcome_text = [
    "Bienvenue sur Tetris by Toine&Blini© ⬇︎⬅︎⏯︎⬅︎",
    "Pour bouger une pièce horizontalement, utiliser les touches fléchées de votre clavier",
    "Pour accélérer la descente d’une pièce, utiliser la flèche du bas",
    "Pour faire tourner une pièce dans le sens horaire (resp. anti-horaire), appuyer sur  la touche d (resp. q).",
    "Pour faire pause/play, appuyer sur la touche espace.",
    "Pour encore plus de fun, mettez le son",
    "Pour commencer, appuyer sur espace",
]

# Init pause image
IMAGE_SCALE = 15
pause_image = pygame.image.load("pause.png")
new_size = (
    pause_image.get_width() // IMAGE_SCALE,
    pause_image.get_height() // IMAGE_SCALE,
)
pause_image = pygame.transform.scale(pause_image, new_size)
rect_image = pause_image.get_rect()
rect_image.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)


class Game:
    def __init__(self, screen):
        self.piece = Piece()
        self.screen = screen
        self.placed_pieces = np.full(
            (NUMBER_OF_TILES_HEIGHT, NUMBER_OF_TILES_WIDGHT), -1
        )
        self.is_running = True
        self.score = 0

    def welcome(self):
        self.screen = pygame.display.set_mode((900, 700))
        font = pygame.font.Font(None, 24)
        self.screen.fill(PIECES_COLOURS[0])
        y = 20
        for line in welcome_text:
            text = font.render(line, True, (0, 0, 0))
            self.screen.blit(text, (50, y))
            y += 30
        pygame.display.flip()
        a = True
        while a:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        a = 0
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

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
        pygame.draw.line(
            self.screen,
            LINE_COLOR,
            [0, LINE_POSITION],
            [SCREEN_WIDTH, LINE_POSITION],
            2,
        )

    def update(self):
        self.piece.update(self.placed_pieces)
        if self.piece.has_collided(self.placed_pieces):
            self.update_placed_pieces()
            self.piece = Piece()
        self.check_full_line()

    def update_placed_pieces(self):
        position = self.piece.position
        for i in range(len(self.piece.shape)):
            for j in range(len(self.piece.shape[i])):
                if self.piece.shape[i, j] == 1:
                    self.placed_pieces[
                        position[0] + i, position[1] + j
                    ] = PIECES_COLOURS.index(self.piece.colour)

    def display_placed_pieces(self):
        for i in range(len(self.placed_pieces)):
            for j in range(len(self.placed_pieces[0])):
                if self.placed_pieces[i, j] != -1:
                    x, y = i * TILES_SIZE, j * TILES_SIZE
                    rect = pygame.Rect(y, x, TILES_SIZE, TILES_SIZE)
                    pygame.draw.rect(
                        self.screen, PIECES_COLOURS[int(self.placed_pieces[i, j])], rect
                    )

    def display(self):
        self.display_checkerboard()
        self.piece.display(self.screen)
        self.display_placed_pieces()

    def check_game_over(self):
        if not np.all(self.placed_pieces[3] == -1):
            self.game_over()

    def game_over(self):
        self.is_running = False

        df = pd.read_csv("score.csv")
        username = get_username()
        new_line = pd.DataFrame([[username, self.score]], columns=["username", "score"])
        df = pd.concat([df, new_line], ignore_index=True)
        df.to_csv("score.csv", index=False)

        self.screen = pygame.display.set_mode((400, 300))
        # best scores ever
        self.screen.fill(SCREEN_COLOR)
        y = 50
        font = pygame.font.Font(None, 36)
        for index, row in df.nlargest(3, "score").iterrows():
            text = f"{row['username']}: {row['score']}"
            score_text = font.render(text, True, (0, 0, 0))
            self.screen.blit(score_text, (50, y))
            y += 40
        y += 40
        # personal best score
        personal_best_score = df.loc[df["username"] == username, "score"].max()
        text = f"your best score: {personal_best_score}"
        score_text = font.render(text, True, (0, 0, 0))
        self.screen.blit(score_text, (50, y))

        pygame.display.set_caption("Highscores")
        pygame.display.flip()
        a = 1
        while a:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    a = 0

    def check_full_line(self):
        for i in range(len(self.placed_pieces)):
            if np.all(self.placed_pieces[i] != -1):
                self.placed_pieces = np.delete(self.placed_pieces, i, axis=0)
                new_line = np.full((1, NUMBER_OF_TILES_WIDGHT), -1)
                self.placed_pieces = np.vstack([new_line, self.placed_pieces])
                self.score += 10

    def pause(self):
        is_paused = True
        self.screen.fill(random.choice(PIECES_COLOURS))
        self.screen.blit(pause_image, rect_image)
        pygame.display.update()
        while is_paused:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        is_paused = False
                if event.type == pygame.QUIT:
                    is_paused = False
                    self.is_running = False


class Piece:
    def __init__(self):
        self.shape = np.array(random.choice(PIECES))
        self.position = [
            0,
            NUMBER_OF_TILES_WIDGHT // 2 - 1,
        ]  # middle
        self.colour = random.choice(PIECES_COLOURS)
        self.horizontal_direction = 0

        random_number = random.randint(0, 3)
        for i in range(random_number + 1):
            self.shape = np.rot90(self.shape)

    def update(self, placed_pieces):
        if self.horizontal_direction != 0:
            self.update_horizontal(placed_pieces)
        if not self.has_collided(placed_pieces):
            self.position[0] += 1

    def update_horizontal(self, placed_pieces):
        width = len(self.shape[0])
        max_width = SCREEN_WIDTH // TILES_SIZE
        former_position = np.copy(self.position)
        new_position = self.position[1] + self.horizontal_direction
        if (new_position >= 0) and (new_position + width <= max_width):
            self.position[1] = new_position
        if self.has_superposed(placed_pieces):
            self.position = former_position
        self.horizontal_direction = 0

    def has_collided(self, placed_pieces):
        max_height = SCREEN_HEIGHT // TILES_SIZE

        has_collided_ground = self.position[0] + len(self.shape) >= max_height

        has_collided_placed_piece = False
        if not has_collided_ground:
            for i in range(len(self.shape)):
                for j in range(len(self.shape[i])):
                    if self.shape[i, j] == 1:
                        if (
                            placed_pieces[
                                self.position[0] + i + 1,
                                self.position[1] + j,
                            ]
                            != -1
                        ):
                            has_collided_placed_piece = True
        return has_collided_ground or has_collided_placed_piece

    def has_superposed(self, placed_pieces):
        max_height = SCREEN_HEIGHT // TILES_SIZE
        width = len(self.shape[0])
        max_width = SCREEN_WIDTH // TILES_SIZE

        is_beyond_borders = (self.position[1] < 0) or (
            self.position[1] + width > max_width
        )
        is_beyond_ground = self.position[0] + len(self.shape) > max_height
        has_superposed_placed_piece = False
        if not is_beyond_ground and not is_beyond_borders:
            for i in range(len(self.shape)):
                for j in range(len(self.shape[i])):
                    if self.shape[i, j] == 1:
                        if (
                            placed_pieces[
                                self.position[0] + i,
                                self.position[1] + j,
                            ]
                            != -1
                        ):
                            has_superposed_placed_piece = True

        return is_beyond_ground or has_superposed_placed_piece or is_beyond_borders

    def rotate_trigo(self, placed_pieces):
        former_shape = np.copy(self.shape)
        self.shape = np.rot90(self.shape)
        if self.has_superposed(placed_pieces):
            self.shape = former_shape

    def rotate_clockwise(self, placed_pieces):
        former_shape = np.copy(self.shape)
        self.shape = np.rot90(self.shape, k=-1)
        if self.has_superposed(placed_pieces):
            self.shape = former_shape

    def down(self, placed_pieces):
        former_position = np.copy(self.position)
        self.position[0] += 1
        if self.has_superposed(placed_pieces):
            self.position = former_position

    def display(self, screen):
        for i in range(len(self.shape)):
            for j in range(len(self.shape[i])):
                if self.shape[i, j] == 1:
                    x = (self.position[0] + i) * TILES_SIZE
                    y = (self.position[1] + j) * TILES_SIZE
                    rect = pygame.Rect(y, x, TILES_SIZE, TILES_SIZE)
                    pygame.draw.rect(screen, self.colour, rect)


def main():
    pygame.init()
    pygame.mixer.init()
    chemin_fichier_audio = "game-tetris-original.mp3"
    pygame.mixer.music.load(chemin_fichier_audio)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    game = Game(screen)
    pygame.mixer.music.play()

    # Welcome
    game.welcome()

    pygame.mixer.music.set_endevent(
        pygame.USEREVENT
    )  # define event for end of the music

    while game.is_running:
        pygame.display.set_caption("Tetris" + f" Score : {game.score}")
        clock.tick(CLOCK_FREQUENCY * (game.score / 100 + 1))

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                # Control
                if event.key == pygame.K_LEFT:
                    game.piece.horizontal_direction += -1
                if event.key == pygame.K_RIGHT:
                    game.piece.horizontal_direction += 1
                if event.key == pygame.K_q:
                    game.piece.rotate_trigo(game.placed_pieces)
                if event.key == pygame.K_d:
                    game.piece.rotate_clockwise(game.placed_pieces)
                if event.key == pygame.K_DOWN:
                    game.piece.down(game.placed_pieces)
                if event.key == pygame.K_SPACE:
                    game.pause()
            if event.type == pygame.QUIT:
                game.is_running = False
            if event.type == pygame.USEREVENT:
                # if end of the music, continue
                pygame.mixer.music.play()
        game.update()
        game.display()
        game.check_game_over()
        pygame.display.update()


main()

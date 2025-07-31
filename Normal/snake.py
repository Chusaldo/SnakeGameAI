import sys
import pygame
from pygame import Vector2
import random

pygame.init()

# Constants
UP = Vector2(0,-1)
DOWN = Vector2(0,1)
RIGHT = Vector2(1,0)
LEFT = Vector2(-1,0)

TITLE_FONT = pygame.font.SysFont(None, 60)
SCORE_FONT = pygame.font.SysFont(None, 40)

# Colors
GREEN = (173, 204, 96)
DARK_GREEN = (43, 51, 24)

# Screen initialization
cell_size = 30
number_of_cells = 25
OFFSET = 75
SCREEN_WIDTH = 2*OFFSET + cell_size*number_of_cells
SCREEN_HEIGHT = SCREEN_WIDTH
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game")

class Food:
    def __init__(self, snake_body):
        self.surface = pygame.image.load("../Graphics/food.png")
        self.position = self.generate_random_pos(snake_body)

    def draw(self):
        food_rect = pygame.Rect(OFFSET + self.position.x * cell_size, OFFSET + self.position.y * cell_size, cell_size, cell_size)
        SCREEN.blit(self.surface, food_rect)

    def generate_random_cell(self):
        x = random.randint(0, number_of_cells - 1)
        y = random.randint(0, number_of_cells - 1)
        return Vector2(x, y)

    def generate_random_pos(self, snake_body):
        position = self.generate_random_cell()
        while position in snake_body:
            position = self.generate_random_cell()
        return position

class Snake:
    def __init__(self):
        self.body = [Vector2(6, 9), Vector2(5, 9), Vector2(4, 9)]
        self.direction = RIGHT
        self.add_segment = False
        self.eat_sound = pygame.mixer.Sound("../Sounds/eat.mp3")
        self.wall_hit_sound = pygame.mixer.Sound("../Sounds/wall.mp3")

    def draw(self):
        for segment in self.body:
            segment_rect = pygame.Rect(OFFSET + segment.x * cell_size, OFFSET + segment.y * cell_size, cell_size, cell_size)
            pygame.draw.rect(SCREEN, DARK_GREEN, segment_rect, 0, 7)

    def update(self):
        self.body.insert(0, self.body[0] + self.direction)
        if self.add_segment:
            self.add_segment = False
        else:
            self.body = self.body[:-1]

    def reset(self):
        self.body = [Vector2(6, 9), Vector2(5, 9), Vector2(4, 9)]
        self.direction = RIGHT

class Game:
    def __init__(self):
        self.snake = Snake()
        self.food = Food(self.snake.body)
        self.state = "RUNNING"
        self.score = 0

    def draw(self):
        self.snake.draw()
        self.food.draw()

    def update(self):
        if self.state == "RUNNING":
            self.snake.update()
            self.check_collision_with_food()
            self.check_collision_with_edges()
            self.check_collision_wit_tail()

    def check_collision_with_food(self):
        if self.snake.body[0] == self.food.position:
            self.food.position = self.food.generate_random_pos(self.snake.body)
            self.snake.add_segment = True
            self.score += 1
            self.snake.eat_sound.play()

    def check_collision_with_edges(self):
        if self.snake.body[0].x == number_of_cells or self.snake.body[0].x == -1 or self.snake.body[0].y == number_of_cells or self.snake.body[0].y == -1:
            self.game_over()

    def check_collision_wit_tail(self):
        if self.snake.body[0] in self.snake.body[1:]:
            self.game_over()

    def game_over(self):
        self.snake.reset()
        self.food.position = self.food.generate_random_pos(self.snake.body)
        self.state = "STOPPED"
        self.score = 0
        self.snake.wall_hit_sound.play()

game = Game()

clock = pygame.time.Clock()
SNAKE_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SNAKE_UPDATE, 150)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SNAKE_UPDATE:
            game.update()
        if event.type == pygame.KEYDOWN:
            if game.state == "STOPPED":
                game.state = "RUNNING"
            elif event.key == pygame.K_LEFT and game.snake.direction != RIGHT:
                game.snake.direction = LEFT
            elif event.key == pygame.K_RIGHT and game.snake.direction != LEFT:
                game.snake.direction = RIGHT
            elif event.key == pygame.K_UP and game.snake.direction != DOWN:
                game.snake.direction = UP
            elif event.key == pygame.K_DOWN and game.snake.direction != UP:
                game.snake.direction = DOWN

    # Drawing
    SCREEN.fill(GREEN)
    pygame.draw.rect(SCREEN, DARK_GREEN, (OFFSET-5, OFFSET-5, cell_size*number_of_cells+10, cell_size*number_of_cells+10), 5)
    game.draw()
    title_surface = TITLE_FONT.render("Snake Game", True, DARK_GREEN)
    score_surface = SCORE_FONT.render("Score: " + str(game.score), True, DARK_GREEN)
    SCREEN.blit(title_surface, (OFFSET-5, 20))
    SCREEN.blit(score_surface, (OFFSET-5, OFFSET+cell_size*number_of_cells+10))

    # Refresh
    pygame.display.update()
    clock.tick(60)
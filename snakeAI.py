import os
import sys
import pygame
from pygame import Vector2
import random
import neat

pygame.init()

# Constants
UP = Vector2(0,-1)
DOWN = Vector2(0,1)
RIGHT = Vector2(1,0)
LEFT = Vector2(-1,0)

TITLE_FONT = pygame.font.SysFont(None, 60)
STATISTICS_FONT = pygame.font.SysFont(None, 40)

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
    def __init__(self, snake_body, snake_color):
        self.surface = pygame.image.load("Graphics/food.png")
        self.position = self.generate_random_pos(snake_body)
        self.color = snake_color

    def draw(self):
        food_rect = pygame.Rect(OFFSET + self.position.x * cell_size, OFFSET + self.position.y * cell_size, cell_size, cell_size)
        pygame.draw.circle(SCREEN, self.color, (OFFSET + (self.position.x+0.5) * cell_size, OFFSET + (self.position.y+0.5) * cell_size), cell_size/2)
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
        self.eat_sound = pygame.mixer.Sound("Sounds/eat.mp3")
        self.wall_hit_sound = pygame.mixer.Sound("Sounds/wall.mp3")
        self.color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
        self.frames_without_food = 0

    def draw(self):
        for segment in self.body:
            segment_rect = pygame.Rect(OFFSET + segment.x * cell_size, OFFSET + segment.y * cell_size, cell_size, cell_size)
            pygame.draw.rect(SCREEN, self.color, segment_rect, 0, 7)

    def update(self, index):
        self.body.insert(0, self.body[0] + self.direction)
        if self.add_segment:
            self.add_segment = False
        else:
            self.body = self.body[:-1]

    def reset(self):
        self.body = [Vector2(6, 9), Vector2(5, 9), Vector2(4, 9)]
        self.direction = RIGHT

    def turn_left(self):
        self.direction = Vector2(-self.direction.y, self.direction.x)

    def turn_right(self):
        self.direction = Vector2(self.direction.y, -self.direction.x)

class Game:
    def __init__(self):
        self.snake = Snake()
        self.food = Food(self.snake.body, self.snake.color)
        self.score = 0

    def draw(self):
        self.snake.draw()
        self.food.draw()

    def update(self, index):
        ge[index].fitness += 0.1
        self.snake.update(index)
        self.check_collision_with_food(index)
        self.check_collision_with_edges(index)
        self.check_collision_wit_tail(index)

    def check_collision_with_food(self, index):
        if self.snake.body[0] == self.food.position:
            self.food.position = self.food.generate_random_pos(self.snake.body)
            self.snake.add_segment = True
            self.score += 1
            self.snake.eat_sound.play()
            self.snake.frames_without_food = 0
            ge[index].fitness += 10
        else:
            self.snake.frames_without_food += 1
            max_frames = 70 + (len(self.snake.body) * 2)
            if self.snake.frames_without_food > max_frames:
                ge[index].fitness -= 2
                self.game_over(index)

    def check_collision_with_edges(self, index):
        if self.snake.body[0].x == number_of_cells or self.snake.body[0].x == -1 or self.snake.body[0].y == number_of_cells or self.snake.body[0].y == -1:
            ge[index].fitness -= 1
            self.game_over(index)

    def check_collision_wit_tail(self, index):
        if self.snake.body[0] in self.snake.body[1:]:
            ge[index].fitness -= 1
            self.game_over(index)

    def game_over(self, index):
        #self.snake.reset()
        #self.food.position = self.food.generate_random_pos(self.snake.body)
        #self.score = 0
        remove(index)
        self.snake.wall_hit_sound.play()


def remove(index):
    games.pop(index)
    ge.pop(index)
    nets.pop(index)

def eval_genomes(genomes, config):
    global games, ge, nets
    games = []
    ge = []
    nets = []

    for genome_id, genome in genomes:
        games.append(Game())
        ge.append(genome)
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        genome.fitness = 0

    def statistics():
        text_1 = STATISTICS_FONT.render(f'Snakes Alive: {len(games)}', True, DARK_GREEN)
        text_2 = STATISTICS_FONT.render(f'Generation: {pop.generation+1}', True, DARK_GREEN)
        title_surface = TITLE_FONT.render("Snake Game", True, DARK_GREEN)

        SCREEN.blit(title_surface, (OFFSET - 5, 20))
        SCREEN.blit(text_1, (OFFSET-5, OFFSET+cell_size*number_of_cells+10))
        SCREEN.blit(text_2, (OFFSET+250, OFFSET+cell_size*number_of_cells+10))

    def get_relative_directions(current_direction):
        front = current_direction
        left = Vector2(-current_direction.y, current_direction.x)
        right = Vector2(current_direction.y, -current_direction.x)
        return front, left, right

    def get_danger(snake):
        head = snake.body[0]
        direction = snake.direction
        front, left, right = get_relative_directions(direction)

        dangers = []
        for move in [front, left, right]:
            next_pos = head + move
            # Comprobar si está fuera del tablero
            if (
                    next_pos.x < 0 or next_pos.x >= number_of_cells or
                    next_pos.y < 0 or next_pos.y >= number_of_cells or
                    next_pos in snake.body[1:]
            ):
                dangers.append(1)  # Hay peligro
            else:
                dangers.append(0)  # No hay peligro

        return dangers  # [peligro_frente, izquierda, derecha]

    def generate_inputs(index):
        snake = games[index].snake
        food = games[index].food

        head = snake.body[0]
        direction = snake.direction
        front, left, right = get_relative_directions(direction)

        # === 1. Peligros ===
        dangers = get_danger(snake)  # [frente, izq, der]

        # === 2. Dirección de la comida (relativa a la serpiente) ===
        food_direction = food.position - head

        def is_food_in_direction(dir_vec):
            return (dir_vec.x != 0 and (food_direction.x / dir_vec.x > 0)) or \
                (dir_vec.y != 0 and (food_direction.y / dir_vec.y > 0))

        food_front = int(is_food_in_direction(front))
        food_left = int(is_food_in_direction(left))
        food_right = int(is_food_in_direction(right))

        # === 3. Dirección actual codificada (one-hot)
        dir_up = int(direction == UP)
        dir_down = int(direction == DOWN)
        dir_left = int(direction == LEFT)
        dir_right = int(direction == RIGHT)

        # === Lista completa de entradas ===
        inputs = [
            *dangers,  # 3 entradas
            food_front,  # 1
            food_left,  # 1
            food_right,  # 1
            dir_up, dir_down,  # 2
            dir_left, dir_right  # 2
        ]

        return inputs  # Total: 9 entradas

    clock = pygame.time.Clock()
    SNAKE_UPDATE = pygame.USEREVENT
    pygame.time.set_timer(SNAKE_UPDATE, 100)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == SNAKE_UPDATE:
                for index, game in enumerate(games):
                    game.update(index)

        for i, game in enumerate(games):
            output = nets[i].activate(generate_inputs(i))
            action = output.index(max(output))
            if action == 0:
                games[i].snake.turn_left()
            elif action == 2:
                games[i].snake.turn_right()

        if len(games) == 0:
            break

        # Drawing
        SCREEN.fill(GREEN)
        pygame.draw.rect(SCREEN, DARK_GREEN, (OFFSET-5, OFFSET-5, cell_size*number_of_cells+10, cell_size*number_of_cells+10), 5)
        for game in games:
            game.draw()
        statistics()

        # Refresh
        pygame.display.update()
        clock.tick(60)

# Set up the NEAT
def run(config_path):
    global pop
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path
    )

    pop = neat.Population(config)
    pop.run(eval_genomes, 50)

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config = os.path.join(local_dir, "config.txt")
    run(config)

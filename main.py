import pygame
import random

#todo make option screen

pygame.init()
screen_height = 650
screen_width = 610
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Snake")

border = 5
score = 0
chunk = 20

start = 35
# making grid
def make_grid():
    y = start
    x = border
    grid = []
    while x + (chunk + border) < screen_width:
        column = []
        while y + (chunk + border) < screen_height:
            column.append([x, y])
            y += (chunk + border)
        grid.append(column)
        x += (chunk + border)
        y = start
    return grid


grid = make_grid()


class Snake:
    def __init__(self):
        self.x = 2
        self.y = 2
        self.x_change = 0
        self.y_change = 1
        self.body = [[self.x, self.y]]

    def update_cordinates(self):
        x = self.x
        y = self.y
        for i in range(len(self.body)):
            temp_x = self.body[i][0]
            temp_y = self.body[i][1]
            self.body[i] = [x, y]
            x = temp_x
            y = temp_y

    def draw(self):
        if len(self.body) > 0:
            if self.body[0][0] != self.x or self.body[0][1] != self.y:
                self.update_cordinates()
        if self.x in range(0, len(grid)) and self.y in range(0, len(grid[0])):
            for cube in self.body:
                x, y = grid[cube[0]][cube[1]]
                cube = (x, y, chunk, chunk)
                pygame.draw.rect(screen, (255, 255, 255), cube)

    def move_right(self):
        if self.x_change != - 1:
            self.x_change = 1
            self.y_change = 0

    def move_left(self):
        if self.x_change != 1:
            self.x_change = -1
            self.y_change = 0

    def move_up(self):
        if self.y_change != 1:
            self.x_change = 0
            self.y_change = -1

    def move_down(self):
        if self.y_change != - 1:
            self.x_change = 0
            self.y_change = 1

    def move(self):
        self.x += self.x_change
        self.y += self.y_change

    def respawn_food(self, food):
        food.column = random.choice(grid)
        food.block = random.choice(food.column)
        if food.block in [grid[part[0]][part[1]] for part in self.body]:
            self.respawn_food(food)

    def have_eaten(self, food):
        global score
        if grid[self.x][self.y] == food.block:
            self.respawn_food(food)
            score += 1
            self.body.append([self.x, self.y])

    def over(self, over):
        if self.x >= len(grid) or self.y >= len(grid[0]):
            over = True
        if self.x < 0 or self.y < 0:
            over = True
        if [self.x, self.y] in self.body:
            over = True
        return over


class Food:
    def __init__(self):
        self.column = random.choice(grid)
        self.block = random.choice(self.column)
        print(self.block)

    def draw(self):
        x, y = self.block
        block = (x, y, chunk, chunk)
        pygame.draw.rect(screen, (0, 255, 0), block)


def show_score():
    global score
    score_font = pygame.font.Font("freesansbold.ttf", 24)
    score_text = score_font.render(f"score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (5, 5))


def game_over():
    fin_font = pygame.font.Font("freesansbold.ttf", 64)
    over_text = fin_font.render("GAME OVER!", True, (255, 255, 255))
    screen.blit(over_text, (screen_height // 7, (screen_height - 64) // 2))
    score_font = pygame.font.Font("freesansbold.ttf", 24)
    score_text = score_font.render(f"your score was: {score}", True, (255, 255, 255))
    screen.blit(score_text, (screen_height // 3 - 10, screen_height // 2 + 30 ))


food = Food()
snake = Snake()
tempo = 120
running = True
is_over = False
while running:
    screen.fill((51, 0, 102))
    pygame.time.delay(tempo)
    for column in grid:
        for block in column:
            pygame.draw.rect(screen, (0, 0, 0), (block[0], block[1], chunk, chunk))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.move_up()
            if event.key == pygame.K_DOWN:
                snake.move_down()
            if event.key == pygame.K_LEFT:
                snake.move_left()
            if event.key == pygame.K_RIGHT:
                snake.move_right()

    snake.move()
    is_over = snake.over(is_over)
    if not is_over:
        snake.draw()
        snake.have_eaten(food)
        food.draw()
        show_score()
    if is_over:
        game_over()

    pygame.display.update()

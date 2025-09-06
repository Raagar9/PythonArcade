
import pygame
import sys

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 900

ROWS = 21
COLS = 20

maze = [
    ['S', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#'],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#', '#', '#', '#', '#', '#', '#', ' ', '#'],
    ['#', ' ', '#', '#', '#', ' ', '#', '#', '#', '#', '#', ' ', '#', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
    ['#', ' ', '#', ' ', '#', ' ', '#', ' ', ' ', ' ', '#', ' ', '#', ' ', '#', '#', '#', '#', ' ', '#'],
    ['#', ' ', '#', ' ', '#', ' ', '#', '#', '#', ' ', '#', ' ', '#', ' ', ' ', ' ', ' ', '#', ' ', '#'],
    ['#', ' ', '#', ' ', '#', ' ', ' ', ' ', '#', ' ', '#', ' ', '#', ' ', '#', '#', ' ', '#', ' ', '#'],
    ['#', ' ', '#', ' ', ' ', ' ', '#', ' ', '#', ' ', '#', ' ', '#', ' ', '#', '#', ' ', '#', ' ', '#'],
    ['#', ' ', '#', ' ', '#', ' ', '#', ' ', '#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#', ' ', '#'],
    ['#', ' ', '#', ' ', '#', ' ', '#', ' ', '#', '#', '#', '#', '#', '#', '#', '#', ' ', '#', ' ', '#'],
    ['#', ' ', '#', ' ', '#', ' ', '#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#', ' ', '#', ' ', '#'],
    ['#', ' ', '#', ' ', '#', ' ', '#', '#', '#', '#', '#', '#', '#', '#', ' ', '#', ' ', '#', ' ', '#'],
    ['#', ' ', '#', ' ', '#', ' ', '#', ' ', ' ', ' ', ' ', ' ', ' ', '#', ' ', '#', ' ', '#', ' ', '#'],
    ['#', ' ', '#', ' ', '#', ' ', '#', ' ', '#', '#', '#', '#', ' ', '#', ' ', '#', ' ', '#', ' ', '#'],
    ['#', ' ', '#', ' ', '#', ' ', '#', ' ', '#', ' ', ' ', '#', ' ', '#', ' ', '#', ' ', '#', ' ', '#'],
    ['#', ' ', '#', ' ', '#', ' ', '#', ' ', '#', ' ', '#', '#', ' ', '#', ' ', '#', ' ', '#', ' ', '#'],
    ['#', ' ', '#', ' ', '#', ' ', '#', ' ', '#', ' ', ' ', ' ', ' ', ' ', ' ', '#', ' ', '#', ' ', '#'],
    ['#', ' ', '#', ' ', '#', ' ', '#', ' ', '#', ' ', '#', '#', '#', '#', '#', '#', ' ', '#', ' ', '#'],
    ['#', ' ', ' ', ' ', '#', ' ', '#', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' ', ' ', ' ', '#', 'E', '#'],
    ['#', '#', '#', ' ', '#', '#', '#', '#', ' ', '#', '#', '#', '#', '#', '#', ' ', '#', '#', '#', '#'],
    ['#', '#', '#', ' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
    ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#']
]

player_row, player_col = 0, 0
for i in range(ROWS):
    for j in range(COLS):
        if maze[i][j] == 'S':
            player_row = i
            player_col = j

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Maze Game")

font = pygame.font.Font(None, 36)

def draw_maze():
    for i in range(ROWS):
        for j in range(COLS):
            cell = maze[i][j]
            if cell == '#':
                pygame.draw.rect(screen, WHITE, (j * 40, i * 40, 40, 40))
            elif cell == 'S':
                pygame.draw.rect(screen, GREEN, (j * 40, i * 40, 40, 40))
            elif cell == 'E':
                pygame.draw.rect(screen, RED, (j * 40, i * 40, 40, 40))
            else:
                pass

def move_player(new_row, new_col):
    global player_row, player_col
    if 0 <= new_row < ROWS and 0 <= new_col < COLS and maze[new_row][new_col] != '#':
        player_row = new_row
        player_col = new_col

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        move_player(player_row - 1, player_col)
    elif keys[pygame.K_LEFT]:
        move_player(player_row, player_col - 1) 
    elif keys[pygame.K_DOWN]:
        move_player(player_row + 1, player_col) 
    elif keys[pygame.K_RIGHT]:
        move_player(player_row, player_col + 1) 

    if maze[player_row][player_col] == 'E':
        print("Congratulations! You reached the end!")
        running = False

    screen.fill(BLACK)
    draw_maze()
    pygame.draw.rect(screen, BLUE, (player_col * 40, player_row * 40, 40, 40)) 
    pygame.display.flip()

    pygame.time.delay(100)

pygame.quit()
sys.exit()
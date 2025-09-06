import pygame
import random
from collections import deque

CELL_SIZE = 40
GRID_WIDTH = 10
GRID_HEIGHT = 10
SCREEN_WIDTH = CELL_SIZE * GRID_WIDTH
SCREEN_HEIGHT = CELL_SIZE * GRID_HEIGHT
FPS = 10

class CellType:
    EMPTY = 0
    WALL = 1
    PLAYER = 2
    BOT = 3

class Direction:
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

class Cell:
    def __init__(self, row, col, cell_type):
        self.row = row
        self.col = col
        self.cell_type = cell_type

class Game:
    def __init__(self):
        self.grid = [[Cell(row, col, CellType.EMPTY) for col in range(GRID_WIDTH)] for row in range(GRID_HEIGHT)]
        self.player_position = (0, 0)
        self.bot_positions = [(0, 0)]
        self.generate_level()
        self.last_bot_move_time = pygame.time.get_ticks()


    def generate_level(self):
        walls = [
            (0,7),
            (1,1), (1,2), (1,6), (1,9),
            (2,2), (2,5),
            (3,0), (3,7),
            (4,2), (4,3), (4,4), (4,7), (4,9),
            (5,1), (5,2), (5,4),
            (6,4), (6,8),
            (7,4), (7,8),
            (8,1), (8,8)
        ]

        for row in range(len(self.grid)):
            for col in range(len(self.grid[0])):
                if (row, col) in walls:
                    self.grid[row][col].cell_type = CellType.WALL
                
        self.player_position = self.get_random_empty_position()
        self.grid[self.player_position[1]][self.player_position[0]].cell_type = CellType.PLAYER

        self.bot_positions = []
        for _ in range(2):
            bot_position = self.get_random_empty_position()
            while self.calculate_distance(self.player_position, bot_position) < 5:
                bot_position = self.get_random_empty_position()
            self.bot_positions.append(bot_position)
            self.grid[bot_position[1]][bot_position[0]].cell_type = CellType.BOT

    def calculate_distance(self, position1, position2):
        return abs(position1[0] - position2[0]) + abs(position1[1] - position2[1])


    def get_random_empty_position(self):
        while True:
            row = random.randint(0, len(self.grid) - 1)
            col = random.randint(0, len(self.grid[0]) - 1)
            if self.grid[row][col].cell_type == CellType.EMPTY:
                return (col, row)

    def is_valid_position(self, position):
        col, row = position
        return 0 <= row < len(self.grid) and 0 <= col < len(self.grid[0])

    def is_empty_position(self, position):
        col, row = position
        return self.is_valid_position(position) and self.grid[row][col].cell_type == CellType.EMPTY

    def move_player(self, direction):
        new_position = (self.player_position[0] + direction[0], self.player_position[1] + direction[1])
        if self.is_empty_position(new_position):
            self.grid[self.player_position[1]][self.player_position[0]].cell_type = CellType.EMPTY
            self.player_position = new_position
            self.grid[self.player_position[1]][self.player_position[0]].cell_type = CellType.PLAYER

    def move_bots(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_bot_move_time >= 250: 
            for i, bot_position in enumerate(self.bot_positions):
                bot_direction = self.get_bot_direction(bot_position)
                new_position = (bot_position[0] + bot_direction[0], bot_position[1] + bot_direction[1])
                if self.is_empty_position(new_position):
                    self.grid[bot_position[1]][bot_position[0]].cell_type = CellType.EMPTY
                    self.bot_positions[i] = new_position
                    self.grid[new_position[1]][new_position[0]].cell_type = CellType.BOT
            self.last_bot_move_time = current_time 

            for bot_position in self.bot_positions:
                if bot_position == self.player_position:
                    print("Game Over - Player caught by a bot!")
                    return True 

        return False 

    def get_bot_direction(self, bot_position):
        if self.calculate_distance(bot_position, self.player_position) == 1:
            print("Player is adjacent to bot. Moving towards player.")
            return self.get_direction_towards_bot(bot_position, self.player_position)
        else:
            for bot_pos in self.bot_positions:
                if self.calculate_distance(bot_pos, self.player_position) == 1:
                    print("Player is adjacent to another bot. Waiting.")
                    return (0, 0) 

            print("Player is not adjacent to bot. Using BFS.")
            visited = {}
            queue = deque([(bot_position, 0, None)]) 
            while queue:
                current_position, distance, previous_position = queue.popleft()
                if current_position == self.player_position:
                    while previous_position != bot_position:
                        current_position = previous_position
                        previous_position = visited[current_position][1] 
                    return self.get_direction_towards_bot(bot_position, current_position)
                visited[current_position] = (distance, previous_position)  
                for direction in [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]:
                    new_position = (current_position[0] + direction[0], current_position[1] + direction[1])
                    if self.is_valid_position(new_position) and new_position not in visited and self.grid[new_position[1]][new_position[0]].cell_type != CellType.WALL:
                        queue.append((new_position, distance + 1, current_position))
            return (0, 0) 

    def get_direction_towards_bot(self, bot_position, player_position):
        dx = player_position[0] - bot_position[0]
        dy = player_position[1] - bot_position[1]
        if abs(dx) > abs(dy):
            return (1 if dx > 0 else -1, 0)
        else:
            return (0, 1 if dy > 0 else -1)

    def draw(self, screen):
        for row in range(len(self.grid)):
            for col in range(len(self.grid[0])):
                cell = self.grid[row][col]
                if cell.cell_type == CellType.WALL:
                    pygame.draw.rect(screen, (100, 100, 100), (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                elif cell.cell_type == CellType.PLAYER:
                    pygame.draw.rect(screen, (0, 255, 0), (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                elif cell.cell_type == CellType.BOT:
                    pygame.draw.rect(screen, (255, 0, 0), (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                else:
                    pygame.draw.rect(screen, (255, 255, 255), (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.display.flip()

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Pygame Pursuit Square")
    clock = pygame.time.Clock()

    game = Game()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            game.move_player(Direction.UP)
        elif keys[pygame.K_s]:
            game.move_player(Direction.DOWN)
        elif keys[pygame.K_a]:
            game.move_player(Direction.LEFT)
        elif keys[pygame.K_d]:
            game.move_player(Direction.RIGHT)

        game.move_bots()

        for bot_position in game.bot_positions:
            if game.calculate_distance(bot_position, game.player_position) == 1:
                print("Game Over - Player caught by a bot!")
                running = False
                break

        screen.fill((255, 255, 255))
        game.draw(screen)

        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()

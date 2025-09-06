import pygame
import sys
import random

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BLOCK_SIZE = 50
QUEUE_SIZE = 5

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Queue Sorting Game")

class Node:
    def __init__(self, data, next=None):
        self.data = data
        self.next = next

class Queue:
    def __init__(self):
        self.front = None
        self.rear = None

    def isEmpty(self):
        return self.front is None

    def enqueue(self, data):
        new_node = Node(data)
        if self.isEmpty():
            self.front = self.rear = new_node
        else:
            self.rear.next = new_node
            self.rear = new_node

    def dequeue(self):
        if self.isEmpty():
            print("Queue is empty.")
            pygame.quit()
            sys.exit()
        temp = self.front
        data = temp.data
        self.front = self.front.next
        if self.front is None:
            self.rear = None
        return data

def draw_queue(queue):
    total_width = QUEUE_SIZE * BLOCK_SIZE
    start_x = (SCREEN_WIDTH - total_width) // 2
    start_y = (SCREEN_HEIGHT - BLOCK_SIZE) // 2

    current = queue.front
    for i in range(QUEUE_SIZE):
        if current:
            pygame.draw.rect(screen, WHITE, (start_x + i * BLOCK_SIZE, start_y, BLOCK_SIZE, BLOCK_SIZE))
            font = pygame.font.SysFont(None, 36)
            text = font.render(str(current.data), True, BLACK)
            text_width, text_height = font.size(str(current.data))
            screen.blit(text, (start_x + i * BLOCK_SIZE + BLOCK_SIZE // 2 - text_width // 2,
                               start_y + BLOCK_SIZE // 2 - text_height // 2))
            current = current.next
        else:
            pygame.draw.rect(screen, WHITE, (start_x + i * BLOCK_SIZE, start_y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(screen, RED, (start_x + i * BLOCK_SIZE + 10, start_y + 10,
                                           BLOCK_SIZE - 20, BLOCK_SIZE - 20))


def move1(queue):
    if queue.isEmpty() or queue.front.next is None:
        print("Not enough elements to perform move 1.")
        return
    temp = queue.front.data
    queue.front.data = queue.front.next.data
    queue.front.next.data = temp

# Function to perform move 2
def move2(queue):
    if queue.isEmpty() or queue.front == queue.rear:
        print("Not enough elements to perform move 2.")
        return
    data = queue.dequeue()
    queue.enqueue(data)

def isSorted(queue):
    if queue.isEmpty() or queue.front == queue.rear:
        return True
    current = queue.front
    while current.next:
        if current.data > current.next.data:
            return False
        current = current.next
    return True

def play_game(queue):
    moves = 0
    while not isSorted(queue):
        draw_queue(queue)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    move1(queue)
                    moves += 1
                elif event.key == pygame.K_2:
                    move2(queue)
                    moves += 1

        screen.fill(BLACK)
        draw_queue(queue)
        pygame.display.flip()

    print("Congratulations! You sorted the queue in", moves, "moves.")

def main():
    queue = Queue()

    for _ in range(QUEUE_SIZE):
        data = random.randint(0, 99)
        queue.enqueue(data)

    play_game(queue)

if __name__ == "__main__":
    main()

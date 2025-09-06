import pygame
import random

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GRAY = (200, 200, 200)
BLUE = (173, 216, 230)

WIDTH = 50
HEIGHT = 50
MARGIN = 5

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

def create_linked_list(sequence):
    head = None
    tail = None

    for data in sequence:
        new_node = Node(data)

        if head is None:
            head = tail = new_node
        else:
            tail.next = new_node
            tail = new_node

    return head

def shuffle_linked_list(head):
    nodes = []
    current = head
    while current:
        nodes.append(current)
        current = current.next

    random.shuffle(nodes)

    for i in range(len(nodes) - 1):
        nodes[i].next = nodes[i + 1]
    nodes[-1].next = None

    return nodes[0]

def display_linked_list(screen, head, bracket1, bracket2):
    font = pygame.font.SysFont(None, 24)
    current = head
    x = MARGIN
    y = MARGIN
    index = 0
    while current:
        if index == bracket1 or index == bracket2:
            pygame.draw.rect(screen, BLUE, [(MARGIN + WIDTH) * index, MARGIN, WIDTH, HEIGHT])
        else:
            pygame.draw.rect(screen, GRAY, [(MARGIN + WIDTH) * index, MARGIN, WIDTH, HEIGHT])

        text = font.render(str(current.data), True, BLACK)
        screen.blit(text, (x + 15, y + 15))
        x += WIDTH + MARGIN

        current = current.next
        index += 1

def is_sorted(head):
    while head and head.next:
        if head.data > head.next.data:
            return False
        head = head.next
    return True

def swap_nodes(head, index1, index2):
    if index1 == index2:
        return head

    prevX, currX = None, head
    for _ in range(index1):
        prevX, currX = currX, currX.next

    prevY, currY = None, head
    for _ in range(index2):
        prevY, currY = currY, currY.next

    if prevX:
        prevX.next = currY
    else:
        head = currY

    if prevY:
        prevY.next = currX
    else:
        head = currX

    currX.next, currY.next = currY.next, currX.next

    return head

def play_game(screen, head):
    selectedIndex1 = 0
    selectedIndex2 = 1
    bracket1 = 0
    bracket2 = 1
    printSequence = True

    pygame.init()
    screen.fill(WHITE)
    font = pygame.font.SysFont(None, 24)
    clock = pygame.time.Clock()

    print("Welcome to the Sequence Arrangement Puzzle!")
    print("You need to rearrange the scrambled sequence to unlock the door.")

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if not is_sorted(head):
            if printSequence:
                screen.fill(WHITE)
                display_linked_list(screen, head, bracket1, bracket2)
                pygame.display.flip()
                printSequence = False

            keys = pygame.key.get_pressed()
            if keys[pygame.K_a]:
                if bracket1 > 0:
                    bracket1 -= 1
                    bracket2 -= 1
                    selectedIndex1 -= 1
                    selectedIndex2 -= 1
                    printSequence = True
            elif keys[pygame.K_d]:
                if bracket2 < 3:
                    bracket1 += 1
                    bracket2 += 1
                    selectedIndex1 += 1
                    selectedIndex2 += 1
                    printSequence = True
            elif keys[pygame.K_x]:
                head = swap_nodes(head, selectedIndex1, selectedIndex2)
                printSequence = True

            clock.tick(10)

        else:
            screen.fill(WHITE)
            display_linked_list(screen, head, bracket1, bracket2)
            text = font.render("Congratulations! You unscrambled the sequence and unlocked the door!", True, RED)
            screen.blit(text, (50, 250))
            pygame.display.flip()
            pygame.time.delay(3000)
            running = False

    pygame.quit()

def free_linked_list(head):
    while head:
        temp = head
        head = head.next
        temp = None

if __name__ == "__main__":
    sequence = [3, 1, 4, 2]
    head = create_linked_list(sequence)
    head = shuffle_linked_list(head)
    WINDOW_SIZE = [(WIDTH + MARGIN) * len(sequence) + MARGIN, HEIGHT + 2 * MARGIN]
    screen = pygame.display.set_mode(WINDOW_SIZE)
    play_game(screen, head)
    free_linked_list(head)


import pygame
import random
from environment import draw_maze, generate_maze
from agent import Mouse
from levels import MAZE_SIZES
from agent import Mouse, CELL_SIZE
from collections import deque
import os
from pathlib import Path


def is_reachable(start, goal, maze):
    queue = deque([start])
    visited = set([start])
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    while queue:
        x, y = queue.popleft()
        if (x, y) == goal:
            return True

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if (0 <= nx < len(maze[0]) and 0 <= ny < len(maze)
                and maze[ny][nx] in (0, 2)
                and (nx, ny) not in visited):
                visited.add((nx, ny))
                queue.append((nx, ny))
    return False


CELL_SIZE = 40
cheese_collected = False

# User level select
level_choice = input("Select level (1 = Easy, 2 = Medium, 3 = Hard): ")
if level_choice not in ["1", "2", "3"]:
    print("Defaulting to Level 1")
    level_choice = "1"

level_index = int(level_choice) - 1
maze_size = MAZE_SIZES[level_index]
maze, actual_width, actual_height = generate_maze(*maze_size)


CHEESE_POSITIONS = []

while len(CHEESE_POSITIONS) < 5:
    x = random.randint(0, actual_width - 1)
    y = random.randint(0, actual_height - 1)
    pos = (x, y)

    if (
        y < len(maze) and
        x < len(maze[0]) and
        maze[y][x] in (0, 2) and
        pos != (0, 0) and
        is_reachable((0, 0), pos, maze)
    ):
        CHEESE_POSITIONS.append(pos)


CHEESE_POSITIONS.append((actual_width - 1, actual_height - 1))

WINDOW_WIDTH = actual_width * CELL_SIZE
WINDOW_HEIGHT = actual_height * CELL_SIZE

pygame.init()

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

mode_choice = input("Select movement mode (1 = Random, 2 = A*, 3 = Greedy, 4 = BFS, 5 = UCS): ")
if mode_choice == "1":
    mode = "random"
elif mode_choice == "2":
    mode = "a_star"
elif mode_choice == "3":
    mode = "greedy"
elif mode_choice == "4":
    mode = "bfs"
elif mode_choice == "5":
    mode = "ucs"
else:
    print("Invalid mode selected. Defaulting to random.")
    mode = "random"

noise_choice = input("Enable noisy perception? (y/n): ")
is_noisy = noise_choice.strip().lower() == "y"

mouse = Mouse(start_pos=(0, 0), noisy_perception=is_noisy)
mouse.set_mode(mode, CHEESE_POSITIONS[0], maze)

pygame.display.set_caption("Mouse and Cheese Maze")
clock = pygame.time.Clock()

mouse_img = pygame.image.load("assets/mouse.png")
mouse_img = pygame.transform.scale(mouse_img, (CELL_SIZE, CELL_SIZE))
cheese_img = pygame.image.load("assets/cheese.png")
cheese_img = pygame.transform.scale(cheese_img, (CELL_SIZE, CELL_SIZE))

MOVE_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(MOVE_EVENT, 150) 

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == MOVE_EVENT:
            mouse.move(maze, screen=screen, draw_fn=draw_maze, mouse_img=mouse_img, cheese_img=cheese_img,cheese_positions=CHEESE_POSITIONS)


            # Check if cheese collected
            for cheese_pos in CHEESE_POSITIONS[:]:  
                if mouse.position == cheese_pos:
                    CHEESE_POSITIONS.remove(cheese_pos)
                    print("Collected a cheese!")

                    # Update target if cheeses remain
                    if CHEESE_POSITIONS:
                        closest = min(CHEESE_POSITIONS, key=lambda pos: mouse.heuristic(mouse.position, pos))
                        mouse.set_mode(mode, closest, maze)

    # Drawing
    screen.fill((255, 255, 255))
    draw_maze(screen, maze)

    # Draw all cheeses
    for cheese_pos in CHEESE_POSITIONS:
        screen.blit(cheese_img, (cheese_pos[0] * CELL_SIZE, cheese_pos[1] * CELL_SIZE))

    if len(mouse.path_taken) > 1:
        pygame.draw.lines(
            screen,
            (0, 0, 255),     
            False,            
            [(x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2) for (x, y) in mouse.path_taken],
            3                 
        )

    # Draw mouse
    mouse.draw(screen, mouse_img)

    pygame.display.flip()
    clock.tick(30)

    # End condition
    if not CHEESE_POSITIONS:
        print("All cheese collected!")
        print(f"Replans due to noise: {mouse.replans_due_to_noise}")
        downloads_path = str(Path.home() / "Downloads")
        pygame.image.save(screen, os.path.join(downloads_path, f"level{level_index+1}_{mode}.png"))
        running = False


pygame.quit()


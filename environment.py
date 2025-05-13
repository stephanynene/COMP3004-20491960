import random
import pygame
from agent import CELL_SIZE


def draw_maze(screen, maze):
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREY = (200, 200, 200)

    # maze's dimensions dynamically
    maze_height = len(maze)
    maze_width = len(maze[0]) if maze_height > 0 else 0

    # Draw maze grid
    for y in range(maze_height):
        for x in range(maze_width):
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if maze[y][x] == 1:
                pygame.draw.rect(screen, BLACK, rect)  # Wall
            elif maze[y][x] == 2:
                pygame.draw.rect(screen, (139, 69, 19), rect)  # Mud tile (brown)
            else:
                pygame.draw.rect(screen, WHITE, rect)  # Path
            pygame.draw.rect(screen, GREY, rect, 1)  # Grid lines


def generate_maze(width, height):
    width = width if width % 2 == 1 else width - 1
    height = height if height % 2 == 1 else height - 1

    maze = [[1 for _ in range(width)] for _ in range(height)]

    def carve(x, y):
        directions = [(0, -2), (0, 2), (-2, 0), (2, 0)]
        random.shuffle(directions)
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 1 <= nx < width - 1 and 1 <= ny < height - 1 and maze[ny][nx] == 1:
                maze[ny - dy // 2][nx - dx // 2] = 0
                maze[ny][nx] = 0
                carve(nx, ny)

    maze[1][1] = 0
    carve(1, 1)

    # Ensure start and goal are accessible
    maze[0][0] = 0
    maze[0][1] = 0
    maze[1][0] = 0

    goal_x, goal_y = width - 1, height - 1
    maze[goal_y][goal_x] = 0

    # Random mud tiles on paths
    for y in range(height):
        for x in range(width):
            if maze[y][x] == 0 and random.random() < 0.3:
                maze[y][x] = 2  # mud

    # Add muddy shortcut, diagonal-ish path from (0, 0) to (goal_x, goal_y)
    x, y = 0, 0
    while x < goal_x and y < goal_y:
        x += 1
        y += 1
        if x < width and y < height:
            maze[y][x] = 2  # force mud
            if maze[y-1][x] == 1:
                maze[y-1][x] = 0  # make adjacent cell walkable to blend with maze

    x, y = 0, 0
    for _ in range(3):
        if x + 1 < width:
            x += 1
            maze[y][x] = 0
    while y + 1 < height:
        y += 1
        maze[y][x] = 0
    while x + 1 < width:
        x += 1
        maze[y][x] = 0

    return maze, width, height

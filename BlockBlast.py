import pygame
import sys
import random  # Import the random module

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 600, 600
GRID_SIZE = 10
CELL_SIZE = WIDTH // GRID_SIZE
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Block Blast Clone")

# Colors
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Define some shapes and their colors
SHAPES = {
    "square": [[0, 0], [0, 1], [1, 0], [1, 1]],  # 2x2 square
    "line": [[0, 0], [0, 1], [0, 2]],  # 1x3 line
    "L": [[0, 0], [1, 0], [1, 1]],  # L-shape
}

SHAPE_COLORS = {
    "square": RED,
    "line": GREEN,
    "L": BLUE,
}

# Grid state (10x10 grid of zeros)
GRID = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

# Function to draw the grid state
def draw_grid_state():
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            color = WHITE if GRID[row][col] == 0 else GRAY
            pygame.draw.rect(screen, color, 
                             (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, GRAY, 
                             (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

# Function to draw a shape at a position
def draw_shape(shape, position):
    shape_color = SHAPE_COLORS.get(current_shape_name, BLUE)  # Get the shape's color
    for block in shape:
        x, y = position[0] + block[1], position[1] + block[0]
        pygame.draw.rect(screen, shape_color, 
                         (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

# Place shape on the grid
def place_shape_on_grid(shape, position):
    for block in shape:
        x, y = position[0] + block[1], position[1] + block[0]
        if 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE:
            GRID[y][x] = 1

# Check and clear full lines
def clear_full_lines():
    global GRID
    cleared = 0

    # Check rows
    GRID = [row for row in GRID if any(cell == 0 for cell in row)]
    cleared += GRID_SIZE - len(GRID)

    # Add empty rows at the top
    for _ in range(cleared):
        GRID.insert(0, [0] * GRID_SIZE)

    return cleared  # Return the number of cleared lines

# Check if the shape can be placed at the given position
def can_place_shape(shape, position):
    for block in shape:
        x, y = position[0] + block[1], position[1] + block[0]
        if not (0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE) or GRID[y][x] != 0:
            return False
    return True

# Handle dragging
dragging = False
current_shape = None
current_position = [0, 0]
current_shape_name = ""

# Function to handle events like dragging shapes
def handle_dragging(event):
    global dragging, current_shape, current_position, current_shape_name

    if event.type == pygame.MOUSEBUTTONDOWN:
        dragging = True
        # Randomly pick a shape from SHAPES
        current_shape_name = random.choice(list(SHAPES.keys()))  # Pick a random shape name
        current_shape = SHAPES[current_shape_name]  # Get the corresponding shape
    elif event.type == pygame.MOUSEBUTTONUP:
        dragging = False
        if can_place_shape(current_shape, current_position):
            place_shape_on_grid(current_shape, current_position)
    elif event.type == pygame.MOUSEMOTION and dragging:
        x, y = event.pos
        new_position = [x // CELL_SIZE, y // CELL_SIZE]
        
        # Prevent moving the shape off-screen
        if 0 <= new_position[0] < GRID_SIZE - max(block[1] for block in current_shape):
            current_position[0] = new_position[0]
        if 0 <= new_position[1] < GRID_SIZE - max(block[0] for block in current_shape):
            current_position[1] = new_position[1]

# Main game loop
def main():
    global dragging

    clock = pygame.time.Clock()
    running = True
    score = 0

    while running:
        screen.fill(WHITE)
        draw_grid_state()

        # Draw the current shape if dragging
        if dragging and current_shape:
            draw_shape(current_shape, current_position)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            handle_dragging(event)

        # Clear lines and update the score
        score += clear_full_lines()

        # Display the score
        font = pygame.font.SysFont("Arial", 24)
        score_text = font.render(f"Score: {score}", True, RED)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

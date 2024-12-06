import pygame
import sys

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
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Define some shapes
SHAPES = {
    "square": [[0, 0], [0, 1], [1, 0], [1, 1]],
    "line": [[0, 0], [0, 1], [0, 2]],
    "L": [[0, 0], [1, 0], [1, 1]]
}

# Grid state (10x10 grid of zeros)
GRID = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

# Function to draw the grid state
def draw_grid_state():
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            color = BLUE if GRID[row][col] == 1 else WHITE
            pygame.draw.rect(screen, color, 
                             (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, GRAY, 
                             (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

# Function to draw a shape at a position
def draw_shape(shape, position):
    for block in shape:
        x, y = position[0] + block[1], position[1] + block[0]
        pygame.draw.rect(screen, BLUE, 
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

# Handle dragging
dragging = False
current_shape = None
current_position = [0, 0]

# Function to handle events like dragging shapes
def handle_dragging(event):
    global dragging, current_shape, current_position

    if event.type == pygame.MOUSEBUTTONDOWN:
        dragging = True
        current_shape = SHAPES["square"]  # Pick a shape for now
    elif event.type == pygame.MOUSEBUTTONUP:
        dragging = False
        place_shape_on_grid(current_shape, current_position)
    elif event.type == pygame.MOUSEMOTION and dragging:
        x, y = event.pos
        current_position = [x // CELL_SIZE, y // CELL_SIZE]

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

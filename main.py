import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 800
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Cat Chi")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Grid dimensions
grid_size = 5
cell_size = 100
grid_origin = ((screen_width - (grid_size * cell_size)) // 2, (screen_height - (grid_size * cell_size) - 120))  # Center the grid and leave space for end text

# Load and resize images
cat_img = pygame.image.load('cat.jpg')
cat_img = pygame.transform.scale(cat_img, (100, 100))

# Fonts
font = pygame.font.Font(None, 24)  # Smaller font size for cell text
title_font = pygame.font.Font(None, 48)
end_font = pygame.font.Font(None, 24)  # Smaller font size for end screen

# Grid positions
grid_positions = [(grid_origin[0] + x * cell_size, grid_origin[1] + y * cell_size) 
                  for y in range(grid_size) for x in range(grid_size)]

# Define immovable objects positions for each level
def generate_immovable_objects(level):
    edge_positions = []

    # Collect edge positions
    for x in range(grid_size):
        edge_positions.append((grid_origin[0] + x * cell_size, grid_origin[1]))  # Top edge
        edge_positions.append((grid_origin[0] + x * cell_size, grid_origin[1] + (grid_size - 1) * cell_size))  # Bottom edge
    for y in range(1, grid_size - 1):
        edge_positions.append((grid_origin[0], grid_origin[1] + y * cell_size))  # Left edge
        edge_positions.append((grid_origin[0] + (grid_size - 1) * cell_size, grid_origin[1] + y * cell_size))  # Right edge

    # Ensure there's no overlap and set specific items for each level
    if level == 0:  # Bedroom
        return {
            "Door": edge_positions.pop(random.randint(0, len(edge_positions) - 1)),
            "Window1": edge_positions.pop(random.randint(0, len(edge_positions) - 1)),
            "Window2": edge_positions.pop(random.randint(0, len(edge_positions) - 1)),
            "Chair": edge_positions.pop(random.randint(0, len(edge_positions) - 1)),
            "Table": edge_positions.pop(random.randint(0, len(edge_positions) - 1)),
            "Nightstand": edge_positions.pop(random.randint(0, len(edge_positions) - 1))
        }
    elif level == 1:  # Office
        return {
            "Door": edge_positions.pop(random.randint(0, len(edge_positions) - 1)),
            "Window1": edge_positions.pop(random.randint(0, len(edge_positions) - 1)),
            "Window2": edge_positions.pop(random.randint(0, len(edge_positions) - 1)),
            "Chair": edge_positions.pop(random.randint(0, len(edge_positions) - 1)),
            "Table": edge_positions.pop(random.randint(0, len(edge_positions) - 1)),
            "Bookcase": edge_positions.pop(random.randint(0, len(edge_positions) - 1))
        }
    elif level == 2:  # Living Room
        return {
            "Door": edge_positions.pop(random.randint(0, len(edge_positions) - 1)),
            "Window1": edge_positions.pop(random.randint(0, len(edge_positions) - 1)),
            "Window2": edge_positions.pop(random.randint(0, len(edge_positions) - 1)),
            "Chair": edge_positions.pop(random.randint(0, len(edge_positions) - 1)),
            "Table": edge_positions.pop(random.randint(0, len(edge_positions) - 1)),
            "TV": edge_positions.pop(random.randint(0, len(edge_positions) - 1))
        }

# Levels and Objectives
levels = [
    {"name": "Bedroom", "object": "Bed", "correct_pos": grid_positions[12], "text": "Find the best place for the bed"},
    {"name": "Office", "object": "Desk", "correct_pos": grid_positions[12], "text": "Find the best place for the desk"},
    {"name": "Living Room", "object": "Couch", "correct_pos": grid_positions[12], "text": "Find the best place for the couch"}
]

current_level = 0
immovable_objects = generate_immovable_objects(current_level)

# Draggable Class
class Draggable:
    def __init__(self, text, position):
        self.text = text
        self.image = font.render(text, True, WHITE)
        self.rect = self.image.get_rect(topleft=position)
        self.dragging = False

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.dragging = True
                self.mouse_x, self.mouse_y = event.pos
                self.offset_x = self.rect.x - self.mouse_x
                self.offset_y = self.rect.y - self.mouse_y
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
            # Snap to grid
            self.snap_to_grid()
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                self.mouse_x, self.mouse_y = event.pos
                self.rect.x = self.mouse_x + self.offset_x
                self.rect.y = self.mouse_y + self.offset_y

    def snap_to_grid(self):
        closest_pos = min(grid_positions, key=lambda pos: (pos[0] - self.rect.x) ** 2 + (pos[1] - self.rect.y) ** 2)
        self.rect.topleft = closest_pos

# Create draggable objects for each level
def create_draggable_objects():
    return [Draggable(level["object"], (grid_origin[0], grid_origin[1])) for level in levels if levels.index(level) == current_level]

# Draw the grid
def draw_grid(surface):
    for x in range(grid_size + 1):
        pygame.draw.line(surface, WHITE, 
                         (grid_origin[0] + x * cell_size, grid_origin[1]), 
                         (grid_origin[0] + x * cell_size, grid_origin[1] + grid_size * cell_size))
    for y in range(grid_size + 1):
        pygame.draw.line(surface, WHITE, 
                         (grid_origin[0], grid_origin[1] + y * cell_size), 
                         (grid_origin[0] + grid_size * cell_size, grid_origin[1] + y * cell_size))
    
    # Draw cell text
    for pos in grid_positions:
        cell_text = font.render(" ", True, WHITE)
        text_rect = cell_text.get_rect(center=(pos[0] + cell_size // 2, pos[1] + cell_size // 2))
        surface.blit(cell_text, text_rect)

# Draw the background
def draw_background(surface):
    surface.fill(BLACK)

# Evaluate feng shui score (simple example)
def evaluate_feng_shui(draggable):
    return draggable.rect.topleft == levels[current_level]["correct_pos"]

# Draw immovable objects
def draw_immovable_objects(surface):
    for obj, pos in immovable_objects.items():
        text_surface = font.render(obj, True, WHITE)
        text_rect = text_surface.get_rect(center=(pos[0] + cell_size // 2, pos[1] + cell_size // 2))
        surface.blit(text_surface, text_rect)

# Draw the title and image
def draw_title(surface):
    title_text = title_font.render("Cat Chi", True, WHITE)
    title_rect = title_text.get_rect(center=(screen_width // 2, 50))
    surface.blit(title_text, title_rect)
    surface.blit(cat_img, (20, 20))

# Main game loop
def main():
    global current_level, immovable_objects
    clock = pygame.time.Clock()
    draggable_objects = create_draggable_objects()
    game_over = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if not game_over:
                for obj in draggable_objects:
                    obj.handle_event(event)

        if not game_over:
            screen.fill(BLACK)
            draw_background(screen)
            draw_title(screen)
            draw_grid(screen)
            draw_immovable_objects(screen)
            for obj in draggable_objects:
                obj.draw(screen)

            level_title = title_font.render(f"Level: {current_level + 1} - {levels[current_level]['name']}", True, WHITE)
            title_rect = level_title.get_rect(center=(screen_width // 2, grid_origin[1] - 40))
            screen.blit(level_title, title_rect)

            instructions_text = font.render(levels[current_level]["text"], True, WHITE)
            instructions_rect = instructions_text.get_rect(center=(screen_width // 2, grid_origin[1] - 20))
            screen.blit(instructions_text, instructions_rect)

            if all(evaluate_feng_shui(obj) for obj in draggable_objects):
                success_text = font.render("Great job! Moving to the next level...", True, WHITE)
                screen.blit(success_text, (screen_width // 2 - success_text.get_width() // 2, screen_height - 100))
                pygame.display.flip()
                pygame.time.wait(2000)  # Wait for 2 seconds
                current_level += 1
                if current_level >= len(levels):
                    game_over = True
                else:
                    immovable_objects = generate_immovable_objects(current_level)
                    draggable_objects = create_draggable_objects()
                continue

            pygame.display.flip()
            clock.tick(60)
        else:
            screen.fill(BLACK)
            draw_background(screen)
            draw_grid(screen)
            draw_immovable_objects(screen)
            end_text = end_font.render("Congratulations! You've completed all levels!", True, WHITE)
            screen.blit(end_text, (screen_width // 2 - end_text.get_width() // 2, grid_origin[1] + (grid_size * cell_size) + 20))
            pygame.display.flip()
            clock.tick(60)

if __name__ == "__main__":
    main()

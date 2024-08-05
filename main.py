import pygame
import sys
import random

pygame.init()

# Screen dimensions
screen_width = 800
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Cat Chi")

# Grid dimensions
grid_size = 5
cell_size = 100
grid_origin = ((screen_width - (grid_size * cell_size)) // 2, (screen_height - (grid_size * cell_size)) // 2 + 50)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Fonts
font = pygame.font.Font(None, 24)
title_font = pygame.font.Font(None, 48)
end_font = pygame.font.Font(None, 24)

# Images
cat_img = pygame.image.load('cat.jpg')
cat_img = pygame.transform.scale(cat_img, (100, 100))
heart_img = pygame.image.load('heart.jpg')
heart_img = pygame.transform.scale(heart_img, (30, 30))

grid_positions = [(grid_origin[0] + x * cell_size, grid_origin[1] + y * cell_size) for y in range(grid_size) for x in range(grid_size)]

def generate_immovable_objects(level):
    edge_positions = []

    for x in range(grid_size):
        edge_positions.append((grid_origin[0] + x * cell_size, grid_origin[1]))  # Top edge
        edge_positions.append((grid_origin[0] + x * cell_size, grid_origin[1] + (grid_size - 1) * cell_size))  # Bottom edge
    for y in range(1, grid_size - 1):
        edge_positions.append((grid_origin[0], grid_origin[1] + y * cell_size))  # Left edge
        edge_positions.append((grid_origin[0] + (grid_size - 1) * cell_size, grid_origin[1] + y * cell_size))  # Right edge

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
lives = 3
game_over = False

class Draggable:
    def __init__(self, text, position):
        self.text = text
        self.image = font.render(text, True, BLACK)
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
            # Check if placed correctly
            if not evaluate_feng_shui(self):
                global lives
                lives -= 1
                if lives == 0:
                    global game_over
                    game_over = True
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                self.mouse_x, self.mouse_y = event.pos
                self.rect.x = self.mouse_x + self.offset_x
                self.rect.y = self.mouse_y + self.offset_y

    def snap_to_grid(self):
        closest_pos = min(grid_positions, key=lambda pos: (pos[0] - self.rect.x) ** 2 + (pos[1] - self.rect.y) ** 2)
        self.rect.topleft = closest_pos

def create_draggable_objects():
    return [Draggable(level["object"], (grid_origin[0], grid_origin[1])) for level in levels if levels.index(level) == current_level]

def draw_grid(surface):
    for x in range(grid_size + 1):
        pygame.draw.line(surface, BLACK, 
                         (grid_origin[0] + x * cell_size, grid_origin[1]), 
                         (grid_origin[0] + x * cell_size, grid_origin[1] + grid_size * cell_size))
    for y in range(grid_size + 1):
        pygame.draw.line(surface, BLACK, 
                         (grid_origin[0], grid_origin[1] + y * cell_size), 
                         (grid_origin[0] + grid_size * cell_size, grid_origin[1] + y * cell_size))
    
    for pos in grid_positions:
        cell_text = font.render(" ", True, BLACK)
        text_rect = cell_text.get_rect(center=(pos[0] + cell_size // 2, pos[1] + cell_size // 2))
        surface.blit(cell_text, text_rect)

def draw_background(surface):
    surface.fill(WHITE)

def evaluate_feng_shui(draggable):
    return draggable.rect.topleft == levels[current_level]["correct_pos"]

def draw_immovable_objects(surface):
    for obj, pos in immovable_objects.items():
        text_surface = font.render(obj, True, BLACK)
        text_rect = text_surface.get_rect(center=(pos[0] + cell_size // 2, pos[1] + cell_size // 2))
        surface.blit(text_surface, text_rect)

def draw_title(surface):
    title_text = title_font.render("Cat Chi", True, BLACK)
    title_rect = title_text.get_rect(center=(screen_width // 2, 50))
    surface.blit(title_text, title_rect)
    surface.blit(cat_img, (20, 20))

def draw_level_info(surface, level, objective):
    level_text = font.render(f"Level: {level}", True, BLACK)
    level_rect = level_text.get_rect(center=(screen_width // 2, grid_origin[1] - 50))
    surface.blit(level_text, level_rect)

    objective_text = font.render(f"Objective: {objective}", True, BLACK)
    objective_rect = objective_text.get_rect(center=(screen_width // 2, grid_origin[1] - 30))
    surface.blit(objective_text, objective_rect)

def draw_lives(surface, lives):
    for i in range(lives):
        surface.blit(heart_img, (screen_width - 40 - i * 40, 20))

def draw_game_over(surface):
    game_over_text = end_font.render("Game Over! Press R to Restart.", True, BLACK)
    game_over_rect = game_over_text.get_rect(center=(screen_width // 2, screen_height - 50))
    surface.blit(game_over_text, game_over_rect)

def reset_game():
    global current_level, immovable_objects, lives, game_over
    current_level = 0
    immovable_objects = generate_immovable_objects(current_level)
    lives = 3
    game_over = False

# Main game loop
def main():
    global current_level, immovable_objects, lives, game_over
    clock = pygame.time.Clock()
    draggable_objects = create_draggable_objects()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if game_over and event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                reset_game()
                draggable_objects = create_draggable_objects()

            for obj in draggable_objects:
                obj.handle_event(event)

        draw_background(screen)
        draw_title(screen)
        draw_grid(screen)
        draw_immovable_objects(screen)

        if not game_over:
            for obj in draggable_objects:
                obj.draw(screen)
            draw_lives(screen, lives)
            draw_level_info(screen, levels[current_level]["name"], levels[current_level]["text"])

            if evaluate_feng_shui(draggable_objects[0]):
                current_level += 1
                if current_level >= len(levels):
                    game_over = True
                else:
                    immovable_objects = generate_immovable_objects(current_level)
                    draggable_objects = create_draggable_objects()
                    lives = 3  # Reset lives for the new level

        else:
            draw_game_over(screen)

        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()

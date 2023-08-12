
import pygame
import sys
import click
from pydantic import BaseModel

from wkg.models import Box

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600

# Colors
WHITE = (255, 255, 255)
BROWN = (139, 69, 19)
BLACK = (0, 0, 0)

# Create screen and clock objects
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Geometry Render")
clock = pygame.time.Clock()

# Font setup
font = pygame.font.SysFont(None, 36)

# Scaling factor for visualization
SCALE = 20
class PygameRenderer:

    @staticmethod
    def draw_box(box_obj: Box, orientation="front"):
        if orientation == "front":
            base_x = 0
            base_y = 0
            rect = (base_x + SCALE * box_obj.start.x, HEIGHT - SCALE * (box_obj.end.y + box_obj.start.z),
                    SCALE * (box_obj.end.x - box_obj.start.x), SCALE * (box_obj.end.y - box_obj.start.y))
            pygame.draw.rect(screen, BROWN, rect)
            pygame.draw.rect(screen, BLACK, rect, 2)
            text_surface = font.render("Front", True, BLACK)
            screen.blit(text_surface, (base_x + 10, 10))

        elif orientation == "side":
            base_x = WIDTH // 3
            base_y = 0
            rect = (base_x + SCALE * box_obj.start.z, HEIGHT - SCALE * (box_obj.end.y + box_obj.start.x),
                    SCALE * (box_obj.end.z - box_obj.start.z), SCALE * (box_obj.end.y - box_obj.start.y))
            pygame.draw.rect(screen, BROWN, rect)
            pygame.draw.rect(screen, BLACK, rect, 2)
            text_surface = font.render("Side", True, BLACK)
            screen.blit(text_surface, (base_x + 10, 10))

        elif orientation == "top":
            base_x = 2 * WIDTH // 3
            base_y = 0
            rect = (base_x + SCALE * box_obj.start.x, HEIGHT - SCALE * (box_obj.start.y + box_obj.start.z),
                    SCALE * (box_obj.end.x - box_obj.start.x), SCALE * (box_obj.end.z - box_obj.start.z))
            pygame.draw.rect(screen, BROWN, rect)
            pygame.draw.rect(screen, BLACK, rect, 2)
            text_surface = font.render("Top", True, BLACK)
            screen.blit(text_surface, (base_x + 10, 10))

    @staticmethod
    def render_loop():
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.flip()
            clock.tick(60)

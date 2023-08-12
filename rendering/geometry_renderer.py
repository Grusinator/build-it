import click
import pygame

from rendering.pygame_renderer import PygameRenderer
from wkg.geometry_parser import load_geometries_from_file

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600

# Colors
WHITE = (255, 255, 255)
BROWN = (139, 69, 19)
BLACK = (0, 0, 0)


class GeometryRenderer:

    def __init__(self, boxes, renderer):
        self.boxes = boxes
        self.renderer = renderer

    def render(self):
        for box_obj in self.boxes:
            # Drawing the boxes in different orientations
            self.renderer.draw_box(box_obj, "front")
            self.renderer.draw_box(box_obj, "side")
            self.renderer.draw_box(box_obj, "top")
        self.renderer.render_loop()

@click.command()
@click.argument('path', type=click.Path(exists=True))
def main(path):
    """Renders geometry from a specified file."""
    boxes = load_geometries_from_file(path)
    geometry_renderer = GeometryRenderer(boxes, PygameRenderer())
    geometry_renderer.render()

if __name__ == "__main__":
    main()

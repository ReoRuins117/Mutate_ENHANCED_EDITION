# ui/render.py

import pygame
from config import TILE_SIZE, WORLD_WIDTH, WORLD_HEIGHT

BACKGROUND_COLOR = (20, 20, 20)
GRID_COLOR = (40, 40, 40)
PLANT_COLOR = (50, 180, 50)

HP_BAR_COLOR = (200, 50, 50)
ENERGY_BAR_COLOR = (50, 150, 250)

class Renderer:
    def __init__(self, screen, world):
        self.screen = screen
        self.world = world
        self.font = pygame.font.SysFont("consolas", 12)

    def world_to_screen(self, pos):
        x, y = pos
        return int(x * TILE_SIZE), int(y * TILE_SIZE)

    def draw(self):
        self.screen.fill(BACKGROUND_COLOR)
        self._draw_grid()
        self._draw_plants()
        self._draw_creatures()
        pygame.display.flip()

    def _draw_grid(self):
        for x in range(WORLD_WIDTH):
            sx = x * TILE_SIZE
            pygame.draw.line(self.screen, GRID_COLOR, (sx, 0), (sx, WORLD_HEIGHT * TILE_SIZE))
        for y in range(WORLD_HEIGHT):
            sy = y * TILE_SIZE
            pygame.draw.line(self.screen, GRID_COLOR, (0, sy), (WORLD_WIDTH * TILE_SIZE, sy))

    def _draw_plants(self):
        for plant in self.world.plants:
            sx, sy = self.world_to_screen(plant.position)
            r = max(1, int(plant.size))
            pygame.draw.circle(self.screen, PLANT_COLOR, (sx, sy), r)

    def _draw_creatures(self):
        for c in self.world.creatures.values():
            sx, sy = self.world_to_screen(c.position)
            color = c.genome.color.rgb
            radius = max(2, int(c.genome.basic.size))

            # body
            pygame.draw.circle(self.screen, color, (sx, sy), radius)

            # HP bar
            hp_ratio = c.health / c.genome.basic.max_health
            en_ratio = c.energy / c.genome.basic.energy_capacity

            bar_w = radius * 2
            bar_h = 3
            x0 = sx - radius
            y0 = sy - radius - 6

            # HP
            pygame.draw.rect(self.screen, (60, 0, 0), (x0, y0, bar_w, bar_h))
            pygame.draw.rect(self.screen, HP_BAR_COLOR, (x0, y0, int(bar_w * hp_ratio), bar_h))

            # Energy
            y1 = y0 - 4
            pygame.draw.rect(self.screen, (0, 0, 60), (x0, y1, bar_w, bar_h))
            pygame.draw.rect(self.screen, ENERGY_BAR_COLOR, (x0, y1, int(bar_w * en_ratio), bar_h))

            # ID text (small overlay)
            text = self.font.render(str(c.id), True, (255, 255, 255))
            self.screen.blit(text, (sx - radius, sy + radius + 2))

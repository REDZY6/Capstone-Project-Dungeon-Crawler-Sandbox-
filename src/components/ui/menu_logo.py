from components.sprite import Sprite
import pygame
import math
import time

class FloatingLogo(Sprite):
    def __init__(self, logo_sprite='Logo.png', x=960, y=200, amplitude=50, speed=0.5):
        super().__init__(image=logo_sprite, is_ui=True)
        self.x = x
        self.base_y = y
        self.amplitude = amplitude
        self.speed = speed
        self.start_time = time.time()
        # Initialize the rect attribute
        self.rect = self.image.get_rect(center=(self.x, self.base_y))
        from core.engine import engine
        engine.active_objs.append(self)

    def update(self):
        elapsed = time.time() - self.start_time
        offset = self.amplitude * math.sin(2 * math.pi * self.speed * elapsed)
        self.rect.center = (self.x, self.base_y + offset)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

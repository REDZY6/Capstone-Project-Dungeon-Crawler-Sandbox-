import pygame
from math import ceil

map = None

map_folder_location = "content/maps"
image_folder_location = "content/images"
tile_size = 48

class TileKind:
    def __init__(self, name, image, is_solid):
        self.name = name
        self.image_name = image
        self.image = pygame.image.load(image_folder_location + "/" + image)
        self.is_solid = is_solid

class Map:
    def __init__(self, data, tile_kinds, legacy_data=False):
        from core.engine import engine
        engine.background_drawables.append(self)

        # Keep a list of different kinds of files
        self.tile_kinds = tile_kinds

        # Set up the tiles from loaded data
        if legacy_data:
            self.tiles = []
            for line in data.split("\n"):
                if line.strip():  # Ignore empty lines
                    row = [int(tile_number) for tile_number in line.split()] 
                    self.tiles.append(row)
        else:
            self.tiles = data

        # Set the size 
        self.tile_size = tile_size

    def is_point_solid(self, x, y):
        x_tile = int(x / self.tile_size)
        y_tile = int(y / self.tile_size)
        if x_tile < 0 or \
            y_tile < 0 or \
            y_tile >= len(self.tiles) or \
            x_tile >= len(self.tiles[y_tile]):
            return True
        tile = self.tiles[y_tile][x_tile]
        return self.tile_kinds[tile].is_solid

    def set_tile(self, x, y, index):
        x_tile = int(x / self.tile_size)
        y_tile = int(y / self.tile_size)
        if x_tile < 0 or \
            y_tile < 0 or \
            y_tile >= len(self.tiles) or \
            x_tile >= len(self.tiles[y_tile]):
            return 
        self.tiles[y_tile][x_tile] = index

    def save_to_file(self, file):
        import struct
        for y, row in enumerate(self.tiles):
            for x, n in enumerate(row):
                packed = struct.pack('H', n)
                file.write(packed)

    def is_rect_solid(self, x, y ,width, height):
        x_checks = int(ceil(width/self.tile_size))
        y_checks = int(ceil(height/self.tile_size))
        # Loop addition of 48 for bigger image checks
        for yi in range(y_checks):
            for xi in range(x_checks):
                x = xi * self.tile_size + x
                y = yi * self.tile_size + y
                if self.is_point_solid(x, y):
                    return True
        if self.is_point_solid(x + width, y): # Check Bottom Right Corner
            return True
        if self.is_point_solid(x, y + height): # Check Top Left Corner
            return True
        if self.is_point_solid(x + width, y + height): # Check Top Right Corner
            return True
        return False

    def draw(self, screen):
        from core.camera import camera
        for y, row in enumerate(self.tiles):
            for x, tile in enumerate(row):
                location = (x * self.tile_size - camera.x, 
                            y * self.tile_size - camera.y)
                image = self.tile_kinds[tile].image
                screen.blit(image, location)

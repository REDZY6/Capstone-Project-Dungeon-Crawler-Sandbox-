# Combine map and Entities
from core.map import Map
from core.engine import engine
import traceback
import struct

area = None
map_folder_location = "content/maps"
file_version = 1

class Area:
    def __init__(self, area_file, tile_types, is_editor_mode=False):
        global area
        area = self  # singleton reference
        self.entities = []
        self.is_editor_mode = is_editor_mode
        self.tile_types = tile_types
        print(f"Initializing Area with file: {area_file}")  # Debug

        try:
            self.load_file(area_file)
            print(f"Area loaded. Name: {self.name}")  # Check if name is set
        except Exception as e:
            print(f"Error loading area: {e}")
    
    def search_for_first(self, kind):
        for e in self.entities:
            c = e.get(kind)
            if c is not None:
                return e

    def add_entity(self, e):
        self.entities.append(e)
        
    def remove_entity(self, e):
        self.entities.remove(e)
        for c in e.components: # does this attribute has a breakdown function
            g = getattr(c, "breakdown", None)
            if callable(g): # If yes is it callable
                c.breakdown() # Free up resources

    def load_file(self, area_file):
        import struct
        from data.objects import create_entity
        from core.engine import engine

        engine.reset()
         # Rb = reading binary
        file = open(map_folder_location + "/" + area_file, "rb")
        # read a single byte from the first
        b = struct.unpack('c', file.read(1))[0]
        # convert it into strings
        b = str(b, 'utf-8')
        if b != '\0':
            # If it doesn't have this, its the old file format
            # We load with the previous method
            file.close()
            print("Loading Legacy file")
            self.load_file_legacy(area_file)
            return
        
        # Get a list of entity and the name of the file
        self.entities = []
        self.name = area_file.split(".")[0].title().replace("_", " ")

        # For backwards compatibility,
        # Try to read the version number from the first 4 byte
        version = struct.unpack('i', file.read(4))[0]
        tilemap_width = struct.unpack('i', file.read(4))[0]
        tilemap_height = struct.unpack('i', file.read(4))[0]
        tilemap_width = int(tilemap_width)
        tilemap_height = int(tilemap_height)

        # Load tile data
        tiles = []
        for y in range(tilemap_height):
            row = []
            for x in range(tilemap_width):
                # Reading two bytes per tile
                binary_data = file.read(2)
                # H here equals to we can read two bytes at once which is = 65000 types of tiles
                tile_number = struct.unpack('H', binary_data)[0]
                row.append(tile_number)
            tiles.append(row)
        self.map = Map(tiles, self.tile_types, False)

        # Load each entity, delimited by a null terminated char
        # Read all the rest of the data from the file
        entity_data = file.read()

        # Convert it to a string
        entity_data = str(entity_data, encoding='utf-8')

        # Split the string to get each entity
        entities = entity_data.split('\0')

        # Throw away the last null because there is a null character at the end of the file
        entities = entities[:len(entities)-1]

        # Load each entity
        for line in entities:
            try:
                items = line.split(',')
                id = int(items[0])
                x = int(items[1])
                y = int(items[2])
                if self.is_editor_mode:
                    from components.entity import Entity
                    from components.sprite import Sprite
                    from components.editor import EntityPlaceholder
                    from data.objects import entity_factories
                    # Create entity
                    e = Entity(Sprite(entity_factories[id].icon),
                               EntityPlaceholder(id, items[3:]),
                               x=x*48,
                               y=y*48)
                    if e.has(EntityPlaceholder):
                        self.entities.append(e)
                else:
                    e = create_entity(id, x, y, items[3:])
                    self.entities.append(e)
            except Exception as e:
                print(f"Error parsing line: {line}. {e}")
                traceback.print_exc()


    def load_file_legacy(self, area_file):
        from data.objects import create_entity 
        from core.engine import engine
        engine.reset()
        
        # Read all the data from the file
        file = open(map_folder_location + "/" + area_file, "r")
        data = file.read()
        file.close() # close file after read
        self.name = area_file.split(".")[0].title().replace("_"," ") # Split the map name by . and get the first part of the name and replace _ with space if there is one
        
        # Split up the data by minus sign
        chunks = data.split('-')
        tile_map_data = chunks[0] # First part of maps is tile data
        entity_data = chunks[1] # Second part of maps after minus sign will be the entity data

        # Load the map
        self.map = Map(tile_map_data, self.tile_types, True)

        # Load the entities
        self.entities = []
        entity_lines = entity_data.split('\n')[1:] # basically start reading from the first line after the minus sign
        for line in entity_lines:
            try: # try here is because user might enter wrong format
                items = line.split(',') # Seperate each information by ,
                id = int(items[0])
                x = int(items[1])
                y = int(items[2])
                if self.is_editor_mode:
                    from components.entity import Entity
                    from components.sprite import Sprite
                    from components.editor import EntityPlaceholder
                    from data.objects import entity_factories
                    e = Entity(Sprite(entity_factories[id].icon),
                               EntityPlaceholder(id, items[3:]),
                               x=x*48,
                               y=y*48)
                    if e.has(EntityPlaceholder):
                        self.entities.append(e)
                else:
                    e = create_entity(id, x, y, items[3:])
                    self.entities.append(e) # Call create_entity function to pass in all the information
            except Exception as e: 
                print(f"Error parsing line: {line} (ID: {items[0] if items else '??'}). {e}")

    def save_file(self, filename):
        from data.objects import create_entity
        if not self.is_editor_mode:
            raise Exception("Cannot save file, not in editor mode")
        import struct

        path = map_folder_location + "/" + filename
        # Write file in binary (Write Binary)
        file = open(path,"wb")

        # --- Header of the File ---
        # Write a null byte to indicate we are using the new file format
        # c = chartype 8 bits
        file.write(struct.pack('c', bytes('\0', 'utf-8'))) 
        # Write the file version for future updates
        # i = integer 4 bits
        file.write(struct.pack('i', file_version))

        # Write the size of the tilemap
        # First Width, then height
        width = len(self.map.tiles[0])
        height = len(self.map.tiles)
        file.write(struct.pack('i', width))
        file.write(struct.pack('i', height))

        # --- Body of the File ---
        # Save the Tile data
        self.map.save_to_file(file)
 
        # --- Filter duplicates ---
        seen_coords = set()

        for e in self.entities:
            from components.editor import EntityPlaceholder
            p = e.get(EntityPlaceholder)
            tile_x = int(e.x / 48)
            tile_y = int(e.y / 48)
            coord_key = (tile_x, tile_y)

            # Skip duplicate
            if coord_key in seen_coords:
                print(f"Duplicate entity at {coord_key} skipped")
                continue
            seen_coords.add(coord_key)

            s = f"{p.id},{tile_x},{tile_y}"
            if p.args is not None and len(p.args) != 0:
                s += "," + ",".join(p.args)
            b = bytes(s, 'utf-8')
            packed = struct.pack(f"{len(b)}s", b)
            file.write(packed)
            file.write(struct.pack('c', bytes('\0', 'utf-8')))

        file.close()


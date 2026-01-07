from data.tile_types import tile_kinds
from core.area import Area
from components.entity import Entity
from components.button import Button
from components.sprite import Sprite
from components.label import Label
from components.ui.text_input import TextInput
from components.ui.scroll_view import ScrollView, create_scroll_sprite_generic
import pygame

# ---- Map Editor Fields ----
filename = None                # Current map file that is being worked on
tool = "Click"                 # Keep track of which tool we are using, Click function
current_tile_index = 0         # The current tile to place with the Tile Tool
current_entity_index = 0       # Current Entity to place with the Entity Tool
tool_entities = None           # Any UI entities used in the current tool
field_one = None               # A potential text field for the current tool
selected_entity = None         # The current entity selected by the click tool
fields = []                    # Fields which can be filled out for entities.
# ---- Setters ----
# Changes a tile to the one selected in the scroll view
def set_filename(filename_in):
    global filename
    filename = filename_in

def set_current_tile(item, index):
    global current_tile_index
    current_tile_index = index

def set_entity(item, index):
    global current_entity_index
    current_entity_index = index

def set_tool(new_tool):
    global tool, tool_entities, field_one
    tool = new_tool
    print(f"Tool has been set tp {tool}")
    for e in tool_entities:
        e.delete_self()
        field_one = None
    tool_entities.clear()
    if tool == "Save":
        save_map()
    if tool == "Entity":
        from data.objects import entity_factories
        from core.camera import camera
        image_names = [i.icon for i in entity_factories]
        sv = Entity(ScrollView(
            image_names,
            create_scroll_sprite_generic,
            set_entity,
            64+4,
            width=64,
            height=camera.height
        ),
        x=camera.width-48-3-3)
        tool_entities.append(sv)
    if tool == "Tile":
        from core.area import area
        from core.camera import camera
        # Get the image name of each TileKind
        image_names = [i.image_name for i in area.map.tile_kinds]
        sv = Entity(ScrollView(
            image_names,
            create_scroll_sprite_generic,
            set_current_tile,
            50,
            width=(50),
            height=camera.height
        ),
        x=camera.width-50-3-3)
        tool_entities.append(sv)

        # Implement brush size to increase the size of the brush
        field_label = Entity(Label("Montserrat-Bold.ttf", "Brush Size"),
                             y=camera.height-65).get(Label)
        field_one = Entity(
            TextInput("Montserrat-Bold.ttf", "1", max_text=1),
            x=field_label.get_bounds().width + 10,
            y=camera.height-60
        ).get(TextInput)
        tool_entities.append(field_label.entity)
        tool_entities.append(field_one.entity)
    return

# ---- Map Editor Functionality ----

def save_map():
    from core.area import area
    area.save_file(filename)

def place_tile(mouse_x, mouse_y):
    from core.camera import camera
    x = mouse_x + camera.x
    y = mouse_y + camera.y
    from core.area import area
    try:
        global field_one
        size = int(field_one.text)
        for yy in range(size):
            for xx in range(size):
                area.map.set_tile(x + (xx*48), y + (yy*48), current_tile_index)
    except Exception as e:
        print("Error placing tile", e)

def place_entity(mouse_x, mouse_y):
    from core.camera import camera
    from core.area import area
    from data.objects import entity_factories
    # Get mouse position moving relative to the map
    x = mouse_x + camera.x
    y = mouse_y + camera.y
    # Get the tile that the mouse is pointing at
    entity_x = int(x / area.map.tile_size) * 48
    entity_y = int(y / area.map.tile_size) * 48
    from components.editor import EntityPlaceholder
    e = Entity(Sprite(entity_factories[current_entity_index].icon),
            EntityPlaceholder(current_entity_index,
                              entity_factories[current_entity_index].defaults),
        x=entity_x,
        y=entity_y)
    # Check if this area has an entity
    if e.has(EntityPlaceholder):
        from core.area import area
        area.entities.append(e)

def click_tool(mouse_x, mouse_y):
    from core.area import area
    from core.camera import camera
    mouse_x += camera.x
    mouse_y += camera.y

    for e in area.entities:
        if e.has(Sprite):
            sprite = e.get(Sprite)
            # Figure out whether the mouse is in the sprite
            if mouse_x > e.x and \
                mouse_y > e.y and \
                mouse_x < e.x + sprite.image.get_width() and \
                mouse_y < e.y + sprite.image.get_height():
                from components.editor import EntityPlaceholder
                from data.objects import entity_factories
                global selected_entity, fields
                fields.clear()
                # Set the selected entity to the entity we just clicked on
                selected_entity = e
                placeholder = e.get(EntityPlaceholder)
                # Reference to the id
                id = placeholder.id
                # Call the factory
                factory = entity_factories[id]
                
                # Clear out Previous tools
                for tool in tool_entities:
                   tool.delete_self()
                tool_entities.clear()

                # Title of Entity
                field_label = Entity(Label("Montserrat-Bold.ttf",
                                           factory.name + ": "),
                            y = camera.height-50).get(Label)
                tool_entities.append(field_label.entity)
                
                # Display all args of entity
                x = field_label.get_bounds().width
                for i, arg in enumerate(factory.arg_names):
                    label = Entity(Label("Montserrat-Bold.ttf",
                                   arg),
                            x=x,
                            y=camera.height-100).get(Label)
                    field = Entity(TextInput("Montserrat-Bold.ttf",
                                   e.get(EntityPlaceholder).args[i],
                                   max_text=15,
                                   width=450,
                                   on_change=lambda: save_args()),
                            x=x,
                            y=camera.height-50
                    ).get(TextInput) 
                    fields.append(field)
                    # 200 width for each box then 20 pixel gap
                    x += 500
                    tool_entities.append(label.entity)
                    tool_entities.append(field.entity)
                return

def save_args():
    from components.editor import EntityPlaceholder
    for i, field in enumerate(fields):
        value = field.text
        selected_entity.get(EntityPlaceholder).args[i] = value

def delete_tool(mouse_x, mouse_y):
    from core.camera import camera
    from core.area import area
    x = mouse_x + camera.x
    y = mouse_y + camera.y
    # Loop through all the entity in area
    for e in area.entities:
        if e.has(Sprite):
            sprite = e.get(Sprite)
            # Figure out whether the mouse is in the sprite
            if x > e.x and \
                y > e.y and \
                x < e.x + sprite.image.get_width() and \
                y < e.y + sprite.image.get_height():
                e.delete_self()
                return

# ---- User Interface ----
def back_button_press():
    global filename
    filename = None
    from core.engine import engine
    engine.switch_to("EditorChooseFile")

def on_click():
    global tool
    mouse_pos = pygame.mouse.get_pos()

    from core.camera import camera
    if mouse_pos[0] > camera.width-(48+3+3) or \
        (mouse_pos[0] < 64 and mouse_pos[1] < 64*4) or \
        (mouse_pos[1] > camera.height - 50):
        return

    if tool == "Click":
        click_tool(mouse_pos[0], mouse_pos[1])
    elif tool == "Tile":
        place_tile(mouse_pos[0], mouse_pos[1])
    elif tool == "Entity":
        place_entity(mouse_pos[0], mouse_pos[1])
    elif tool == "Delete":
        delete_tool(mouse_pos[0], mouse_pos[1])

def edit_map():
    global tool_entities
    tool_entities = []
    Area(filename, tile_kinds, is_editor_mode=True)

    from components.editor_helper import EditorHelper
    Entity(EditorHelper(on_click))
    
    Entity(Button(lambda: set_tool("Click"),
                  pygame.Rect(0, 0, 60, 60)),
           Sprite('button_background.png', True),
           Sprite('mouse_tool.png', True),
           x=2,
           y=2+64*0)
    Entity(Button(lambda: set_tool("Tile"),
                  pygame.Rect(0, 0, 60, 60)),
           Sprite('button_background.png', True),
           Sprite('tile_tool.png', True),
           x=2,
           y=2+64*1)
    Entity(Button(lambda: set_tool("Save"),
                  pygame.Rect(0, 0, 60, 60)),
           Sprite('button_background.png', True),
           Sprite('save.png', True),
           x=2,
           y=2+64*2)
    Entity(Button(lambda: set_tool("Entity"),
                  pygame.Rect(0, 0, 60, 60)),
           Sprite('button_background.png', True),
           Sprite('entity.png', True),
           x=2,
           y=2+64*3)
    Entity(Button(lambda: set_tool("Delete"),
                   pygame.Rect(0, 0, 60, 60)),
            Sprite('button_background.png', True),
            Sprite('trash.png', True),
            x=2,
            y=2+64*4)
    Entity(Button(lambda: back_button_press(),
                  pygame.Rect(0, 0, 60, 60)),
           Sprite('button_background.png', True),
           Sprite('cancel.png', True),
           x=2,
           y=2+64*5)

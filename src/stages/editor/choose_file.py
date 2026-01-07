from components.button import Button, create_simple_label_button
from components.ui.scroll_view import ScrollView, create_scroll_label_generic, print_on_choose
from components.ui.text_input import TextInput
from components.entity import Entity
from components.label import Label
from components.sprite import Sprite
from stages.editor.edit_map import set_filename
import shutil

new_map_input = None
page_width = 500

def create_map():
    if len(new_map_input.text) < 4 or new_map_input.text[-4:] != ".map":
        new_map_input.max_text += 5
        new_map_input.set_text(new_map_input.text + ".map")
    print(f"Creating map {new_map_input.text}")

    filename = new_map_input.text

    # Check if the map already exists.
    import os
    if os.path.exists("content/maps/" + filename):
        print(f"Error, map already exists: {filename}")
        return

    shutil.copyfile("content/maps/template.map", "content/maps/" + filename)
    set_filename(filename)

    from core.engine import engine
    engine.switch_to("EditorEditMap")

def load_map(map, index):
    print(f"Loading map {map}")
    set_filename(map)
    from core.engine import engine
    engine.switch_to("EditorEditMap")

def get_maps():
    import os
    files = os.listdir("content/maps")
    if 'template.map' in files:
        files.remove('template.map')
    files.sort()
    return files

def back():
    from core.engine import engine
    engine.switch_to("Menu")

def editor_choose_file():
    Entity(Sprite("background1.png", is_ui=True))
    global new_map_input

    page_x =  1920/2 - page_width/2 - 150

    create_simple_label_button(
        back,
        "Montserrat-ExtraBold.ttf",
        "Back",
        x=10,
        y=10
    )

    create_simple_label_button(
        create_map,
        "Montserrat-ExtraBold.ttf",
        "Create",
        x=page_x+830,
        y=100
    )

    Entity(Label("Montserrat-ExtraBold.ttf", "Create New Map"),
            x=page_x + 185, y=20)

    new_map_input = Entity(TextInput("Montserrat-ExtraBold.ttf",
                                     "Test",
                                    width=800),
                            x=page_x,
                            y=100).get(TextInput)

    Entity(Label("Montserrat-ExtraBold.ttf", "Load Map"),
            x=page_x + 270, y=1010)

    Entity(ScrollView(get_maps(),
                      create_scroll_label_generic,
                      load_map,
                      48,
                      width=800,
                      height=800), x=page_x, y=200)
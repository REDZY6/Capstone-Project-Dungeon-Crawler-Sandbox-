from components.entity import Entity
from components.sprite import Sprite, Animation
from components.player import Player
from components.physics import Body
from components.teleporter import Teleporter
from components.inventory import Inventory, DroppedItem
from data.item_types import item_types
from components.usable import Usable, Minable, Interactable
from components.enemy import Enemy
from components.npc import NPC

class EntityFactory:
    def __init__(self, name, icon, factory, arg_names=[], defaults=[]):
        self.name = name
        self.icon = icon
        self.factory = factory
        self.arg_names = arg_names
        self.defaults = defaults

# Create a section to store all the entity, and when i need them for each particular map i can call it.
entity_factories = [
    # 0 - Player (100 Player Health)
    # lamda arguments is used because the argument does not require a name.
    EntityFactory("Player",
                  "player.png",
                  lambda args: Entity(Player(100), 
                  Animation("player_sprite_sheet.png", 72, 74, frame_coords=[(0, 0)], frames_per_image=10), 
                  Body(12, 40, 40, 20)),
                 ),
    # 1 - Rock 1
    EntityFactory("Rock 1",
                  "23_Rock 1.png",
                  lambda args: Entity(Sprite("23_Rock 1.png"), 
                  Body(10, 10, 35, 50), 
                  Minable("rock")),
                 ),

    # 2 - Teleporter
    EntityFactory("Teleporter",
                  "Halo Anim 1.png",
                  lambda args: Entity(Teleporter(args[0], args[1], args[2]), Sprite("Halo Anim 1.png")),
                  ['Area File', 'Player X', 'Player Y'],
                  # By Default
                  ['start.map', '2', '8']
                 ),

    # 3 - Sword (Dropped Item)
    # How to code in map 1. What kind of entity 2. X position 3. Y position 4. What kind of item 5. Quantity of Item
    EntityFactory("Dropped Item",
                  "Item1_Sword.png",
                  lambda args: Entity(DroppedItem(item_types[int(args[0])], int(args[1])), 
                  Sprite(item_types[int(args[0])].icon_name)),
                  ['Item Type ID', 'Quantity'],
                  # By Default
                  ['0', '1']
                 ),

    # 4 - Statue
    EntityFactory("Statue",
                  "Statue.png",
                  lambda args: Entity(Sprite("Statue.png"), 
                  Body(30, 100, 110, 150), 
                  Interactable("statue", "Interacted_Statue.png"))),

    # 5 - NPC
    EntityFactory("NPC",
                  "pink_npc.png",
                  lambda args: Entity(Sprite(args[1]), Body(7, 20, 18, 60), NPC(args[0], args[2])),
                  ["NPC's Name", "Image", "NPC File"],
                  ["Zarvokh", "pink_npc.png", "demon.npc"]
                 ),

    # 6 - Enemy(Health, Item ID)
    EntityFactory("Rogue",
                  "Demon_npc.png",
                  lambda args: Entity(Sprite(args[0]), Enemy(100, 3), Body(7, 20, 18, 60)),
                  ["Image"],
                  ["Demon_npc.png"]
                 ),
]

def create_entity(id, x, y, data=None, index=None): # id = the number corresponding to the entity (example: 0 = player, 1 = rock etc), x,y is the corresponding coordinate in the map
    print(f"Creating entity {id} at ({x}, {y}) with data: {data}")  # Debugging output
    factory = entity_factories[id].factory
    e = factory(data)
    e.index = index
    print(f"Entity created: {e}")  # Check the entity after creation
    e.x = x * 48
    e.y = y * 48
    return e

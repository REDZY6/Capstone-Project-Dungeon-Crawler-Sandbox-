from components.inventory import ItemType

item_types = [
    # Item type, png, how many it is stackable in the inventory
    
    # 1. What kind of entity 2. X position 3. Y position 4. What kind of item 5. Quantity of Item
    
    #0
    ItemType("Sword", "Item1_Sword.png", 1, damage=10, cooldown=0.5, range=50, sound='sword_sound.mp3'),
    #1
    ItemType("Pickaxe", "Item2_Pickaxe.png", 1, mine_power=10),
    #2
    ItemType("Orb", "Item3_Orb.png", 1, orb_power=10),
    #3
    ItemType("Weak Sword", "Item1_Sword.png", 1, damage=2, cooldown=1.0, range=50, sound='sword_sound.mp3'),
]
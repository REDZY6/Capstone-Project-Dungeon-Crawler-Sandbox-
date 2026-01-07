import pygame
from components.physics import Trigger
from core.sound import Sound

image_path = "content/images"
pick_up_sound = Sound('pick_up.mp3')

# Information about each type (icon, value, stack size, etc)
class ItemType:
    def __init__(self, name, icon, stack_size=1, **kwargs): # kwargs to capture keywords like mine_power
        self.name = name
        self.icon_name = icon
        self.icon = pygame.image.load(image_path + "/" + icon)
        self.value = 0
        self.weight = 0
        self.stack_size = stack_size
        self.stats = dict() # add stats to items
        for key in kwargs:
            self.stats[key] = kwargs[key]

# Can hold a quantity of can item
class ItemSlot:
    def __init__(self):
        self.type = None
        self.amount = 0

# Has a certain number of slots for items.
class Inventory:
    # Creates a new inventory
    def __init__(self, capacity):
        self.capacity = capacity
        self.taken_slots = 0
        self.equipped_slot = None
        self.slots = []
        for _ in range(self.capacity):
            self.slots.append(ItemSlot())
        self.listener = None

    # Lets a listener know the inventory changed
    def notify(self):
        if self.listener is not None:
            self.listener.refresh()
    
    # Use the best weapon in your inventory
    def get_best(self, stat):
        best = {"power": 0, "item": None}
        for s in self.slots:
            if s.type is not None and stat in s.type.stats:
                p = int(s.type.stats[stat])
                if p > best["power"]:
                    best["power"] = p 
                    best["item"] = s.type
        return best

    # Attempts to add a certain amount of an item to the inventory, Default is 1 of that item. 
    # Returns any excess items it couldn't add.
    def add(self, item_type, amount=1):
        # Furst sweep for any open stacks
        if item_type.stack_size > 1:
            for slot in self.slots:
                if slot.type == item_type:
                    add_amo = amount
                    # Basically check if the slot is full or not for stackable items
                    if add_amo > item_type.stack_size - slot.amount: 
                        add_amo = item_type.stack_size - slot.amount
                    slot.amount += add_amo
                    amount -= add_amo
                    if amount <= 0:
                        self.notify()
                        return 0
        # Next, place the item in the next slot
        for slot in self.slots:
            if slot.type == None: # If slot is empty
                slot.type = item_type # Set slot type to item type
                # Stack as much as we can in that slot
                if item_type.stack_size < amount:
                    slot.amount = item_type.stack_size
                    self.notify()
                    return self.add(item_type, amount - item_type.stack_size)
                else:
                    slot.amount = amount 
                    self.notify()
                    return 0
    
    # Attempts to remove a certain amount of an item from the inventory. Default is 1 of that item.
    # Returns what is was able to remove
    def remove(self, item_type, amount=1):
        found = 0
        for slot in self.slots:
            if slot.type == item_type:
                if slot.amount < amount: # Check is this slot reach the required amount. If less than required amount remove all from the slot
                    found += slot.amount
                    slot.amount = 0
                    slot.type = None
                    self.notify()
                    continue
                elif slot.amount == amount: # If equal amount remove all from inventory and equals to 0
                    found += slot.amount
                    slot.amount = 0
                    self.notify()
                    return found
                else: # If amount is more than required we will just subtract the required amount of the item
                    found += amount
                    slot.amount -= amount
                    self.notify()
                    return found
        return found

    # Returns whether a ceratin amount of an item is present in the inventory. Useful for shops.
    def has(self, item_type, amount=1):
        found = 0 # Starting from 0
        for slot in self.slots: # Check how many of that item is in your inventory
            if slot.type == item_type:
                found += slot.amount
                if found >= amount:
                    return True
        return False

    # Returns the first slot number of where an item is.
    def get_index(self, item_type):
        for index, slot in enumerate(self.slots):
            if slot.type == item_type:
                return index
        return -1 # if we dont find anything we will return -1

    # Returns a string (text) of the inventory. Very useful for degbugging.
    def __str__(self):
        s = ""
        for i in self.slots:
            if i.type is not None:
                s += str(i.type.name) + ": " + star(i.amount) + "\t"
            else:
                s += "Empty slot\t"
        return s

    # Returns how many slots are currently open.
    def get_free_slots(self):
        return self.capacity - self.taken_slots

    # Returns true if all slots have an item. False otherwise.
    def is_full(self):
        return self.taken_slots == self.capacity

    # Returns the total weight of all items in the inventory.
    def get_weight(self):
        weight = 0
        for i in self.slots:
            weight += i.weight * i.amount
        return weight

    # Returns the total value of all items in the inventory.
    def get_value(self):
        value = 0
        for i in self.slots:
            value += i.value * i.amount
        return value

def pick_up(item, other):
    from components.player import Player, inventory
    if other.has(Player):
        pick_up_sound.play()
        # inventory = other.get(Inventory)
        extra = inventory.add(item.item_type, item.quantity)
        item.quantity -= item.quantity - extra
        if item.quantity <= 0:
            from core.area import area
            area.remove_entity(item.entity)
        # print(inventory)

# An item on the ground you can pick up 
class DroppedItem(Trigger): # Call Trigger Class
    def __init__(self, item_type, quantity):
        self.item_type = item_type
        self.quantity =  quantity
        super().__init__(lambda other: pick_up(self, other), 0, 0, 32, 32)
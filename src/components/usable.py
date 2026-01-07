from core.sound import Sound

class Usable:
    def __init__(self, obj_name):
        self.obj_name = obj_name
        from core.engine import engine
        engine.usables.append(self)

    def breakdown(self):
        from core.engine import engine
        engine.usables.remove(self)

    # Call this function when player interact with it
    def on(self, other, distance):
        print("Base on function called")

# Something you can interact or mine with
class Minable(Usable):
    def __init__(self, obj_name):
        super().__init__(obj_name)
        self.sound = Sound('mine_rock.mp3')
    
    def on(self, other, distance):
        from components.player import Player, inventory
        player = other.get(Player)
        mine_best = inventory.get_best("mine_power")

        # Check if the player has something they can use to mine
        if mine_best["power"] <= 0:
            player.show_message("You need a pickaxe to mine this " + self.obj_name)
            return

        # Player x,y, Effect position, last for 10 frames, icon of the best item
        from core.effect import Effect
        Effect(other.x, other.y, 0, 1, 10, mine_best["item"].icon)

        # Check if player is in range with the usable obj
        if distance < 60:
            self.sound.play()
            player.show_message("Mining " + self.obj_name)
            from core.area import area
            area.remove_entity(self.entity)
        else:
            player.show_message("I need to get closer")

class Interactable(Usable):
    def __init__(self, obj_name, interacted_image):
        super().__init__(obj_name)
        self.interacted_image = interacted_image
        self.is_interacted = False
        self.sound = Sound('activate_statue_sound.mp3')

    def on(self, other, distance):
        from components.player import Player, inventory
        from components.sprite import Sprite
        player = other.get(Player)

        # If already interacted
        if self.is_interacted:
            player.show_message("This statue has already activated.")
            return

        orb_best = inventory.get_best("orb_power")

        # Check if the player has something they can use to activate the statue
        if orb_best["power"] <= 0:
            player.show_message("You need an orb to activate this " + self.obj_name)
            return

        # Player x,y, Effect position, last for 10 frames, icon of the best item
        from core.effect import Effect
        Effect(other.x, other.y, 0, 1, 10, orb_best["item"].icon)

        # If in range
        if distance < 150:
            self.sound.play()
            player.show_message("Activating " + self.obj_name)
            self.entity.get(Sprite).set_image(self.interacted_image)
            self.is_interacted = True
        else:
            player.show_message("I need to get closer")
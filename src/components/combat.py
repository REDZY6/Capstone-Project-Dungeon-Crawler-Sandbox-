from core.sound import Sound
import pdb

class Combat:
    def __init__(self, health, on_death):
        self.health = health
        self.max_health = health
        self.global_cooldown = 0
        self.equipped = None
        self.regen = 0.01
        self.sound = None
        self.on_death = on_death
        self.weapon_sprite = None
        from core.engine import engine
        engine.active_objs.append(self)

    def equip(self, item):
        from components.entity import Entity
        from components.sprite import Sprite
        self.equipped = item
        print("equipping", self.equipped)
        if self.equipped is None:
            return
        if 'sound' in self.equipped.stats:
            self.sound = Sound(self.equipped.stats['sound'])
        self.weapon_sprite = Entity(Sprite(self.equipped.icon_name)).get(Sprite)
        from core.engine import engine 
        engine.active_objs.append(self)
        
    def unequip(self):
        print("calling unequip")
        self.equipped = None
        if self.weapon_sprite and self.weapon_sprite.entity:
            self.weapon_sprite.entity.delete_self()  # Delete the weapon from the player's hand
        self.weapon_sprite = None
        self.sound = None
        print("Weapon sprite", self.weapon_sprite)


    def breakdown(self):
        from core.engine import engine
        engine.active_objs.remove(self)
        
        # Ensure the weapon sprite is only deleted if it exists and is not None
        if self.weapon_sprite and self.weapon_sprite.entity:
            self.weapon_sprite.entity.delete_self()  # Delete the weapon sprite on enemy death
        self.weapon_sprite = None  # Reset the weapon sprite to avoid any reference conflicts

    def attack(self, other):
        if self.equipped == None:
            # If we dont have any weapon, dont attack.
            return

        # If we are still on cooldown
        if self.global_cooldown > 0:
            return

        damage = int(self.equipped.stats['damage'])
        other.health -= damage
        self.global_cooldown = self.equipped.stats['cooldown']*60
        if self.sound is not None:
            self.sound.play()

        from core.effect import create_hit_text, Effect
        create_hit_text(other.entity.x, other.entity.y, str(damage), (255, 0, 0))
 
        if other.health <= 0:
            other.on_death(other.entity)

    def perform_attack(self):
    # Swing sword
        if self.equipped is None:
            return

        if not 'range' in self.equipped.stats:
            # Weapon has no range 
            return

        from components.physics import get_bodies_within_circle
        # Get all nearby entities
        nearby_objs = get_bodies_within_circle(self.entity.x,
                                               self.entity.y,
                                               self.equipped.stats['range'])

        for o in nearby_objs:
            if o.entity.has(Combat) and o.entity != self.entity:
                self.attack(o.entity.get(Combat))


    def update(self):
        # update attack cooldown
        if self.global_cooldown > 0:
            self.global_cooldown -= 1
        # update regeneration
        if self.health < self.max_health:
            self.health += self.regen
        # if regen > max health set it back to max_health
        if self.health > self.max_health:
            self.health = self.max_health

        # Position the weapon sprite in person hand
        if self.weapon_sprite is not None:
            self.weapon_sprite.entity.x = self.entity.x + 30
            self.weapon_sprite.entity.y =self.entity.y + 10


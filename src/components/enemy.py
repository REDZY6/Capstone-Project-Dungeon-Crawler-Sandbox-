import random
from components.physics import Body
from data.item_types import item_types
from core.math_ext import distance
from components.entity import Entity
from components.ui.bar import Bar

def on_enemy_death(entity):
    from core.area import area
    area.remove_entity(entity)
    print("Called Death")

class Enemy:
    def __init__(self, health, weapon_item_id) -> None:
        self.prev_positions = []
        # Base Combat Attributes
        self.health = health
        self.weapon = item_types[weapon_item_id]

        # Ai Attributes
        self.target = None
        self.targeted_entity = None
        # AI update rate
        self.step_to_update = 0
        # How far can the enemy sees
        self.vision_range = 500
        # How fast the enemy can walk
        self.walk_speed = 0.5
        # Initial State
        self.state = "guard"
        # Make Updatable
        from core.engine import engine
        engine.active_objs.append(self)

    def setup(self):
        from components.combat import Combat
        self.entity.add(Combat(self.health, on_enemy_death))
        print(f"Entity components after adding combat: {self.entity.components}")
        self.combat = self.entity.get(Combat)

        self.combat.equip(self.weapon)
        del self.health


    def flee(self):
        if self.prev_positions:
            flee_x, flee_y = self.prev_positions[0]
            self.entity.x, self.entity.y = flee_x, flee_y
           
    def breakdown(self):
        from core.engine import engine
        engine.active_objs.remove(self)
   
    def update_ai(self):
        from components.physics import get_bodies_within_circle
        from components.player import Player
        seen_objects = get_bodies_within_circle(self.entity.x,
                                                self.entity.y,
                                                self.vision_range)
        found_player = False
        for s in seen_objects:
            if s.entity.has(Player):
                self.target = (s.entity.x, s.entity.y)
                self.targeted_entity = s.entity
                found_player = True
           
        if not found_player:
            self.target = None
            self.targeted_entity = None


    def update(self):
        from core.engine import engine

        # Every enemy have 0-30, if let say this enemy is 23 frame it will only update at frame 23
        if engine.step % 30 == self.step_to_update:
            self.update_ai()
       
        # Log the current health and state
        #print(f"Health: {self.combat.health}, State: {self.state}")


        if self.targeted_entity is not None:
            weapon_range = int(self.combat.equipped.stats['range'])
            dist = distance(self.entity.x, self.entity.y,
                            self.targeted_entity.x,
                            self.targeted_entity.y)
            if weapon_range > dist:
                from components.combat import Combat
                self.combat.attack(self.targeted_entity.get(Combat))


        if self.target is not None:
            body = self.entity.get(Body)
            # Initial location of enemy
            prev_x = self.entity.x
            prev_y = self.entity.y


             # Check if current position is different from last position
            current_position = (self.entity.x, self.entity.y)
            if not self.prev_positions or self.prev_positions[-1] != current_position:
                # Only append if the current position is different from the last one
                self.prev_positions.append(current_position)  
               
            if self.combat.health < 50:
                self.state = "flee"
                self.flee()
            elif self.combat.health > 70:
                self.state = "guard"

            if self.state == "flee":
                self.flee()
               
            else:
                if self.entity.x < self.target[0]:
                    self.entity.x += self.walk_speed
                if self.entity.x > self.target[0]:
                    self.entity.x -= self.walk_speed
                if not body.is_position_valid():
                    self.entity.x = prev_x


                if self.entity.y < self.target[1]:
                    self.entity.y += self.walk_speed
                if self.entity.y > self.target[1]:
                    self.entity.y -= self.walk_speed
                if not body.is_position_valid():
                    self.entity.y = prev_y


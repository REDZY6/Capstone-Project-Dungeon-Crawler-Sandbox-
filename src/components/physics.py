from pygame import Rect

bodies = []
triggers = []

# To see if the hitbox is inside the circle
def get_bodies_within_circle(circle_x, circle_y, radius):
    items = []
    for body in bodies:
        if body.is_circle_colliding_with(circle_x, circle_y, radius):
            items.append(body)
    return items

def reset_physics():
    global bodies, triggers
    bodies.clear()
    triggers.clear()

class PhysicalObj:
    def __init__(self, x, y, width, height):
        self.hitbox = Rect(x, y, width, height)

    def is_colliding_with(self, other):
        x = self.entity.x + self.hitbox.x
        y = self.entity.y + self.hitbox.y
        other_x = other.entity.x + other.hitbox.x
        other_y = other.entity.y + other.hitbox.y

        # Check if two rectangle is colliding
        if x < other_x + other.hitbox.width and \
            x + self.hitbox.width > other_x and \
            y < other_y + other.hitbox.height and \
            y + self.hitbox.height > other_y:
            return True
        else:
            return False

    def is_circle_colliding_with(self, circle_x, circle_y, radius):
        # Rectangle collide with circle collision detection
        body_x = self.entity.x + self.hitbox.x
        body_y = self.entity.y + self.hitbox.y
        circle_dist_x = abs(circle_x - body_x)
        circle_dist_y = abs(circle_y - body_y)
        # First we draw a rectangle around the circle
         # Check if circle is way to the right
        if circle_dist_x > (self.hitbox.width/2 + radius):
            return False
         # Check if circle is way below
        if circle_dist_y > (self.hitbox.height/2 + radius):
            return False
        # Check if the circle is way to the left
        if circle_dist_x <= (self.hitbox.width/2):
            return True
        # Check if the circle is way to the top
        if circle_dist_y <= (self.hitbox.height/2):
            return True
        # Second if the rectangle collide with the circle we drew, now we do further checking ti see how close this the hitbox close the the corner
        corner_dist_squared = (circle_dist_x - self.hitbox.width/2)**2 + \
                              (circle_dist_y - self.hitbox.height/2)**2

        return corner_dist_squared <= radius**2

class Trigger(PhysicalObj):
    def __init__(self, on, x=0, y=0, width=48, height=48):
        super().__init__(x, y, width, height)
        triggers.append(self)
        self.on = on

    def breakdown(self):
        global triggers
        triggers.remove(self)

class Body(PhysicalObj):
    def __init__(self, x=0, y=0, width=48, height=48):
        super().__init__(x, y, width, height)
        bodies.append(self)

    def breakdown(self):
        global bodies
        bodies.remove(self)

    def is_position_valid(self):
        from core.area import area
        x = self.entity.x + self.hitbox.x
        y = self.entity.y + self.hitbox.y
        if area.map.is_rect_solid(x, y, self.hitbox.width, self.hitbox.height):
            return False

        for body in bodies:
            if body != self and body.is_colliding_with(self):
                return False
        return True

    



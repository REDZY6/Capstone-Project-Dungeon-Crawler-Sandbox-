class Entity:
    def __init__(self, *components, x=0, y=0): # Variable Arguments
        self.components = []
        self.x = x 
        self.y = y
        for c in components:
            self.add(c, False)
        for c in components:
            g = getattr(c, "setup", None)
            if callable(g):
                c.setup()

    # Function that can add entity into component
    def add(self, component, perform_setup=True):
        component.entity = self # Allow component know about the entity
        self.components.append(component)
        if perform_setup:
            g = getattr(component, "setup", None)
            if callable(g):
                component.setup()

    # Can delete itself when we wanna remove it.
    def delete_self(self):
        from core.area import area
        if self in area.entities:
            area.entities.remove(self)
        for c in self.components:
            g = getattr(c, "breakdown", None)
            if callable(g):
                c.breakdown()
        self.components.clear()

    # Remove based on a type
    def remove(self, kind):
        c = self.get(kind)
        self.remove_component(c)

    # Remove an entity passed into it, prepare engine for editor view
    def remove_component(self, c):
        if c is not None:
            g = getattr(c, "breakdown", None)
            if callable(g):
                c.breakdown()
            c.entity = None
            self.components.remove(c)

    def has(self, kind):
        for c in self.components:
            if isinstance(c, kind):
                return True
        return False

    # Function to get the entity
    def get(self, kind):
        for c in self.components:
            # Search for the entity
            if isinstance(c, kind):
                return c
        return None
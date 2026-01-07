import pygame
pygame.init()

engine = None 
default_width = 1920
default_height = 1080

class Engine:
    def __init__(self, game_title):
        # How many frames has passed for ai optimization
        self.step = 0
        from core.camera import create_screen
        global engine
        engine = self

        self.active_objs = [] # Anything with an update() method which can be called

        self.background_drawables = []
        self.drawables = [] # Anything to be drawn in the world
        self.ui_drawables = [] # Anything to be drawn over the world

        # Anything that the player can interact with will be store here
        self.usables = []

        self.clear_color = (55, 0, 0)
        self.screen = create_screen(default_width, default_height, game_title)
        self.stages = {}
        self.current_stage = None

    def register(self, stage_name, func): # Register stage at the begining
        self.stages[stage_name] = func

    def switch_to(self, stage_name): # Call to switch to a stage
        self.reset() # Clear data of previous stage
        self.current_stage = stage_name
        func = self.stages[stage_name]
        print(f"Switching to {self.current_stage}")
        func()

    def run(self): # Game Loop
        from core.input import keys_down, mouse_buttons_down, mouse_buttons_just_pressed, keys_just_pressed, reset_scroll
        self.running = True
        while self.running:
            reset_scroll()
            self.step += 1
            mouse_buttons_just_pressed.clear()
            keys_just_pressed.clear()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    keys_down.add(event.key)
                    keys_just_pressed.add(event.key)
                elif event.type == pygame.KEYUP:
                    keys_down.remove(event.key)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_buttons_down.add(event.button)
                    mouse_buttons_just_pressed.add(event.button)
                elif event.type == pygame.MOUSEBUTTONUP:
                    mouse_buttons_down.remove(event.button)
                elif event.type == pygame.TEXTINPUT:
                    from core.input import text_input_listeners
                    for t in text_input_listeners: 
                        t.text_input(event.text)
                elif event.type == pygame.MOUSEWHEEL:
                    from core.input import add_scroll_delta
                    # There is event.x to scroll horizontally but we are using y now
                    add_scroll_delta(event.y)

            # Update Code
            for a in self.active_objs:
                a.update()

            # Draw Code
            self.screen.fill(self.clear_color)

            # Draw background items (tiles)
            for b in self.background_drawables:
                b.draw(self.screen)
            # Draw the main objects
            for s in self.drawables:
                s.draw(self.screen)

            # Draw Effects
            from core.effect import effects
            for e in effects:
                e.draw(self.screen)

            # Draw UI
            for l in self.ui_drawables:
                l.draw(self.screen)

            pygame.display.flip()

        pygame.quit()

    def reset(self): # Clear all active_objs, and all drawables
        from core.area import area
        if area is not None:
            e = area.entities.copy()
            for a in e:
                a.delete_self()
        from components.physics import reset_physics
        reset_physics()
        self.active_objs.clear()
        self.drawables.clear()
        self.ui_drawables.clear()
        self.background_drawables.clear()
        self.usables.clear()
        from core.effect import effects
        effects.clear()
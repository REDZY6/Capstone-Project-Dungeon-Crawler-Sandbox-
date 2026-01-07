import pygame
from components.ui.window import create_window
from math import ceil
from components.entity import Entity
from components.sprite import Sprite
from components.ui.window import Window
from components.label import Label
from core.input import is_key_just_pressed

# Left and right size of the dialogue box in pixels
dialogue_box_width = 1000
# Up and down size of the dialogue box in pixels
dialogue_box_height = 200
# Empty pixels separating the dialogue box and the bottom of the window
padding_bottom = 50

# Where the name of the speaker is, in the dialogue box
speaker_label_x = 50
speaker_label_y = 25

# Where the text of the speaker is, in the dialogue box
content_label_x = 50
content_label_y = 75

# Where the helper text is, in the dialogue box
helper_label_x = 50
helper_label_y = 150

class DialogueView:
    def __init__(self, lines, npc, player, dialogue_box_sprite="text_box.png"):
        self.lines = lines
        self.npc = npc
        self.player = player

        from core.camera import camera
        window_x = camera.width/2 - dialogue_box_width/2
        window_y = camera.height - padding_bottom - dialogue_box_height
        self.window =  create_window(window_x, window_y,
                                     dialogue_box_width,
                                     dialogue_box_height).get(Window)

        self.background = Entity(Sprite(dialogue_box_sprite, is_ui= True),
                                 x=window_x,
                                 y=window_y).get(Sprite)

        self.speaker_label = Entity(Label("Montserrat-ExtraBold.ttf", "", size=25), 
                                  x=window_x + speaker_label_x, 
                                  y=window_y + speaker_label_y).get(Label)

        self.content_label = Entity(Label("Montserrat-Bold.ttf", "", size=25), 
                                  x=window_x + content_label_x, 
                                  y=window_y + content_label_y).get(Label)

        self.helper_label = Entity(Label("Montserrat-BoldItalic.ttf", 
                                         "[Press Enter or Space]", 
                                         size=25), 
                                  x=window_x + helper_label_x, 
                                  y=window_y + helper_label_y).get(Label)

        self.window.items.append(self.background)
        self.window.items.append(self.speaker_label)
        self.window.items.append(self.content_label)
        self.window.items.append(self.helper_label)

        from core.engine import engine
        engine.active_objs.append(self)

        self.current_line = -1
        self.next_line()

    # Get the next line of the dialogue
    def next_line(self):
        self.current_line += 1
        # When hit final line we call breakdown to close the dialogue
        if self.current_line >= len(self.lines):
            self.breakdown()
            return
        line = self.lines[self.current_line]
        print(len(line))
        if len(line) == 0:
            self.next_line()
            return
        # - is player speaking
        if line[0] == '-':
            self.player_speak(line)
        # ! is command line where an action will be triggered
        elif line[0] == '!':
            self.command(line)
        elif line[0] == '$':
            self.narrate(line)
        # npc is speaking
        else:
            self.npc_speak(line)

    # Have the NPC speak the nextt line of dialogue
    def npc_speak(self, line):
        self.speaker_label.set_text(self.npc.obj_name)
        self.content_label.set_text(line)

    # Have the player speak the next line of dialogue
    def player_speak(self, line):
        self.speaker_label.set_text("You")
        # Start from 1 which is the second character to ignore the - sign until the end of the line with the ':'
        self.content_label.set_text(line[1:])

    # Place some text in the window without anyone speaking
    def narrate(self, line):
        self.speaker_label.set_text("")
        self.content_label.set_text(line[1:])

    # Execute some special command, like giving the player an item
    # Or jumping to another line
    def command(self, line):
        # Split the line with spaces
        words = line.split(" ")
        # Take the command of the first word
        command = words[1]
        # Take in the argument of the second word and after
        arguments = words[2:]
        if command == "give":
            from components.player import inventory
            from data.item_types import item_types
            # Look for the first integer of the argument
            t = item_types[int(arguments[0])]
            amount = int(arguments[1])
            excess = inventory.add(t, amount)
            amount_added = amount - excess
            if amount_added == 0:
                self.speaker_label.set_text("")
                self.content_label.set_text(f"Your inventory is full!")
            else:
                self.speaker_label.set_text("")
                self.content_label.set_text(f"You receive {amount_added} {t.name}")

        elif command == "goto":
            # minus 2 is just to fix the line because line start from 0
            self.current_line = int(arguments[0])-2
            print(self.current_line)
            self.next_line()
        elif command == "end":
            self.breakdown()
        elif command == "random":
            import random
            next_lines = [int(x) for x in arguments]
            result = random.choice(next_lines)
            self.current_line = result-2
            self.next_line()
        else:
            print(f"Unkown command {command}")

    # Check if a key is pressed to move to the next line
    def update(self):
        # Return key is enter key
        if is_key_just_pressed(pygame.K_SPACE) or is_key_just_pressed(pygame.K_RETURN):
            self.next_line()

        if is_key_just_pressed(pygame.K_w) or is_key_just_pressed(pygame.K_a) \
            or is_key_just_pressed(pygame.K_s) or is_key_just_pressed(pygame.K_d) \
                or is_key_just_pressed(pygame.K_ESCAPE):
            self.breakdown()

    # Destroy the window when the dialogue is done
    def breakdown(self):
        from core.engine import engine
        from core.area import area
        engine.active_objs.remove(self)
        for c in self.window.items:
            c.breakdown()

from core.engine import Engine
from stages.menu import menu
from stages.play import play
from stages.editor.choose_file import editor_choose_file
from stages.editor.edit_map import edit_map

e = Engine("Dungeon Decks")
e.register("Menu", menu)
e.register("Play", play)
e.register("EditorChooseFile", editor_choose_file)
e.register("EditorEditMap", edit_map)
e.switch_to("Menu")
e.run()

#import pygame
#from core.input import keys_down
#from components.player import Player
#from components.sprite import sprites, Sprite
#from core.map import TileKind, Map
#from core.camera import create_screen
#from components.entity import active_objs
#from components.physics import Body
#from core.area import Area, area
#from data.tile_typess import tile_kinds
#from components.label import labels
#
#pygame.init()
#
#screen = create_screen(1920, 1080, "Dungeon Decks")
#
#clear_color = (55, 0, 0)
#running = True
#
#area = Area("start.map", tile_kinds)
#
##Game Loop
#while running:
#
#    for event in pygame.event.get():
#        if event.type == pygame.QUIT:
#            running = False
#        elif event.type == pygame.KEYDOWN:
#            keys_down.add(event.key)
#                
#        elif event.type == pygame.KEYUP:
#            keys_down.discard(event.key)
#        
#    # Update Code
#    # Entity = player, Component = get(Player)
#    for a in active_objs:
#        a.update()
#
#    # Draw Code
#    screen.fill(clear_color)
#    area.map.draw(screen)
#    for s in sprites:
#        s.draw(screen)
#
#    for l in labels:
#        l.draw(screen)
#
#    pygame.display.flip()  # Update the display
#
#pygame.quit()
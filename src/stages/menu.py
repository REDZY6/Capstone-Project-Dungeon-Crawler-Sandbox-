from components.entity import Entity
from components.button import Button
from components.label import Label
from components.sprite import Sprite
from components.ui.menu_logo import FloatingLogo
from core.sound import Sound
import pygame

menu_music = None
play_music = None
panel_width = 600
panel_height = 400

def editor_press():
    from core.engine import engine
    global menu_music
    if menu_music:
        menu_music.stop()
    engine.switch_to("EditorChooseFile")

def new_game():
    from core.engine import engine
    global menu_music
    if menu_music:
        menu_music.stop()
    engine.switch_to("Play")
    global play_music
    play_music = Sound('dungeon_bgm.wav')
    play_music.loop()

def quit_game():
    from core.engine import engine
    engine.running = False

def menu():
    if play_music:
        play_music.stop()
        
    # Load the sprite image
    main_menu = Sprite("background.png", is_ui=True)

    # Resize the image using pygame.transform.scale
    scaled_image = pygame.transform.scale(main_menu.image, (1920, 1080))

    # Create a new Sprite with the scaled image
    main_menu.image = scaled_image
    Entity(main_menu)

    # Create and add the FloatingLogo (floating effect for the menu logo)
    logo = FloatingLogo(logo_sprite='Logo.png', x=960, y=250, amplitude=30, speed=0.5)

    #Entity(Sprite("main_menu.png", is_ui=True)) # is_ui = True to separate from other drawables
    
    new_game_button = Entity(Label("Montserrat-Bold.ttf",
                                        "New Game", 100,
                                        (255, 253, 208)))
    editor_button = Entity(Label("Montserrat-Bold.ttf",
                                        "Editor", 100,
                                        (255, 253, 208)))
    quit_game_button = Entity(Label("Montserrat-Bold.ttf",
                                        "Quit Game", 100,
                                        (255, 253, 208)))

    new_button_size = new_game_button.get(Label).get_bounds()
    editor_button_size = editor_button.get(Label).get_bounds()
    quit_button_size = quit_game_button.get(Label).get_bounds()

    global menu_music
    menu_music = Sound('menu_bgm.wav')
    menu_music.loop()

    new_game_button.add(Button(new_game, new_button_size)) # Function then button size
    editor_button.add(Button(editor_press, editor_button_size))
    quit_game_button.add(Button(quit_game, quit_button_size)) # Function then button size

    from core.camera import camera
    new_game_button.x = camera.width/2 - new_button_size.width/2 # Screen Size - button size
    new_game_button.y = camera.height - 500
    editor_button.x = camera.width/2 - editor_button_size.width/2 + 10# Screen Size - button size
    editor_button.y = camera.height - 350
    quit_game_button.x = camera.width/2 - quit_button_size.width/2
    quit_game_button.y = camera.height/2 + 350

    
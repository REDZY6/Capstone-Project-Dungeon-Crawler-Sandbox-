import pygame

audio_folder_location = "content/audio/sounds/"
sound_effects = {}
audio_enabled = True

# Volume range between 0.0 - 1.0, given that 1.0 is 100% of the audio
class Sound:
    def __init__(self, file, volume=1.0):
        self.file = file
        # First time of loading the sound.
        if not file in sound_effects:
            path = audio_folder_location + file
            sound_effects[file] = pygame.mixer.Sound(path)

        self.sound = sound_effects[file]
        self.sound.set_volume(volume)

    def play(self):
        if audio_enabled:
            pygame.mixer.Sound.play(self.sound)

    def loop(self):
        if audio_enabled:
            pygame.mixer.Sound.play(self.sound, loops=-1)
    
    def stop(self):
        self.sound.stop()

    def set_volume(self, volume):
        self.sound.set_volume(volume)
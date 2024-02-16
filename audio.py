"""
Holds all the code that makes the audio for the game.
"""
from kivy.core.audio import SoundLoader


def init_audio(self):
    """
    Initiates the audio files.
    """
    self.begin_audio = SoundLoader.load("audio/begin.wav")
    self.collision_audio = SoundLoader.load("audio/gameover_impact.wav")
    self.gameover_audio = SoundLoader.load("audio/gameover_voice.wav")
    self.restart_audio = SoundLoader.load("audio/restart.wav")
    self.music_audio = SoundLoader.load("audio/music1.wav")
    self.horizon_audio = SoundLoader.load("audio/horizon2.wav")
    self.menu_music = SoundLoader.load("audio/HaloByAtomMusicAudio.mp3")

    self.begin_audio.volume = 0.25
    self.collision_audio.volume = 0.6
    self.gameover_audio.volume = 0.25
    self.restart_audio.volume = 0.25
    self.music_audio.volume = 1
    self.horizon_audio.volume = 0.25
    self.menu_music.volume = 1


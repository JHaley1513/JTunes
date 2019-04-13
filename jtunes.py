"""Main driver file for JTunes mp3 player. Execute 'python3 JTunes.py' in Terminal/Command Prompt."""
from musicLibrary import MusicLibrary
from audioEngine import AudioEngine
from gui import GUI

lib = MusicLibrary('library.txt')
gui = GUI(AudioEngine(lib))
gui.loadgui()

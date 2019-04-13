import pygame
from songUtils import randomSongFromLibrary, randomSongFromAlbum
from random import randint

class AudioEngine:
    """Class for playing, pausing, shuffling, and otherwise interacting with the music library.
    The songs in the music library are represented by Song objects, each containing
    a path to the actual song file (.mp3), as well as other information about the song.

    The user interacts with AudioEngine via the GUI.
    """

    def __init__(self, lib=None):   #lib set to None if you want to run AudioEngine without a library.
        self.lib = lib
        self.currentArtistName = None
        self.currentAlbum = None
        self.currentSong = None
        self.songQueue = []
        self.queuePosition = 0
        self.repeat = False     #whether or not to repeat one song indefinitely
        self.playing = False
        pygame.mixer.init()

    def updateArtist(self, artistName=None):
        self.currentArtistName = artistName

    def updateAlbum(self, album=None):  #updates to None when going back to the library view.
        self.currentAlbum = album

    def isPlaying(self):    #used for the <Return> keybinding in the GUI class.
        return self.playing

    def newSong(self, song):
        """Called when a song's button is pressed in album view
         (not from pressing Prev, Next, or Shuffle).
         """
        if not self.repeat: #repeat is off, activate and play from the queue
            self.queueFrom(song, song.getTrackNum())
            self.play(self.songQueue[self.queuePosition])
        else:   #repeat is on, play the one song only
            self.play(song)

    def play(self, song):
        """Called when playing a new song (not when unpausing a previously started one)."""
        self.playing = True
        pygame.mixer.music.load(song.getPath())
        self.currentSong = song
        if not self.repeat:
            pygame.mixer.music.play()
        else:
            pygame.mixer.music.play(-1) #plays the song indefinitely
        # while pygame.mixer.music.get_busy():
        #     pygame.time.Clock().tick(10)

    def pauseSong(self):
        self.playing = False
        pygame.mixer.music.pause()

    def unpauseSong(self):
        self.playing = True
        pygame.mixer.music.unpause()

    def queueFrom(self, song, posInAlbum=-1):
        """Called with play() - this clears the current queue, queues
        all songs in the album that come after the selected song (if any), so that they'll
        play once the song finishes.

        posInAlbum represents the track number (position) of the song in its album.
        The queue loads up all the songs from that album and starts at that track number,
        to make it easy to go Prev/Next. posInAlbum = -1 when shuffling.
        """
        self.clearQueue()
        albumTracks = self.lib.getSongsFromAlbumName(song.getAlbumName())
        if posInAlbum > -1:  #queue all songs in album
            for s in albumTracks:
                self.songQueue.append(s)
            self.queuePosition = posInAlbum-1
        #self._printQueue()

    def _printQueue(self):
        for song in self.songQueue:
            if song is not None:
                print(str(song))
            else:
                print('None')
        print(self.queuePosition)

    def clearQueue(self):
        self.songQueue = []

    def prevSong(self):
        if self.currentSong is not None:
            if not self.repeat:
                if self.queuePosition > 0:
                    pygame.mixer.music.stop()
                    previous = self.songQueue[self.queuePosition-1]
                    self.queuePosition -= 1
                    self.play(previous)
                    return previous
            else:   #repeat the current song
                self.play(self.currentSong)
        else:
            return None

    def nextSong(self):
        if self.currentSong is not None:
            if not self.repeat:
                if self.queuePosition < len(self.songQueue)-1:
                    pygame.mixer.music.stop()
                    next = self.songQueue[self.queuePosition+1]
                    self.queuePosition += 1
                    self.play(next)
                    return next
            else:   #repeat the current song
                self.play(self.currentSong)
        else:
            return None

    def shuffle(self):
        """Shuffle-plays the tracks of the current album.

        If an album is currently selected, shuffles the current album.
        Otherwise (if user is viewing the list of all albums) shuffles the entire library.

        Returns the first song to be played (to allow the GUI to update).
        """
        if self.currentAlbum is not None:
            self._getShuffleOrder('album')
        else:
            self._getShuffleOrder('all')
        self.play(self.songQueue[0])
        return self.songQueue[0]

    def shuffleAll(self):
        self._getShuffleOrder('all')
        self.play(self.songQueue[0])
        return self.songQueue[0]

    def _getShuffleOrder(self, shuffleType):
        """shuffleType is a string, can be artist, album, or all, to shuffle
        from the current artist, album, or all songs by all artists."""
        def _slotInSongs(queue, alb):
            for song in alb.getAllSongs():
                while True:
                    pos = randint(0,totalSongs-1)
                    if queue[pos] is None:
                        queue[pos] = song
                        break

        #from song_library import albums, tracks
        totalSongs = 0
        if shuffleType == 'all':
            for alb in self.lib.getAllAlbums():
                totalSongs += len(alb)
        elif shuffleType == 'artist':
            for alb in self.lib.getAlbumsFromArtist(self.currentArtistName):
                totalSongs += len(alb)
        elif shuffleType == 'album':
            totalSongs += len(self.currentAlbum)
        self.songQueue = [None] * totalSongs
        #self._printQueue()

        if shuffleType == 'all':
            for alb in self.lib.getAllAlbums():
                _slotInSongs(self.songQueue, alb)
        elif shuffleType == 'artist':
            for alb in self.lib.getAlbumsFromArtist(self.currentArtistName):
                _slotInSongs(self.songQueue, alb)
        elif shuffleType == 'album':
            _slotInSongs(self.songQueue, self.currentAlbum)
        self.queuePosition = 0

    def repeatOn(self):
        """Called when repeat button says 'Repeat off'."""
        self.repeat = True

    def repeatOff(self):
        """Called when repeat button says 'Repeat on'."""
        self.repeat = False


if __name__ == '__main__':
    from Song import Song
    x = Song('X', 'Music Library/Blue Blood/05 X.mp3')
    engine = AudioEngine()
    engine.play(x)

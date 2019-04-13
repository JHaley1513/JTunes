class Song:
    """A representation that holds information about a particular song, as well as
    a path to the actual sound file it represents."""

    def __init__(self, name, path, artist='Unknown Artist', albumName='Unknown Album', trackNum=0, genre='', comments='', lyrics=''):
        """The last few parameters are optional in case you want to make a standalone
        instance of Song (i.e. outside a Library), in which case they would be unnecessary."""
        self.name = name
        self.path = path
        self.artist = artist
        self.albumName = albumName
        self.trackNum = trackNum
        self.genre = genre
        self.comments = comments
        self.lyrics = lyrics

    def __str__(self):
        return self.name

    def getName(self):
        return self.name

    def getPath(self):
        return self.path

    def getArtist(self):
        return self.artist

    def getAlbumName(self):
        return self.albumName

    def getTrackNum(self):
        return self.trackNum

    def getGenre(self):
        return self.genre

    def getComments(self):
        return self.comments

    def editComments(self, newComments):
        self.comments = newComments

    def getLyrics(self):
        return self.lyrics

    def editLyrics(self, newLyrics):
        self.lyrics = newLyrics

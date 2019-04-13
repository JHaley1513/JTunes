class MusicLibrary:
    """Stores Song objects together in one place, along with album and track information.

    Contains methods to get, add, and remove songs, albums, and artists
    """

    def __init__(self, libTxtFilename=''):
        self.fullLib = {} #key: artist name, value: list of Album objects
        self.libTxtFilename = libTxtFilename
        self.initLibrary()

    def initLibrary(self):
        if len(self.libTxtFilename) > 0:
            writeLibraryFromFile(self, self.libTxtFilename)

    def __str__(self):
        return dictToString(self.fullLib)

    def __len__(self):
        totalAlbums = 0
        for artistName in self.fullLib.keys():
            totalAlbums += len(self.fullLib[artistName])
        return totalAlbums

    def addAlbum(self, alb):
        """Adds an Album object to its artist's list of albums in the self.fullLib
        dictionary. If this is the first album added from the album's artist,
        create a new dictionary entry for the artist, otherwise add it to the
        existing dictionary entry's list of albums for that artist."""
        artist = alb.getArtistName()
        if artist in self.fullLib:
            self.fullLib[artist].append(alb)
        else:
            self.fullLib[artist] = [alb]

    def removeAlbum(self, albName):
        for artistName, alb in self.fullLib.items():
            if alb.getName() == albName:
                if len(self.fullLib[artistName]) > 1:
                    self.fullLib[artistName].remove(alb)
                else:
                    del self.fullLib[artistName]
                return True
        return False

    def getSongsFromAlbum(self, alb):
        """Returns all tracks (Song objects) from the selected album as a list.

        alb is an Album object.
        """
        return alb.getAllSongs()

    def getSongsFromAlbumName(self, albName):
        """albName is a string."""
        for alb in self.getAllAlbums():
            if alb.getName() == albName:
                return self.getSongsFromAlbum(alb)
        raise ValueError('Album not found with name', albName)

    def getSongsFromArtist(self, alb):
        pass

    def getAlbumsFromArtist(self, artistName):
        """Returns a list of all the albums by the desired artist."""
        return self.fullLib[artistName]

    def getAllAlbums(self):
        allAlbums = []
        for artistName in self.fullLib.keys():
            allAlbums.extend(self.getAlbumsFromArtist(artistName))
        return allAlbums

    def allArtistNames(self):
        """Returns a list of the names of all the artists who have songs in this library."""
        return list(self.fullLib.keys())



def writeLibraryFromFile(lib, filename):
    from song import Song
    from album import Album
    import songUtils
    f = open(filename, 'r')
    consecNewlines = 0
    artistName = ''
    albumName = None
    tracklist = []

    for line in f: #line can be '\n' at minimum, for a newline
        if line == '\n':
            consecNewlines += 1
            if albumName: #just finished parsing through an album, now build and add the album
                newAlbum = Album(albumName, artistName, tracklist, year, copyrightInfo)
                lib.addAlbum(newAlbum)
                albumName = None
        else:                           # we're at a non-empty line, so count the number of consecutive empty lines before this line to see if we've gone to a new album/artist
            line = line.rstrip('\n')
            if consecNewlines == 2:     # a new artist
                artistName = line
                consecNewlines = 0
            elif consecNewlines == 1:   # a new album from the same artist
                albumName, year, copyrightInfo = _albumInfoFromLine(line)
                tracklist = []
                consecNewlines = 0
            else: # another song from the current album and artist
                #print(line)
                songName, genre, comments, lyrics = _songInfoFromLine(line)
                trackNum = len(tracklist) + 1
                path = songUtils.getSongPath(songName, trackNum, artistName, albumName)
                newSong = Song(songName, path, artistName, albumName, trackNum, genre, comments, lyrics)
                tracklist.append(newSong)
    f.close()



def _albumInfoFromLine(line):
    copyrightAndOthers = _divideInTwo(line, '\\\\')
    copyright, others2 = copyrightAndOthers[1], copyrightAndOthers[0]
    yearAndOthers = _divideInTwo(others2, '\\')
    year, others = yearAndOthers[1], yearAndOthers[0]
    name = others
    return name, year, copyright

def _songInfoFromLine(line):
    lyricsAndOthers = _divideInTwo(line, '\\\\\\')
    lyrics, others3 = lyricsAndOthers[1], lyricsAndOthers[0]
    commentsAndOthers = _divideInTwo(others3, '\\\\')
    comments, others2 = commentsAndOthers[1], commentsAndOthers[0]
    genreAndOthers = _divideInTwo(others2, '\\')
    genre, others = genreAndOthers[1], genreAndOthers[0]
    name = others
    return name, genre, comments, lyrics

def _divideInTwo(item, divide_on):
    divided = item.split(divide_on)
    if len(divided) == 1: # if there was nothing on the other side of divide_on, we still want to add an empty item, to normalize output list length
        divided.append('')
    divided[0] = divided[0].rstrip(' ')
    divided[1] = divided[1].lstrip(' ')
    return divided

def dictToString(d): #a sample of this is given in sampleLibrary.py
    #strRep = ['{']
    strRep = []
    for artistName, albumList in d.items():
        strRep.append(artistName + ':')
        for alb in albumList:
            strRep.append('Album ' + alb.getName() + ' contains:')
            strRep.append(alb.strWithIndent(3))
    #strRep.append('}')
    strRep = '\n'.join(strRep)
    return strRep


if __name__ == '__main__':
    newlib = MusicLibrary('library.txt')
    print(newlib)

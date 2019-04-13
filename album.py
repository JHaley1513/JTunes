class Album:
    def __init__(self, name, artist, songs, year=0, copyright=''):
        self.name = name
        self.artist = artist # can be a list if the album is a compilation, otherwise a string
        self.songs = songs
        self.year = year
        self.copyright = copyright
        #self.isCompilation = isCompilation

    def __len__(self):
        return len(self.songs)

    def __str__(self):
        songNames = self.getSongNames()
        strRep = []
        line = ''
        for idx, name in enumerate(songNames):
            if len(line) + len(name) > 60: #keep line length at 60 or below, to maximize readability
                strRep.append(line)
                line = ''
            line += name
            if idx < len(songNames) - 1:
                line += ', '
        strRep.append(line)
        strRep = '[' + '\n'.join(strRep) + ']'
        return strRep

    def strWithIndent(self, amount_indent):
        songNames = self.getSongNames()
        strRep = []
        line = '    ' * amount_indent
        for idx, name in enumerate(songNames):
            if len(line) + len(name) > 60: #keep line length at 60 or below, to maximize readability
                strRep.append(line)
                line = ' ' * 4 * amount_indent
            line += name
            if idx < len(songNames) - 1:
                line += ', '
        strRep.append(line)
        #strRep = '[' + '\n'.join(strRep) + ']'
        strRep = '\n'.join(strRep)
        return strRep

    def getName(self):
        return self.name

    def getArtistName(self):
        """self.artist is a string if all the tracks were done by one artist, and
        a list of strings if there's more than one artist (i.e. it's a compilation album).
        """
        return self.artist

    def getAllSongs(self):
        """self.songs is a Python list of the album's songs. Each song
        is represented by a Song object. The list's order does not matter as each Song object
        contains a reference to its own track number.
        """
        return self.songs

    def getSongNames(self):
        """Returns an ordered list of song names, ordered by track number."""
        allTracks = []
        tracks = {}
        for s in self.songs:        # first group songs by track number - some songs might have the same
                                    # track number (usually if the user set them that way by accident)
            trackNum = s.getTrackNum()
            if trackNum in tracks:
                tracks[trackNum].append(s)
            else:
                tracks[trackNum] = [s]
        trackNums = []
        for num in tracks.keys():   # then find all the possible track numbers
            trackNums.append(num)
        trackNums.sort()            # then sort them from least to greatest
        for n in trackNums:         # finally, append songs to allTracks list in order of track number.
            for s in tracks[n]:
                allTracks.append(s.getName())
        return allTracks

    def addSong(self, newSong):
        """Takes a new Song object and appends it to the list of the album's songs. Each song
        is represented by a Song object. The list's order does not matter as each Song object
        contains a reference to its own track number.
        """
        self.songs.append(newSong)

    def removeSong(self, songObj):
        """Takes the Song instance of the desired song as an argument. If the song
        is in this album, remove the song and return True. Otherwise return False."""
        for i, s in self.songs.enumerate():
            if s == songObj:
                del self.songs[i]
                return True
        return False

    def getNumSongs(self):
        return len(self.songs)

    def getGenre(self):
        """Returns the name of the most commonly occurring genre among the album's songs.
        If there's a tie, then one of the tied-for-the-most common genre names is returned.
        """
        genres = {}
        for s in self.songs:
            songGenre = s.getGenre()
            if len() > 0:
                if songGenre in genres:
                    genres[songGenre] += 1
                else:
                    genres[songGenre] = 1
        mostSongs = 0
        mainGenre = ''
        for genre, total in genres.items():
            if total > mostSongs:
                mostSongs = total
                mainGenre = genre
        return mainGenre

    def getYear(self):
        """Returns the integer value of the year in which the song was made."""
        return self.year

    def editYear(self, newYear):
        self.year = newYear

    def getCopyrightInfo(self):
        """Example: ℗ 2001 Sony Music Entertainment Inc."""
        return self.copyright

    def editCopyrightInfo(self, newCopyright):
        self.copyright = newCopyright

    # def isCompilationAlbum(self):
    #     return self.isCompilation

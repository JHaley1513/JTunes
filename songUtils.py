from random import randint
import os

audio_extensions = ['mp3', 'm4a', 'wav', 'aif', 'aiff', 'ogg']
image_extensions = ['jpg', 'jpeg', 'png']

def getSongPath(songName, trackNum, artistName, albumName):
    """Generates the song path to be fed into the Audio Engine."""
    path = 'Music_Library/' + artistName + '/' + albumName + '/'
    if trackNum < 10:   #put the song's track number before its name (if single digit, preceded by a 0)
        path += '0'
    path += str(trackNum)
    path += ' ' + songName
    path += _getAudioExtension(path)
    return path

def _getAudioExtension(songPath):
    for ext in audio_extensions:
        if os.path.isfile(songPath + '.' + ext):
            return '.' + ext
    raise FileNotFoundError('File not found for any audio extension:', songPath)

def getImagePath(alb):
    """@album: string, name of album."""
    path = 'Album_Covers/' + alb.getArtistName() + '/' + alb.getName()
    return path + _getImageExtension(path)

def _getImageExtension(imagePath):
    for ext in image_extensions:
        if os.path.isfile(imagePath + '.' + ext):
            return '.' + ext
    raise FileNotFoundError('File not found for any image extension:', imagePath)

def randomSongFromLibrary(lib):
    """@lib: Library object from which a song is chosen."""
    randNum = randint(0, len(lib.allAlbumNames)-1)
    randAlbum = lib.allAlbumNames[randNum]
    return randomSongFromAlbum(lib, randAlbum)


def randomSongFromAlbum(lib, alb):
    """@album: string, name of album."""
    albumTracks = lib.getSongsFrom(alb)   #list of tracks
    randTrackNum = randint(1, len(albumTracks))
    return albumTracks[randTrackNum]    #returns a Song object

def overwriteFilename(source, dest):
    def _incrementNumber(dest, i): #the number that's added to the end of the name of a duplicate song file
        nameAndExtension = dest.split('.')
        name, extension = nameAndExtension[0], nameAndExtension[1]

        if i > 1:
            numDigitsToRemove = len(str(i))
            keep = len(name) - numDigitsToRemove - 1 #includes 1 for the space between song's name and duplicate number
            name = name[:keep]
        name = name + ' ' + str(i)
        dest = name + '.' + extension
        return(dest)

    i = 1
    if not os.path.exists(source):
        raise ValueError('No such path exists:', source)
    while os.path.exists(dest):
        dest = _incrementNumber(dest, i)
        i += 1
    try:
        os.rename(source, dest)
    except WindowsError:
        os.remove(dest)
        os.rename(source, dest)

if __name__ == '__main__':
    overwriteFilename('x2 1.txt', 'x2.txt')
    overwriteFilename('x3.txt', 'x4.txt')

from tkinter import Tk, Frame, Label, Canvas, Button, Text
from tkConstants import *
from functools import partial
from PIL import Image, ImageTk
from songUtils import getImagePath

class GUI:
    """Class to handle loading and changing screens in the GUI. Allows the
    user to interact with the audio engine.
    """

    def __init__(self, engine): #engine is an AudioEngine object, lib is a Library object
        self.engine = engine
        self.lib = engine.lib  # used to display artist name and albums, and to load the buttons for all songs.

        """These variables will not be reassigned values"""
        self.root = Tk()
        self.root.title('JTunes Library')
        self.root.geometry('947x606')

        self.topFrame = Frame()
        self.mainFrame = Frame()
        self.topFrame.grid(row=0, column=0, sticky=W)
        self.mainFrame.grid(row=1, column=0, sticky=W)

        """These variables will be reassigned when changing screens"""
        self.banner = Label(self.mainFrame, text='My Music', font=("Arial Black", 32))
        self.banner.grid(row=3, column=0)
        self.libraryCanvases = []  #initialized in loadLibraryView()
        self.albumCovers = []
        self.albumButtons = []
        self.songButtons = []

        self.nowPlaying = Text(self.topFrame, width=39, height=1, wrap=WORD, bg='light grey')
        self.nowPlaying.grid(row=0, column=5, sticky=W)
        self.nowPlayingSubtitle = Text(self.topFrame, width=39, height=1, wrap=WORD, bg='light grey')
        self.nowPlayingSubtitle.grid(row=1, column=5, sticky=W)


        self.nowPlaying.configure(state='disabled') #makes it so that the user can't edit them.
        self.nowPlayingSubtitle.configure(state='disabled')

        self.backButton = None   #only set to a Button object when in album view

        self.playButton = Button(self.topFrame, text = 'PLAY', width=6)
        self.playButton.grid(row=0, column=3, sticky=W)
        #playButton starts as a dummy button before any song starts playing.
        #is replaced with 'PAUSE' button when playing music.

        self.repeatButton = Button(self.topFrame, text = 'Repeat is off', width=10, command = self.turnRepeatOn)
        self.repeatButton.grid(row=0, column=8, sticky=W)
        #is replaced with 'Repeat is on' when repeat is turned on, using turnRepeatOn().

        """Key bindings"""
        self.root.bind('<Return>', lambda event: self.pauseOrUnpause())
        self.root.bind('<space>', lambda event: self.pauseOrUnpause())
        self.root.bind('<Left>', lambda event: self.playPrev())
        self.root.bind('<Right>', lambda event: self.playNext())

    """Initializing Frame, basic widgets, etc."""
    def initTopBanner(self):
        #back button, pause button, play button (used when un-pausing), skip button,
        #shuffle button, shuffle-all button, repeat on-off button, quit button
        Button(self.topFrame, text = 'Quit', width=6, command = self.root.quit).grid(row=0, column=0, sticky=W)
        Button(self.topFrame, text = 'Prev', width=6, command = self.playPrev).grid(row=0, column=2, sticky=W)
        Button(self.topFrame, text = 'Next', width=6, command = self.playNext).grid(row=0, column=4, sticky=W)

        #The space for song name (row 0, col 5) and artist/album (row 1, col 5) start out blank. (these are in topFrameCtr)

        Button(self.topFrame, text = 'Shuffle', width=8, command = self.startShuffle).grid(row=0, column=6, sticky=W)
        Button(self.topFrame, text = 'Shuffle All', width=8, command = self.startShuffleAll).grid(row=0, column=7, sticky=W)



################################# CALLED WHEN CHANGING SCREENS #################################



    """Add/delete Album and Song buttons (to be called when changing screens).
    Plus a Back button.
    Library view: you are viewing the names and images of all the individual albums.
    Album view: you are viewing the individual tracks of one particular album.
    """
    def loadLibraryView(self):  #displays all Album images and Buttons
        # add text at top of screen (below the top bar): artist name.
        self.banner.config(text='My Music')
        self.engine.updateAlbum(None)

        ALBUMS_PER_LINE = 6
        num_albums = 0
        for alb in self.lib.getAllAlbums():
            #album canvas
            canvas = Canvas(self.mainFrame, width=150, height=150)
            self.libraryCanvases.append(canvas)
            canvas.grid(row=4 * (1 + num_albums // ALBUMS_PER_LINE), column=num_albums % ALBUMS_PER_LINE, sticky=W)

            #album image
            imagePath = getImagePath(alb)
            im = Image.open(imagePath)
            im = im.resize((150,150), Image.ANTIALIAS)
            albumArt = ImageTk.PhotoImage(im)
            self.albumCovers.append(albumArt)   #save a reference to the image
            cover = self.libraryCanvases[num_albums].create_image(0, 0, anchor=NW, image=albumArt)

            #album button (to select album; goes below album image)
            temp = Button(self.mainFrame, text = alb.getName(), width=14, command = partial(self.loadAlbumView, alb))
            temp.grid(row=5 * (1 + num_albums // ALBUMS_PER_LINE), column=num_albums % ALBUMS_PER_LINE)
            self.albumButtons.append(temp)   #storing in a list, to make it easier to remove them later
            num_albums += 1

    def deleteLibraryView(self):
        """Clears the library view by removing all the album buttons, canvases, and covers,
        so that the album view can then be loaded.
        """
        for i in self.albumButtons:
            i.destroy()
        self.albumButtons = []
        self.albumCovers = []
        for c in self.libraryCanvases:
            c.destroy()
        self.libraryCanvases = []

    def loadAlbumView(self, album):
        """Displays the tracks of an individual album.

        @album: Album object
        """
        self.deleteLibraryView()       #clear the previous screen first

        bannerText = album.getArtistName() + ' - ' + album.getName()
        self.banner.config(text=bannerText)

        canvas = Canvas(self.mainFrame, width=150, height=150)
        self.libraryCanvases.append(canvas)
        canvas.grid(row=4, column=0, sticky=W)

        imagePath = getImagePath(album)
        im = Image.open(imagePath)
        im = im.resize((150,150), Image.ANTIALIAS)
        albumArt = ImageTk.PhotoImage(im)
        self.albumCovers.append(albumArt)   #save a reference to the image
        cover = self.libraryCanvases[0].create_image(0, 0, anchor=NW, image=albumArt)

        self.backButton = Button(self.topFrame, text = 'Back', width=6, command=self.exitAlbumView)
        self.backButton.grid(row=1, column=0, sticky=W)

        self.engine.updateAlbum(album)      #tells the audio engine which album is being viewed, so it knows to load songs from this album if you click PLAY or SHUFFLE.

        #load the button for each individual track
        trackNum = 1
        for song in self.lib.getSongsFromAlbum(album):
            temp = Button(self.mainFrame, text = str(song), width=14, command = partial(self.playSong, song))
            temp.grid(row=trackNum+4, column=0, sticky=W)
            self.songButtons.append(temp)
            trackNum += 1

    def deleteAlbumView(self):
        """Clears the album view so that the library view can then be loaded.

        Also removes the back button as it's not needed in library view.
        """
        for i in self.songButtons:
            i.destroy()
        self.songButtons = []
        self.albumCovers = []
        for c in self.libraryCanvases:
            c.destroy()
        self.libraryCanvases = []
        self.backButton.destroy()
        self.engine.updateAlbum(None)       #informs the audio engine that you're no longer viewing an album.



###################################### BUTTON SUBROUTINES ######################################



    """The following subroutines call their counterparts in the AudioEngine class,
    and apply any corresponding updates to the GUI interface.
    """
    def exitAlbumView(self):
        """Called when the Back button is pressed in album view.

        The Back button does not exist in library view.
        """
        self.deleteAlbumView()
        self.loadLibraryView()

    def pauseOrUnpause(self):
        """Used for the <Return> keybinding; calls pause() or unpause() depending
        on whether a song is currently playing.
        """
        if self.engine.isPlaying():
            self.pause()
        else:
            self.unpause()

    def playSong(self, song):
        """Called when a song is clicked on to be played.
        Destroys the current play button and replaces with one that says 'PAUSE'.

        @song: a Song object
        """
        self.engine.newSong(song)
        self._updateNowPlaying(song)
        self._changePlayButton('PAUSE')

    def pause(self):
        """Called when the play button is pressed while displaying 'PAUSE'.

        Destroys the current play button and replaces with one that says 'PLAY'.
        """
        self.engine.pauseSong()
        self._changePlayButton('PLAY')

    def unpause(self):
        """Called when the play button is pressed while displaying 'PLAY'.

        Destroys the current play button and replaces with one that says 'PAUSE'.
        """
        self.engine.unpauseSong()
        self._changePlayButton('PAUSE')

    def _updateNowPlaying(self, song):
        """Updates the Now Playing and Subtitle text boxes."""
        if song is not None:    #will be None if you try go Prev/Next while no song is currently playing.
            #first unlock the text boxes to enable editing
            self.nowPlaying.configure(state='normal')
            self.nowPlayingSubtitle.configure(state='normal')

            #remove the text from the previous song, replace with current
            self.nowPlaying.delete(1.0, END)
            self.nowPlaying.insert(END, str(song))
            self.nowPlayingSubtitle.delete(1.0, END)
            self.nowPlayingSubtitle.insert(END, song.getArtist() + ' - ' + song.getAlbumName())

            #set text to center justify (default is left justify)
            self.nowPlaying.tag_configure("center", justify=CENTER)
            self.nowPlaying.tag_add("center", 1.0, "end")
            self.nowPlayingSubtitle.tag_configure("center", justify=CENTER)
            self.nowPlayingSubtitle.tag_add("center", 1.0, "end")

            #now re-disable the text boxes so that the user can't edit them.
            self.nowPlaying.configure(state='disabled')
            self.nowPlayingSubtitle.configure(state='disabled')

    def playPrev(self):
        song = self.engine.prevSong()
        self._updateNowPlaying(song)

    def playNext(self):
        song = self.engine.nextSong()
        self._updateNowPlaying(song)

    def _changePlayButton(self, changeTo):
        """@changeTo: 'PLAY' or 'PAUSE'"""
        self.playButton.destroy()
        if changeTo == 'PLAY':
            self.playButton = Button(self.topFrame, text = changeTo, width=6, command = self.unpause)
        elif changeTo == 'PAUSE':
            self.playButton = Button(self.topFrame, text = changeTo, width=6, command = self.pause)
        self.playButton.grid(row=0, column=3, sticky=W)

    def startShuffle(self):
        song = self.engine.shuffle()
        self._changePlayButton('PAUSE')
        self._updateNowPlaying(song)

    def startShuffleAll(self):
        song = self.engine.shuffleAll()
        self._changePlayButton('PAUSE')
        self._updateNowPlaying(song)

    def turnRepeatOn(self):
        """Called when the repeat button is pressed while displaying 'Repeat is off'.

        Destroys the current repeat button and replaces with one that says 'Repeat is on'.
        """
        self.engine.repeatOn()
        self._changeRepeatButton('on')

    def turnRepeatOff(self):
        """Called when the repeat button is pressed while displaying 'Repeat is on'.

        Destroys the current repeat button and replaces with one that says 'Repeat is off'.
        """
        self.engine.repeatOff()
        self._changeRepeatButton('off')

    def _changeRepeatButton(self, changeTo):
        """@changeTo: 'on' or 'off'"""
        self.repeatButton.destroy()
        if changeTo == 'on':
            self.repeatButton = Button(self.topFrame, text = 'Repeat is on', width=10, command = self.turnRepeatOff)
        elif changeTo == 'off':
            self.repeatButton = Button(self.topFrame, text = 'Repeat is off', width=10, command = self.turnRepeatOn)
        self.repeatButton.grid(row=0, column=8, sticky=W)



########################################## MAIN LOOP ##########################################



    def loadgui(self):
        """To be called by an outside driver module"""
        self.initTopBanner()
        self.loadLibraryView()
        self.root.mainloop()

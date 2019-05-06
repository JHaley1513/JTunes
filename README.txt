J. Haley, August '18

JTunes is an MP3 player written in Python, using PyGame for the audio engine
and Tkinter for the GUI.
To run JTunes, simply navigate to the JTunes project folder using Terminal/Command line
and execute the command "python3 jtunes.py".

JTunes doesn't come loaded with anything in the Music_Library and Album_Covers folders; however, it comes with preloaded metadata for a number of songs and albums in library.txt.
You can download the corresponding Music_Library and Album_Covers from the following Google Drive link: https://drive.google.com/open?id=1o1SIsnO_ugnt-rpXxeJZ0NgwULDwUuzJ
Just replace the existing Music_Library and Album_Covers folders with the ones you downloaded, and you'll be all set.

In addition to the preloaded songs, currently we have a simple system for the user to add your own songs, albums, and artists. It requires manually adding and editing files in the project folder - full details below.
We also have a framework in place to add and edit lyrics, copyright, and other info for songs and albums,
but haven't yet implemented a way to enable this for the user in the GUI.

TO DO
Implement a system to edit song info within the GUI, as well as create a more user-friendly way to add new songs and artists.


--ADDING NEW SONGS--

Artists, Albums, and Songs are loaded by the MusicLibrary, via information read from library.txt.
If you've added a new artist, album, or song, you must add the corresponding information into library.txt, to make the MusicLibrary aware of your changes.
To add a new artist to library.txt, put two empty line breaks before the artist name.
Then, add another empty line break, then add the name of the artist's album.
Add a \ and a space, then put the album's release year (if you'd like) followed by another space (only if you added the year).
Add a \\ and copyright info (if any).
On the following lines, add each track name in order of track listing.
Genre goes after \, notes or comments go after \\, and lyrics go after \\\.
Afterwards, add an empty line break before another album by the same artist, or add two empty line breaks before a different artist.

To add the actual artist/album/song files and folders, navigate to JTunes/Music_Library and just drop 'em in there.
Note that you'll need to include the track number at the beginning of each song's name - see the
pre-loaded songs for reference.

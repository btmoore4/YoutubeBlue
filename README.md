# YoutubeBlue

A simple script that periodically checks a user's specified playlist and downloads them to a directory. 
I use Dropbox to sync downloaded videos to all my devices. 
Mainly a way to download youtube videos synced to a specifc playlist for offline viewing. 

## Installation: 
1. Clone the repoisitory and change into the main directory. 
```
git clone https://github.com/btmoore4/YoutubeBlue.git && cd YoutubeBlue
```
2. Download the dependencies.
```
pip install youtube-dl
```
3. Run the script. 
```
python download_playlist.py [PATH TO DESTINATION DIRECTORY] --playlist [PLAYLIST_ID]
python download_playlist.py [PATH TO DESTINATION DIRECTORY] --playlist [PLAYLIST_ID] --repeat [NUM_TIMES_TO_REPEAT]
```

## Notes: 
  * Program defaults to checking the playlist every hour.
  * Program defaults to not repeating.

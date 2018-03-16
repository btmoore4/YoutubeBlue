# YoutubeBlue

A simple script that periodically checks a user's youtube subscriptions and downloads them to a directory. 
I use Dropbox to sync downloaded videos to all my devices. 
Mainly a way to download youtube videos without YoutubeRed. 

## Installation: 
1. Clone the repoisitory and change into the main directory. 
```
git clone https://github.com/btmoore4/YoutubeBlue.git && cd YoutubeBlue
```
2. Download the dependencies.
```
pip install youtube-dl
pip install --upgrade google-api-python-client
```
3. Add a .txt file containing your Youtube API key. 
```
echo '<YOUTUBE API KEY>' > key.txt
```
4. Add a .txt file containing the Youtube User Channel ID who's subscriptions you would like to download. 
```
echo '<YOUTUBE USER CHANNEL ID>' > user.txt
```
5. Run the script. 
```
python script.py <PATH TO DESTINATION DIRECTORY> --key key.txt --user user.txt
```

## Notes: 
  * Program defaults to fetching 1 days worth of subscriptions and checks every 60 minutes. 

import sys
import os
import glob
import argparse
import socket
import datetime
import time
import threading
from subprocess import call
from apiclient.discovery import build

DOWNLOAD_INTERVAL = 60*60
CHECK_INTERVAL = 10

#YoutubeBlue CML Arguements
def parse_arguements(): 
    parser = argparse.ArgumentParser(description='Process some YoutubeBlue Args.')
    parser.add_argument('dest', nargs='+', help='Downloads Destination')
    parser.add_argument('--playlist', nargs='?', help='Youtube Playlist ID')
    parser.add_argument('--repeat', nargs='?', help='Number of Times the script runs')
    args = parser.parse_args()
    
    if not args.dest or len(args.dest) != 1 or not os.path.isdir(args.dest[0]):
        print("No destination path. Exiting...")
        sys.exit(0)
    if not args.playlist:
        print("--playlist Arg is Invalid. Exiting...")
        sys.exit(0)
    return args

#YoutubeBlue Main
def youtube_blue_playlist_main():
    print("Starting YoutubeBlue Playlist Stashing Script...")
    args = parse_arguements()
    OUTPUT_DIR = args.dest[0]
    PLAYLIST_ID = args.playlist
    REPEAT = 100 if (args.repeat is None) else int(args.repeat)
    download_repeat(DOWNLOAD_INTERVAL, REPEAT, CHECK_INTERVAL, PLAYLIST_ID, OUTPUT_DIR)

#Executes get_videos Periodically
def download_repeat(execution_interval, repeat, check_interval, playlist_url, output_directory):
    count = 0
    while (count < repeat):
        start_time = datetime.datetime.now()
        execute_time = start_time + datetime.timedelta(seconds=execution_interval)
        print("Starting Process at " + start_time.isoformat())
        print("Next Execution at " + execute_time.isoformat())
        count = count + 1
        try: 
            download_playlist(playlist_url, output_directory)
            print("Execution Complete waiting until " + execute_time.isoformat())
        except socket.timeout as e:
            print("Exception Raised during Execution. Waiting until " + execute_time.isoformat())
            print(e)
        while(execute_time > datetime.datetime.now()):
            time.sleep(check_interval)

def download_playlist(playlist_url, output_directory):
    call(["youtube-dl", "-o", output_directory+"/%(title)s.%(ext)s", playlist_url])

if __name__ == "__main__":
    youtube_blue_playlist_main()

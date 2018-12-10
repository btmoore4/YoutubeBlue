import sys
import os
import argparse
import socket
import datetime
import time
import subprocess

#Parser function for youtube_blue cml arguements
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

#Main function to call youtube-dl
def download_playlist(playlist_url, output_directory):
    subprocess.call(["youtube-dl", "-o", output_directory+"/%(title)s.%(ext)s", playlist_url])

#Utility function to repeat periodically
def repeat_function(target_function, repeat=1, execution_interval=3600, check_interval=10):
    for count in range(0, repeat):
        start_time = datetime.datetime.now()
        execute_time = start_time + datetime.timedelta(seconds=execution_interval)
        print(f"Starting Process #{count} at {start_time.isoformat()}")
        try: 
            target_function()
            print(f"Execution #{count} Complete.")
        except socket.timeout as e:
            print(f"Execution Raised during Execution #{count}: {e}")
        if count != repeat - 1:
            print(f"Next Execution at {execute_time.isoformat()}")
            while(execute_time > datetime.datetime.now()):
                time.sleep(check_interval)
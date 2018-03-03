"""This module is used to download Youtube Subscriptions"""

"""Requirements:                                        """
"""  -- yotube-dl;                                      """
"""  -- google Youtube API                              """

import sys
import os
import argparse
import datetime
import time
import threading
from subprocess import call
from apiclient.discovery import build

DOWNLOAD_INTERVAL = 60*30
CHECK_INTERVAL = 10
NUM_DAYS = 1


#YoutubeBlue CML Arguements
def parse_arguements(): 
    parser = argparse.ArgumentParser(description='Process some YoutubeBlue Args.')
    parser.add_argument('dest', nargs='+', help='Downloads Destination')
    parser.add_argument('--key', nargs='?', help='Youtube API Key Text File')
    parser.add_argument('--user', nargs='?', help='Youtube User Channel ID Text File')
    args = parser.parse_args()
    
    if not args.dest or len(args.dest) != 1 or not os.path.isdir(args.dest[0]):
        print("No destination path. Exiting...")
        sys.exit(0)
    if not args.key or not os.path.isfile(args.key):
        print("--key Arg is Invalid. Exiting...")
        sys.exit(0)
    if not args.user or not os.path.isfile(args.user):
        print("--user Arg is Invalid. Exiting...")
        sys.exit(0)

    return args


#YoutubeBlue Main
def youtube_blue_main():
    print("Starting YoutubeBlue Stashing Script...")

    args = parse_arguements()

    OUTPUT_DIR = args.dest[0]
    with open(args.key) as inputfile:
        for line in inputfile:
            KEY = line
    with open(args.user) as inputfile:
        for line in inputfile:
            USER = line

    repeat_task(USER, DOWNLOAD_INTERVAL, CHECK_INTERVAL, KEY, OUTPUT_DIR, NUM_DAYS)


#Executes get_videos Periodically
def repeat_task(user_id, execution_interval, check_interval, key, output_directory, num_days):
    while (True):
        start_time = datetime.datetime.now()
        execute_time = start_time + datetime.timedelta(seconds=execution_interval)
        print("Starting Process at " + start_time.isoformat())
        print("Next Execution at " + execute_time.isoformat())
        get_videos(get_subs(user_id, key), key, output_directory, num_days)
        print("Execution Complete waiting until " + execute_time.isoformat())
        while(execute_time > datetime.datetime.now()):
            time.sleep(check_interval)


#Get Subscriptions from User
def get_subs(user_id, key):
    youtube = build('youtube', 'v3', developerKey=key)
    sub_response = youtube.subscriptions().list(
        part='snippet',
        channelId=user_id,
        maxResults=50
        ).execute()
    subs = []
    for sub in sub_response['items']:
        subs.append(sub['snippet']['resourceId']['channelId'])
    return subs


#Downloads Videos from Channels in Channel List
def get_videos(channel_list, key, output_directory, num_days):
    TIME_STRING = (datetime.datetime.now() - datetime.timedelta(days=num_days)).isoformat()
    TIME_STRING = TIME_STRING.split('T')[0]+"T00:00:00Z"
    youtube = build('youtube', 'v3', developerKey=key)
    VIDEO_LIST = []
    for CHANNEL in channel_list:
        search_response = youtube.search().list(
            part="id",
            type='video',
            order='date',
            channelId=CHANNEL,
            maxResults=5,
            videoDuration="short", 
            publishedAfter=TIME_STRING
            ).execute()
        for item in search_response['items']: 
            VIDEO_LIST.append(item['id']['videoId'])
    for VIDEO in VIDEO_LIST: 
        call(["youtube-dl", "-o", output_directory+"/%(title)s.%(ext)s", VIDEO])

    VIDEO_LIST = []
    for CHANNEL in channel_list:
        search_response = youtube.search().list(
            part="id",
            type='video',
            order='date',
            channelId=CHANNEL,
            maxResults=5,
            videoDuration="medium", 
            publishedAfter=TIME_STRING
            ).execute()
        for item in search_response['items']: 
            VIDEO_LIST.append(item['id']['videoId'])
    for VIDEO in VIDEO_LIST: 
        call(["youtube-dl", "-o", output_directory+"/%(title)s.%(ext)s", VIDEO])

    delete_old(output_directory, num_days+1)


#Deletes older videos
def delete_old(output_directory, days_delete):
    if os.name == 'nt':
        print("Cannot Delete on Windows")
        return
    print("Deleting the Following Videos...")
    call(["find", output_directory, "-mindepth", "1", "-mtime", "+"+str(days_delete), "-depth", "-print"])
    call(["find", output_directory, "-mindepth", "1", "-mtime", "+"+str(days_delete), "-delete"])


if __name__ == "__main__":
    youtube_blue_main()

"""This module is used to download Youtube Subscriptions"""

"""Requirements:                                        """
"""  -- yotube-dl;                                      """
"""  -- google Youtube API                              """

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

        try: 
            get_videos(get_subs(user_id, key), key, output_directory, num_days)
            print("Execution Complete waiting until " + execute_time.isoformat())
        except socket.timeout as e:
            print("Exception Raised during Execution. Waiting until " + execute_time.isoformat())
            print(e)
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

    video_id_list = []
    video_title_list = []
    for CHANNEL in channel_list:
        search_response = youtube.search().list(
            part="id,snippet",
            type='video',
            order='date',
            channelId=CHANNEL,
            maxResults=5,
            videoDuration="short", 
            publishedAfter=TIME_STRING
            ).execute()
        for item in search_response['items']: 
            video_title_list.append(item['snippet']['title']+".mp4")
            video_id_list.append(item['id']['videoId'])

    for CHANNEL in channel_list:
        search_response = youtube.search().list(
            part="id,snippet",
            type='video',
            order='date',
            channelId=CHANNEL,
            maxResults=5,
            videoDuration="medium", 
            publishedAfter=TIME_STRING
            ).execute()
        for item in search_response['items']: 
            video_title_list.append(item['snippet']['title']+".mp4")
            video_id_list.append(item['id']['videoId'])

    for video_id in video_id_list: 
        call(["youtube-dl", "-o", output_directory+"/%(title)s.%(ext)s", video_id])

    delete_old(output_directory, video_title_list)


#Deletes older videos
def delete_old(output_directory, titles):
    os.chdir(output_directory)
    titles = [title.replace('|', '_') for title in titles]
    titles = [title.replace('"', '\'') for title in titles]
    titles = [title.replace(':', ' -') for title in titles]
    titles = [title.replace('?', '') for title in titles]
    for file in glob.glob("*"):
        if file in str(titles):
            continue 
        print("Deleting " + file)
        call(["rm", file])


if __name__ == "__main__":
    youtube_blue_main()

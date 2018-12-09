import youtube_blue

#YoutubeBlue Main
def youtube_blue_playlist_main():
    print("Starting YoutubeBlue Playlist Stashing Script...")
    args = youtube_blue.parse_arguements()
    OUTPUT_DIR = args.dest[0]
    PLAYLIST_ID = args.playlist
    REPEAT = 1 if (args.repeat is None) else int(args.repeat)
    youtube_blue.repeat_function(lambda: youtube_blue.download_playlist(PLAYLIST_ID, OUTPUT_DIR), repeat=REPEAT)

if __name__ == "__main__":
    youtube_blue_playlist_main()
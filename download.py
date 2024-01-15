from pytube import YouTube, Playlist
from pytube.cli import on_progress

def list_available_qualities(yt):
    streams = yt.streams.filter(progressive=True, file_extension='mp4')
    qualities = set()
    for stream in streams:
        qualities.add(stream.resolution)
    return sorted(list(qualities))

def display_quality_menu(yt):
    available_qualities = list_available_qualities(yt)
    print("Available qualities:")
    for i, quality in enumerate(available_qualities, 1):
        print(f"{i}. {quality}")
    choice = input("Enter the number of the desired quality: ").strip()
    try:
        choice = int(choice)
        if 1 <= choice <= len(available_qualities):
            return available_qualities[choice - 1]
    except ValueError:
        pass
    return 'best'

def download_video(video_url, quality, download_path='./'):
    try:
        yt = YouTube(video_url, on_progress_callback=on_progress)
        stream = yt.streams.filter(res=quality, file_extension='mp4').first()
        video = yt.streams.first()
        print(f"Downloading video: {yt.title} in {stream.resolution}...")
        stream.download(output_path=download_path)
        print("Download complete!")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def download_playlist(playlist_url, quality,download_path='./'):
    try:
        playlist = Playlist(playlist_url)
        for video_url in playlist.video_urls:
            download_video(video_url, quality, download_path=download_path)
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def playlist_qualities():
    available_qualities = ['360p', '720p']
    print("Enter the quality of the playlist or playlists:")
    for key,value in enumerate(available_qualities):
        print(f"{key + 1}. {value}")
    while True:
        choice = int(input("Your choice is: ").strip()) - 1
        if choice > len(available_qualities) or choice < 0:
            print("Please enter a valid quality")
        else: break
    return available_qualities[choice]

def app():
    choice = input("Do you want to download\n(1) A single video\n(2) Multiple videos\n(3) A playlist\n(4) Multiple playlists\nEnter 1, 2, 3 or 4: ").strip()
    download_path = (input("Enter the download path or paths if more than one video or playlist arranged (default is current directory): ").strip() or './Videos').split(" ")
    
    if choice == '1':
        video_url = input("Enter the URL of the video: ").strip().split(" ")[0]
        quality = display_quality_menu(YouTube(video_url, on_progress_callback=on_progress))
        download_video(video_url, quality, download_path=download_path[0])
    elif choice == '2':
        videos_urls = input("Enter the URLs of the videos separated by spaces: ").strip().split()
        quality = display_quality_menu(YouTube(videos_urls[0], on_progress_callback=on_progress))
        for key,value in enumerate(videos_urls):
            path = path = download_path[0] if key >= len(download_path) else download_path[key]
            print(path)
            download_video(value, quality, path)
    elif choice == '3':
        playlist_url = input("Enter the URL of the playlist: ").strip().split(" ")[0]
        quality = playlist_qualities()
        print(f"Starting the playlist")
        download_playlist(playlist_url, quality,download_path=download_path[0])
        print(f"Finished the playlist")
        print("#" * 20)
        print("#" * 20)
    elif choice == '4':
        playlists_urls = input("Enter the URLS of the playlists separated by spaces: ").strip().split(" ")
        quality = playlist_qualities()
        for key,value in enumerate(playlists_urls):
            path = download_path[0] if key >= len(download_path) else download_path[key]
            print(f"Starting the playlist number: {key + 1}")
            download_playlist(value, quality,path)
            print(f"Finished the playlist number: {key}")
            print("#" * 20)
            print("#" * 20)
    else:
        print("Invalid choice. Please enter 1, 2, 3 or 4.")
        
def main():
    app()
    while True:
        choice = input("You want to download anymore videos? [y/n] ").strip()
        if choice.lower() == 'y':
            app()
        else: break

if __name__ == "__main__":
    main()

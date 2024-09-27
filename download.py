import os
import subprocess
import yt_dlp

def list_available_qualities(ydl, video_url):
    """
        Retrieve available video qualities for a given video URL.
        
        Args:
            ydl: An instance of yt_dlp.YoutubeDL to manage downloads.
            video_url (str): The URL of the video to check.
            
        Returns:
            list: A sorted list of available video heights (qualities).
    """

    with ydl:
        info_dict = ydl.extract_info(video_url, download=False)
        formats = info_dict.get('formats', [])
        qualities = set()
        for fmt in formats:
            if fmt.get('vcodec') != 'none' and fmt.get('ext') == 'mp4':
                qualities.add(fmt.get('height'))
        return sorted(list(qualities))


def display_quality_menu(video_url):
    """
        Display available video quality options for the user to select.
        
        Args:
            video_url (str): The URL of the video.
            
        Returns:
            int: The selected video quality, or 'best' if the input is invalid.
    """

    ydl = yt_dlp.YoutubeDL()
    available_qualities = list_available_qualities(ydl, video_url)
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


def clean_video_url(video_url):
    """
        Remove unnecessary parameters from the video URL.
        
        Args:
            video_url (str): The URL of the video.
            
        Returns:
            str: Cleaned video URL without any unwanted parameters.
    """

    if '&list' in video_url:
        video_url = video_url.split('&list')[0]

    return video_url


def download_video(video_url, quality, download_path='./Videos'):
    """
        Download a single video at the specified quality.
        
        Args:
            video_url (str): The URL of the video to download.
            quality (int): The quality of the video to download.
            download_path (str): The directory where the video will be saved.
    """

    ydl_opts = {
        'format': f'bestvideo[height<={quality}]+bestaudio/best',
        'outtmpl': f'{download_path}/%(title)s.%(ext)s',
    }

    os.makedirs(download_path, exist_ok=True) 
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"Downloading video: {video_url}...")
            ydl.download([video_url])
            print("Download complete!")
    except Exception as e:
        print(f"An error occurred while downloading {video_url}: {str(e)}")


def display_static_quality_menu():
    """
        Display available static video quality options for playlists.
        
        Returns:
            int: The selected quality, defaulting to 1080p if the input is invalid.
    """

    static_qualities = [144, 360, 480, 720, 1080]
    print("Available qualities for playlist download:")
    for i, quality in enumerate(static_qualities, 1):
        print(f"{i}. {quality}p")
    choice = input("Enter the number of the desired quality: ").strip()
    try:
        choice = int(choice)
        if 1 <= choice <= len(static_qualities):
            return static_qualities[choice - 1]
    except ValueError:
        pass
    return 1080


def get_playlist_title(playlist_url):
    """
        Fetch the title of a playlist given its URL.
        
        Args:
            playlist_url (str): The URL of the playlist.
            
        Returns:
            str: The title of the playlist, or "Unknown Playlist" if an error occurs.
    """

    try:
        result = subprocess.run(
            ['yt-dlp', playlist_url, '-I', '1:1', '--skip-download', '--no-warning', '--print', 'playlist_title'],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        return result.stdout.strip()
    except Exception as e:
        print(f"Failed to fetch playlist title: {str(e)}")
        return "Unknown Playlist"


def download_playlist(playlist_url, quality, download_path='./Videos'):
    """
        Download all videos in a playlist at the specified quality.
    
        Args:
            playlist_url (str): The URL of the playlist to download.
            quality (int): The quality of the videos to download.
            download_path (str): The directory where the videos will be saved.
    """

    playlist_title = get_playlist_title(playlist_url)
    
    if not download_path or download_path == './Videos': 
        base_download_path = './Videos'
        playlist_download_path = os.path.join(base_download_path, playlist_title)
    else:
        playlist_download_path = download_path

    os.makedirs(playlist_download_path, exist_ok=True)

    ydl_opts = {
        'format': f'bestvideo[height<={quality}]+bestaudio/best',
        'outtmpl': f'{playlist_download_path}/%(title)s.%(ext)s',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"Downloading playlist: {playlist_title} with quality {quality}p to {playlist_download_path}...")
            ydl.download([playlist_url])
            print(f"Playlist '{playlist_title}' download complete!")
    except yt_dlp.utils.DownloadError as e:
        if 'Private video' in str(e):
            print(f"An error occurred: Some videos in the playlist are private or restricted.")
        else:
            print(f"An error occurred while downloading the playlist: {str(e)}")


def app():
    """
        Main application loop for user interaction to download videos or playlists.
    """

    choice = input("Do you want to download\n(1) A single video\n(2) Multiple videos\n(3) A playlist\n(4) Multiple playlists\nEnter 1, 2, 3 or 4: ").strip()
    download_path = (input("Enter the download path or paths if more than one video or playlist arranged (default is current directory): ").strip() or './Videos')

    if choice == '1':
        video_url = input("Enter the URL of the video: ").strip().split(" ")[0]
        video_url = clean_video_url(video_url)
        quality = display_quality_menu(video_url)
        download_video(video_url, quality, download_path=download_path)
    elif choice == '2':
        videos_urls = input("Enter the URLs of the videos separated by spaces: ").strip().split()
        for key, value in enumerate(videos_urls):
            value = clean_video_url(value)
            quality = display_quality_menu(value)
            path = download_path if key >= len(download_path) else download_path[key]
            download_video(value, quality, path)
    elif choice == '3':
        playlist_url = input("Enter the URL of the playlist: ").strip()
        quality = display_static_quality_menu()  
        download_playlist(playlist_url, quality, download_path)
    elif choice == '4':
        playlists_urls = input("Enter the URLs of the playlists separated by spaces: ").strip().split()
        quality = display_static_quality_menu()
        for playlist_url in playlists_urls:
            download_playlist(playlist_url, quality, download_path)
    else:
        print("Invalid choice. Please enter 1, 2, 3 or 4.")


def main():
    """
        Run the application and prompt the user for additional downloads.
    """

    app()
    while True:
        choice = input("You want to download any more videos? [y/n] ").strip()
        if choice.lower() in ('y', 'yes'):
            app()
        else:
            break


if __name__ == "__main__":
    main()

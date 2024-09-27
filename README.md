# yt-down

This Python script uses `yt-dlp` to download single videos, multiple videos, or playlists from YouTube. It allows users to select the video quality dynamically for individual videos and provides static quality options for playlists (1444, 360p, 480p, 720p, 1080p). The tool also organizes downloaded playlists into directories named after the playlist title.

## Features

- Download **single** or **multiple videos** from YouTube with dynamic quality selection.
- Download **playlists** with qualites (360p, 480p, 720p, 1080p).
- Supports downloading to a specified path or defaults to the `./Videos` directory.

## Requirements

- Python 3.x
- `yt-dlp` library

## Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/MekuXXX/yt-down.git
   cd yt-down
   ```
2. Install yt-dlp by using:

   1. pip

      ```bash
      pip install -r requirements
      ```
   2. pipenv

      ```bash
      pipenv install
      ```

## Usage:

1. **Run the script**:
   Open your terminal or command prompt and execute the following command:

   ```bash
   python download.py
   ```
2. **Choose the type downloading**:

- (1) A single video
- (2) Multiple videos
- (3) A playlist
- (4) Multiple playlists

3. **Enter the path of download**
4. **Enter the URL(s)**
5. **If want to download more choose write [yes / y]**

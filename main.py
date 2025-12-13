import yt_dlp
import os

Video_url = input("Enter youtube link: ")

# Get the current working directory (download location)
download_dir = os.getcwd()
print(f"\nDownload directory: {download_dir}\n")

ydl_opts = {
    'format': 'best[ext=mp4]/best',
}

try:
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([Video_url])
    print(f"\nVideo Download Complete!")
    print(f"File saved in: {download_dir}")
except Exception as e:
    print(f"An error occurred: {e}")

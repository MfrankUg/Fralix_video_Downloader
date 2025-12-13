# Fralix Trailers - Video Downloader Website

A modern, fast, and user-centered video downloader web application that enables users to download videos from YouTube, LinkedIn, X (Twitter), and Instagram with a seamless and intuitive experience.

## Features

- **Multi-Platform Support**: Download videos from YouTube, LinkedIn, X (Twitter), and Instagram
- **Fast Processing**: Lightning-fast downloads with optimized processing
- **Modern UI/UX**: Clean, professional design with smooth animations
- **Responsive Design**: Works perfectly on desktop, tablet, and mobile devices
- **Secure & Private**: No data collection, no tracking, just downloads
- **Format Selection**: Choose your preferred video quality and format

## Installation

1. **Clone the repository** (or navigate to the project directory)

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python app.py
   ```

4. **Open your browser** and navigate to:
   ```
   http://localhost:5000
   ```

## Usage

1. **Paste Link**: Copy and paste the video URL from any supported platform
2. **Select Format**: Choose your preferred video quality and format
3. **Download**: Get your video instantly and enjoy offline access

## Supported Platforms

- ✅ YouTube (videos, playlists, shorts)
- ✅ LinkedIn (professional videos)
- ✅ X (Twitter) (videos and media)
- ✅ Instagram (videos, reels, IGTV)

## Project Structure

```
Youtube_downloader/
├── app.py                 # Flask backend application
├── main.py               # Original CLI script (legacy)
├── requirements.txt      # Python dependencies
├── README.md            # This file
├── templates/
│   └── index.html       # Main HTML template
├── static/
│   ├── css/
│   │   └── style.css    # Stylesheet
│   ├── js/
│   │   └── main.js      # Frontend JavaScript
│   └── images/          # Image assets
└── downloads/           # Downloaded videos (created automatically)
```

## Technical Details

- **Backend**: Flask (Python)
- **Video Processing**: yt-dlp
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Design**: Modern, responsive, with smooth animations

## Disclaimer

Fralix Trailers is for personal use only. Please respect copyright and terms of service of content platforms. Users are responsible for ensuring they have the right to download content.

## License

This project is provided as-is for educational and personal use.

## Support

For issues or questions, please check the code comments or refer to the yt-dlp documentation for video processing details.


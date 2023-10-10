# YouTube Playlist Length Calculator

## Description

This project is a Python script that calculates the total duration of all videos within a specified YouTube playlist. This is especially useful for assessing the total watch time of course material, tutorial series, or any collection of videos grouped into a YouTube playlist.

## Features

- Extracts all video durations from a YouTube playlist.
- Calculates the total length (hours, minutes, and seconds) of all videos combined.
- Utilizes YouTube Data API v3.
- Displays a progress bar during data retrieval and processing.
- Handles API key management (save, update, and use).

## Prerequisites

- Python 3.x
- `requests` library
- `tqdm` library
- A valid YouTube Data API key

To install the necessary libraries, use:
```bash
pip install requests tqdm
```

## Usage

1. **API Key**: Obtain a YouTube Data API key from the [Google Developers Console](https://console.developers.google.com/) and save it in a file named `api_key.txt` within the same directory as the script or provide it when prompted.

2. **Run the Script**: Use the script from the command line as follows:

```bash
python main.py [-u URL] [-c] [-au]
```

### Arguments

- `-u, --url` [**URL**]: YouTube playlist URL. If not provided, you'll be prompted to input it during execution.
- `-c, --cleanup`: Remove the stored API key file.
- `-au, --api_update`: Update the stored API key file.

### Example

```bash
python main.py -u "https://www.youtube.com/playlist?list=PLxyz"
```

## Notes

- Ensure that you've enabled the YouTube Data API v3 on your Google Developers Console and your API key is active and valid for the YouTube Data API.
- API quotas and limitations apply as per your API key settings in the Google Developers Console.
- The script may take a varying amount of time to retrieve data based on the number of videos in the playlist.

## Troubleshooting

- **Invalid URL**: Ensure the playlist URL is valid.
- **API Quota Exceeded**: Ensure you do not exceed your API quota.
- **Connection Issues**: Ensure your internet connection is stable during execution.
- **API Key Issues**: Ensure your API key is valid and active.

## License

This project is open-source and available to everyone. Feel free to use, modify, and distribute as per your needs.

import requests
import re
import argparse
import os
from tqdm import tqdm

BASE_URL = 'https://www.googleapis.com/youtube/v3/'
BATCH_SIZE = 50

def extract_playlist_id(playlist_url) -> str:
    """Extracts playlist ID from playlist url."""
    match = re.search(r'list=([a-zA-Z0-9_-]+)', playlist_url)
    if match is None:
        raise ValueError("Invalid playlist URL")
    return match.group(1)

def get_playlist_info(api_key, playlist_id) -> dict:
    """Get playlist info from YouTube API."""
    page_token = None
    all_items = []
    total_items = None
    pbar = None

    while True:
        url = f'{BASE_URL}playlistItems?part=contentDetails&maxResults={BATCH_SIZE}&playlistId={playlist_id}&key={api_key}'
        
        if page_token:
            url += f'&pageToken={page_token}'
        
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            if total_items is None:
                total_items = data.get('pageInfo', {}).get('totalResults', 0)
                pbar = tqdm(total=total_items, desc='Fetching playlist info', bar_format='{l_bar}{bar} {n_fmt}/{total_fmt}')
            all_items.extend(data["items"])
            pbar.update(len(data["items"]))
            page_token = data.get("nextPageToken")
            if not page_token:
                break
        else:
            response.raise_for_status()
    
    if pbar is not None:
        pbar.close()

    return {"items": all_items}

def extract_video_ids(playlist_info) -> list:
    """Extracts video IDs from playlist information."""
    return [info["contentDetails"]["videoId"] for info in playlist_info["items"]]

def get_videos_info(api_key, video_ids) -> dict:
    """Gets video info from YouTube API."""
    ids = ','.join(video_ids)
    url = f"{BASE_URL}videos?part=contentDetails&id={ids}&key={api_key}"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()

def extract_duration(video_info) -> str:
    """Extracts the video duration from the video information."""
    return video_info["contentDetails"]["duration"]

def format_duration(string_duration) -> tuple:
    """Formats the duration string to hours, minutes, and seconds."""
    match = re.match(r'P((\d+)D)?T((\d+)H)?((\d+)M)?((\d+)S)?', string_duration)

    days = int(match.group(2)) if match.group(2) else 0
    hours = int(match.group(4)) if match.group(4) else 0
    minutes = int(match.group(6)) if match.group(6) else 0
    seconds = int(match.group(8)) if match.group(8) else 0

    total_hours = (days * 24) + hours
    return total_hours, minutes, seconds

def get_total_playlist_length(api_key, playlist_id) -> tuple:
    """Calculate the total playlist length."""
    playlist_info = get_playlist_info(api_key, playlist_id)
    video_ids = extract_video_ids(playlist_info)

    total_hours, total_minutes, total_seconds = 0, 0, 0

    pbar = tqdm(total=len(video_ids), desc='Processing videos     ', bar_format='{l_bar}{bar} {n_fmt}/{total_fmt}')

    for i in range(0, len(video_ids), BATCH_SIZE):
        batch_video_ids = video_ids[i:i+BATCH_SIZE]
        videos_info = get_videos_info(api_key, batch_video_ids)
        for video_info in videos_info["items"]:
            video_duration = extract_duration(video_info)
            video_hours, video_minutes, video_seconds = format_duration(video_duration)
            total_hours += video_hours
            total_minutes += video_minutes
            total_seconds += video_seconds
        
        pbar.update(len(batch_video_ids))

    pbar.close()
    return total_hours, total_minutes, total_seconds

def format_total_time(total_hours, total_minutes, total_seconds) -> tuple:
    """Converts total time to a standardized format of hours (any amount), minutes (<60), and seconds (<60)."""
    total_minutes += total_seconds // 60
    total_seconds = total_seconds % 60
    total_hours += total_minutes // 60
    total_minutes = total_minutes % 60

    return total_hours, total_minutes, total_seconds

def update_api_key(user_api_key):
    """Update or create API key file."""
    with open("api_key.txt", "w") as file:
        file.write(user_api_key)

def read_api_key():
    """Reads API key from user input or file."""
    if os.path.exists("api_key.txt"):
        with open("api_key.txt", "r") as file:
            api_key = file.readline()
            return api_key
    else: 
        api_key = input("API key: ")
        update_api_key(api_key)
        return api_key

    
def main(api_key, playlist_url):
    """Main function to get and print total playlist length."""
    try:
        playlist_id = extract_playlist_id(playlist_url)
        hours, minutes, seconds = get_total_playlist_length(api_key, playlist_id)
        formatted_hours, formatted_minutes, formatted_seconds  = format_total_time(hours, minutes, seconds)
        print(f'Total playlist length: {formatted_hours} hours, {formatted_minutes} minutes, and {formatted_seconds} seconds')
    except requests.exceptions.HTTPError as errh:
        print ("Http Error:",errh)
    except requests.exceptions.ConnectionError as errc:
        print ("Error Connecting:",errc)
    except requests.exceptions.Timeout as errt:
        print ("Timeout Error:",errt)
    except requests.exceptions.RequestException as err:
        print ("Oops: Something Else",err)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Get total length of a YouTube playlist.')
    parser.add_argument("-u","--url", type=str, help="YouTube Playlist URL (string)", default="")
    parser.add_argument("-c","--cleanup", action='store_true', help="Remove API Key File")
    parser.add_argument("-au","--api_update", action='store_true', help="Change The API Key File")

    args = parser.parse_args()

    if args.api_update:
        user_api_key = input("API Key: ")
        update_api_key(user_api_key)

    if args.url:
        api_key = read_api_key()
        main(api_key, args.url)

    if args.cleanup:
        os.remove("api_key.txt")
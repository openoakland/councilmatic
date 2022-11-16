VERSION = "0.1"

import argparse

import json

import requests
import re

def fix_empty_video_links(meeting_file):

    
    print("Opening JSON file")
    f = open(meeting_file,'r+')
    data = json.load(f)

    # fill in video URLs from EventMedia id
    for meeting in data:
        if meeting['EventMedia'] is not None:
            meeting['EventVideoPath'] = 'http://oakland.granicus.com/MediaPlayer.php?view_id=2&clip_id=' + meeting['EventMedia']
        # if Video URL is empty let's try scraping the legistar website for it
        if meeting['EventMedia'] is None and meeting['EventVideoPath'] is None and meeting['EventInSiteURL'] is not None:
            print(meeting['EventInSiteURL'])
            try:
                legistar_site_scrape = requests.get(meeting['EventInSiteURL'], timeout=5)
                videoID = re.search(r'(?<=ID1=)[^&]*',legistar_site_scrape.text)
                if(videoID):
                    meeting['EventVideoPath'] = 'http://oakland.granicus.com/MediaPlayer.php?view_id=2&clip_id=' + videoID[0]
            except requests.exceptions.RequestException:
                print("Error scraping for video URL...")

    f.seek(0)
    print("Rewriting JSON file")
    json.dump(data, f, indent=4)
    print("Closing JSON file")
    f.close()

if __name__ == '__main__':
    print(" ")
    print("<---------Running Software Version:", VERSION, "- scrape_granicus.py ----------->")
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", help="Name of JSON file", type=str)
    args = parser.parse_args()

    fix_empty_video_links(args.file)

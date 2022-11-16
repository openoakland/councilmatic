VERSION = "0.1"

import argparse

import json

import requests
import re

from datetime import datetime, timedelta

def add_cdp_links(meeting_file):

    print("Scraping CDP site")
    try:
        cdp_site_scrape = requests.get("https://councildataproject.org/oakland/#/events/", timesout=5)
    except requests.exceptions.RequestException:
        print("Error")
    
       print("Opening JSON file")
       f = open(meeting_file,'r+')
       data = json.load(f)

       # if Video URL is empty let's try scraping the legistar website for it
       for meeting in data:
        if meeting['EventCDPPath'] is None:
           print(meeting['EventId'])
           event_date = datetime.strptime(meeting['EventDate'], '%Y-%m-%dT%H:%M:%S')
           event_date = event_date.strftime("%B %-d, %Y")
           event_name = meeting['EventBodyName'] # Convert to the right format
           cdp_date = re.search(r''+event_date, cdp_site_scrape.text)
           cdp_name = re.search(r''+event_name, cdp_site_scrape.text)
           if(cdp_date and cdp_name):
               meeting.add()
           else:
               meeting.add();

    f.seek(0)
    print("Rewriting JSON file")
    json.dump(data, f, indent=4)
    print("Closing JSON file")
    f.close()

        
if __name__ == '__main__':
    print(" ")
    print("<---------Running Software Version:", VERSION, "- scrape_cdp.py ----------->")
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", help="Name of JSON file", type=str)
    args = parser.parse_args()

    fix_empty_video_links(args.file)

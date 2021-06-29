# Written by Max Flander
#
# Scrapes data by using the Legistar API and then puts them in a json file
#
# There are two arguments.
# Argument #1 is the number of days to scrape
# Argument #2 is the location of the output file
# Argument #3 is the location of the calendar ICS directory

import requests
import tqdm
import json
import datetime as dt
import argparse
import logging
import os.path #Temp fix near line 75
from os import path #Part of same temp fix

import re

VERSION = "1.4"

API_URL = 'http://webapi.legistar.com/v1/oakland/'
logging.basicConfig(level=logging.INFO)


def scrape_api(days, year, meeting_file, calendar_dir):
    if days:
        today = dt.date.today()
        date_cutoff = (today - dt.timedelta(days=days)).strftime('%Y-%m-%d')
    else:
        date_cutoff = '{}-01-01'.format(year)

    print("date_cuttoff:", date_cutoff)
    logging.info(f"Querying Events API with Date Cutoff: {date_cutoff}")
    meetings = requests.get(
        API_URL + 'Events?$filter=EventDate+ge+datetime%27{}%27'.format(date_cutoff)
        ).json()

    if year:
        meetings = [m for m in meetings if int(m['EventDate'][:4]) == year]

    today = dt.datetime.now()
    midnight = dt.datetime.combine(today, dt.datetime.min.time())

    logging.info("Retrieving meeting details from EventItems API...")
    for meeting in tqdm.tqdm(meetings):
        # For some reason the time is 0:00 in meeting['EventDate'] and is instead present in meeting['EventTime'] in %I:%M %p format instead of iso format. For efficiency's sake, we convert it to ISO format and put it into meeting['EventDate']. This simplifies Jinja2 date and time parsing later
        meeting_date = dt.datetime.fromisoformat(meeting['EventDate'])
        meeting_time = dt.datetime.strptime(meeting['EventTime'], '%I:%M %p')
        meeting_date = meeting_date.replace(hour=meeting_time.hour, minute=meeting_time.minute)
        meeting['EventDate'] = meeting_date.isoformat()
        try:
            agenda = requests.get(API_URL + 'Events/{}/EventItems?AgendaNote=1&MinutesNote=1&Attachments=1'.format(meeting['EventId'])).json()
            meeting['EventAgenda'] = agenda
            # Sometimes the EventVideoLink ID is null, so we just take the ID of the first EventItemVideo
            # WARNING: there is a bug with the granicus video player, where if you access via https,
            # the agenda doesn't show up, so we need to use the http URL
            ##for item in agenda:
            ##    if item['EventItemVideo'] is not None:
            ##        meeting['EventVideoPath'] = 'http://oakland.granicus.com/MediaPlayer.php?view_id=2&meta_id=' + str(item['EventItemVideo'])
            ##        break

            # search for zoom links and make calendar ICS files for future meetings
            meeting_date = dt.datetime.strptime(meeting['EventDate'], '%Y-%m-%dT%H:%M:%S')
            daydiff = (meeting_date - midnight).days
            if daydiff >= 0: # only set 'EventVideoPath' to a zoom URL and make ICS file if this is a future meeting
                for item in agenda:
                    if item['EventItemTitle'] is not None and "zoom" in item['EventItemTitle']:
                        zoomLink = re.search('https://us02web.zoom.us/j/[0-9]*',str(item['EventItemTitle']))
                        if(zoomLink):
                            meeting['EventVideoPath'] = zoomLink[0]

                filename = str(calendar_dir) + str(meeting['EventId']) + ".ics"
                if path.exists(filename): #Temp work around for error of file not found
                    f = open(filename, 'w')
                    f.write("BEGIN:VCALENDAR\nVERSION:2.0\nCALSCALE:GREGORIAN\nBEGIN:VEVENT\nDTSTART;TZID=America/Los_Angeles:" + meeting_date.strftime("%Y%m%d") + "T" + str(dt.datetime.strptime(str(meeting['EventTime']), "%I:%M %p").strftime("%H%M%S")) + "\nDTEND;TZID=America/Los_Angeles:" + meeting_date.strftime("%Y%m%d") + "T" + str(int(dt.datetime.strptime(str(meeting['EventTime']), "%I:%M %p").strftime("%H%M%S"))+10000) + "\nSUMMARY:" + str(meeting['EventBodyName']) + "\nURL:" + str(meeting['EventInSiteURL']) + "\nDESCRIPTION:For details link here:" + str(meeting['EventInSiteURL']) + "\nLOCATION:" + str(meeting['EventLocation']) + "\nEND:VEVENT\nEND:VCALENDAR\n")
                    f.close()
                else:
                    print("The following file was not found near line 78 of run_meeting_json.py:",filename)
                    
        except requests.exceptions.RequestException:
            logging.warning("Error retrieving agenda...")

   # meeting_file = 'meetings.json'
    logging.info(f"Saving results to {meeting_file}")
    with open(meeting_file, 'w') as f:
        json.dump(meetings, f, indent=4)


if __name__ == '__main__':
    print(" ")
    print("<---------Running Software Version:", VERSION, "- run_meeting_json.py ----------->")
    parser = argparse.ArgumentParser()
    parser.add_argument("--days", help="Number of previous days to retrieve meeting details for", type=int)
    parser.add_argument("--year", help="Year to retrieve events for (overrides days)", type=int)
    parser.add_argument("--output", help="Name of output file", type=str)
    parser.add_argument("--calendars", help="Location to put generated ICS calendar files", type=str)
    args = parser.parse_args()
    print("Year:",args.year)
    print("Days:",args.days)
    if args.days is None and args.year is None:
        print('Must provide either days or year param')
        exit(1)
    if args.output is None:
        print('Must provide output argument')
        exit(1)
    if args.calendars is None:
        print('Must provide calendars directory argument')
        exit(1)

    scrape_api(args.days, args.year, args.output, args.calendars)

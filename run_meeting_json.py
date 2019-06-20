# Written by Max Flander
# Scrapes data by using Legistar API and then puts them in a json file
#
# There are two arguments.
# Argument #1 is the number of days to scrape
# Argument #2 is the location of the output file

import requests
import tqdm
import json
import datetime as dt
import argparse
import logging

VERSION = "1.0"

API_URL = 'http://webapi.legistar.com/v1/oakland/'
logging.basicConfig(level=logging.INFO)


def scrape_api(days, year, meeting_file):
    if days:
        today = dt.date.today()
        date_cutoff = (today - dt.timedelta(days=days)).strftime('%Y-%m-%d')
    else:
        date_cutoff = '{}-01-01'.format(year)

    logging.info(f"Querying Events API with Date Cutoff: {date_cutoff}")
    meetings = requests.get(
        API_URL + 'Events?$filter=EventDate+ge+datetime%27{}%27'.format(date_cutoff)
        ).json()

    if year:
        meetings = [m for m in meetings if int(m['EventDate'][:4]) == year]

    logging.info("Retrieving meeting details from EventItems API...")
    for meeting in tqdm.tqdm(meetings):
        try:
            agenda = requests.get(API_URL + 'Events/{}/EventItems?AgendaNote=1&MinutesNote=1&Attachments=1'.format(meeting['EventId'])).json()
            meeting['EventAgenda'] = agenda
        except requests.exceptions.RequestException:
            logging.warning("Error retriving agenda...")

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
    args = parser.parse_args()
    if args.days is None and args.year is None:
        print('Must provide either days or year param')
        exit(1)
    if args.output is None:
        print('Must provide output argument')
        exit(1)

    scrape_api(args.days, args.year, args.output)

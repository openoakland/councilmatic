import requests
import tqdm
import json
import datetime as dt
import argparse
import logging

API_URL = 'http://webapi.legistar.com/v1/oakland/'
logging.basicConfig(level=logging.INFO)


def scrape_api(days):
    today = dt.date.today()
    date_cutoff = (today - dt.timedelta(days=days)).strftime('%Y-%m-%d')
    logging.info(f"Date Cutoff: {date_cutoff}")
    meetings = requests.get(
        API_URL + 'Events?$filter=EventDate+ge+datetime%27{}%27'.format(date_cutoff)
        ).json()
    logging.info("Retrieving meeting details from API...")
    for meeting in tqdm.tqdm(meetings):
        try:
            agenda = requests.get(API_URL + 'Events/{}/EventItems?AgendaNote=1&MinutesNote=1&Attachments=1'.format(meeting['EventId'])).json()
            meeting['EventAgenda'] = agenda
        except requests.exceptions.RequestException:
            logging.warning("Error retriving agenda...")

    meeting_file = 'meetings.json'
    logging.info(f"Saving results to {meeting_file}")
    with open('meetings.json', 'w') as f:
        json.dump(meetings, f, indent=4)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("days", 
            help="Number of previous days to retrieve meeting details for", type=int)
    args = parser.parse_args()
    scrape_api(args.days)

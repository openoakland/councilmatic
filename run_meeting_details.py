import argparse
import sys, traceback

from scraper.controller.meeting_details import MeetingDetails
from scraper.model.meeting_details import MeetingDetails as MeetingDetailsModel

def get_args():
    parser = argparse.ArgumentParser()

    #default_url = "https://oakland.legistar.com/MeetingDetail.aspx?ID=672632&GUID=8E103490-AFEF-46D5-AAAC-68207C9C9397&Options=info&Search="
    #default_url = "https://oakland.legistar.com/MeetingDetail.aspx?ID=678861&GUID=FC80363C-34A9-4AFC-A99D-539632DE452E&Options=info&Search="
    #default_url = "https://oakland.legistar.com/MeetingDetail.aspx?ID=676089&GUID=4E273FCF-A9CC-45CE-9B20-F208CFB9D0BB&Options=info&Search="
    default_url = "https://oakland.legistar.com/MeetingDetail.aspx?ID=672829&GUID=0465062F-3439-44B1-A4D6-0FFE65CDF997&Options=&Search="
    parser.add_argument("-u", "--url", help="url", type=str, default=default_url)

    return parser.parse_args()

def scrape(args):
    try:
        md = MeetingDetails(args.url)
        md.run()
        md.close()
    except Exception as ex:
        traceback.print_exception(type(ex), ex, ex.__traceback__)

def main():
    args = get_args()

    scrape(args)

if __name__ == "__main__":
    main()

        
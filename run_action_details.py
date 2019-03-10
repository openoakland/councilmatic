import argparse

from scraper.controller.action_details import ActionDetails
from scraper.model.action_details import ActionDetails as ActionDetailsModel

def get_args():
    parser = argparse.ArgumentParser()

    default_url = "https://oakland.legistar.com/HistoryDetail.aspx?ID=14244515&amp;GUID=5C424C63-D8FE-4A1B-8DE3-D111FC715FF5"
    parser.add_argument("-u", "--url", help="url", type=str, default=default_url)

    return parser.parse_args()

def scrape(args):
    ad = ActionDetails(args.url)
    ad.run()
    ad.close()

def main():
    args = get_args()

    scrape(args)

if __name__ == "__main__":
    main()

        
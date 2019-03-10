import argparse

from scraper.controller.legislation_details import LegislationDetails
from scraper.model.legislation_details import LegislationDetails as LegislationDetailsModel

def get_args():
    parser = argparse.ArgumentParser()

    default_url = "https://oakland.legistar.com/LegislationDetail.aspx?ID=3838892&GUID=19B756FA-6C05-4778-AF2A-8DF76CD3E7E7&Options=&Search="
    parser.add_argument("-u", "--url", help="url", type=str, default=default_url)

    return parser.parse_args()

def scrape(args):
    ld = LegislationDetails(args.url)
    ld.run()
    ld.close()

def main():
    args = get_args()

    scrape(args)

if __name__ == "__main__":
    main()

        
import json
from scraper.model.calendar import Calendar as CalendarModel
#from scraper.model.meeting_item import MeetingItem as MeetingItemModel
#import traceback


def load_json(file_name):
    with open(file_name, 'r') as myfile:
        json_data=myfile.read()

    return json.loads(json_data)


def main():
    json_list = load_json('WebPage/website/scraped/year2019.json')

    cal_list = CalendarModel.from_list_json(json_list, warn_on_err=False)
    print("cal_list - len: %d" % len(cal_list))
    for i, cal in enumerate(cal_list):
        print("%d: %s" % (i, cal))
        
    """

    json_obj = load_json('meeting_item.json')
    meeting_item = MeetingItemModel.from_json(json_obj, warn_on_err=False)
    print(meeting_item)
    """

if __name__ == "__main__":
    main()
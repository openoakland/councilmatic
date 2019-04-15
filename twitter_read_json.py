# twitter_read_json.py - Get the necessary objects from json file
#
# Written by Howard Matis on April 15, 2019
# from code written by Phillip Chen

import json
from scraper.model.calendar import Calendar as CalendarModel


def load_json(file_name):
    with open(file_name, 'r') as myfile:
        json_data=myfile.read()

    return json.loads(json_data)


def twitter_read_json(printit):     # printit tell whether to print out information
    json_list = load_json('WebPage/website/scraped/Twitter.json')
    scraped=[]
    cal_list = CalendarModel.from_list_json(json_list, warn_on_err=False)
    print("cal_list - len: %d" % len(cal_list))
    for i, cal in enumerate(cal_list):
            if printit:
                print(" ")
                #print(cal_list[i])
                if i == 0:
                    print("%d: %s" % (i, cal))
                print(" ")
                print("OBJECTS", i)

            scraped.append([])
            if printit:
                print(cal.name)
                print(cal.meeting_date)
                print(cal.meeting_time)
                print(cal.agenda)
            scraped[i].append(cal.name)                 # Item 0 - name
            scraped[i].append(cal.meeting_date)         # Item 1 - date
            scraped[i].append(cal.meeting_time)         # Item 2 - time
            scraped[i].append(cal.agenda)               # Item 3 - agenda link or "none"

    return scraped

#   Post a message to twitter

import os
import sys
import twitter
import datetime
import calendar

import csv
from datetime import datetime, timedelta
import datetime as dt

VERSION = "1,0"
LOOKAHEAD = 21  # Number of the days to look ahead for meetings
MAKEATWEET = True

'''
This runs off a a file  ".tweeter"  which resides in your home directory.  The format is below

    consumer_key: "consumer_key"
    consumer_secret: "consumer_password"
    access_key: "access_key"
    access_secret: "access_password"
    
Make sure this file does not have world access and is not accessible to the public    
'''


def read_csv_file(datafile, elements):
    data = list(csv.reader(open(datafile, encoding="utf-8"), delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL,
                           skipinitialspace=True))
    numrows = len(data)
    today = dt.datetime.now()
    midnight = datetime.combine(today, datetime.min.time())
    out_index_start = len(elements)

    for i in range(numrows):  # Find out which meetings have not occurred
        if i > 0:  # Don't read headers
            if len(data[i][:]) >= 8:
                meeting_daytime = datetime.strptime(data[i][1], '%m/%d/%Y')  # Convert to daytime format to compare
                daydiff = (meeting_daytime - midnight).days
                if daydiff < 0:
                    break
                elements.append([])
                for j in range(0, 10):    # date within range
                    elements[out_index_start + i - 1].append(0)
                    elements[out_index_start + i - 1][j] = data[i][j]
    return elements


def read_dot_tweeter():  # Read the .tweeter file in the home directory to get the keys to the twitter account
    path = os.path.expanduser('~') + "/.tweeter"
    file = open(path, "r")
    key = []
    for i in range(0, 4):
        line = file.readline().split()
        key.append(line[1])
    return key


def tweet_meeting(key, message, doatweet):    # Tweet to the world
    encoding = None
    key = read_dot_tweeter()  # Fetch the code values from  ~.tweeter
    consumer_key = key[0]
    consumer_secret = key[1]
    access_key =  key[2]
    access_secret = key[3]

    if not consumer_key or not consumer_secret or not access_key or not access_secret:
        print("To Tweet, you need four environmental variables")
        sys.exit(2)
    api = twitter.Api(consumer_key=consumer_key, consumer_secret=consumer_secret,
                      access_token_key=access_key, access_token_secret=access_secret,
                      input_encoding=encoding)
    if doatweet:
        did_tweet = False
        try:
            status = api.PostUpdate(message)
        except UnicodeDecodeError:
            print("Your message could not be encoded.  Perhaps it contains non-ASCII characters? ")
            print("Try explicitly specifying the encoding with the --encoding flag")
            did_tweet = True

        if did_tweet:
           print("{0} just posted: {1}".format(status.user.name, status.text))
    else:
        print("Simulation of Tweeting")
        print(message)


print(" ")
print("<---------Running Software Version:", VERSION, "- Tweeter.py ----------->")

tempfile = "tempfile.html"
f1 = open(tempfile, 'w+')


key = read_dot_tweeter()   # Read the permissions for sending the Tweet
currentDay = datetime.now().day
currentMonth = datetime.now().month
currentYear = datetime.now().year
formatedDay = datetime.now().strftime("%A, %B %d, %Y at %I:%M %p")
print(formatedDay)
theDate = '<font size="-1">Updated: ' + str(formatedDay) + '<br> </font></p>'

# Check if close to a new year

if currentMonth == 12:  # See if need to look at next year's record
    if currentDay > 31 - LOOKAHEAD:
        years = [str(currentYear + 1), str(currentYear)]  # Allows reading later file first
    else:
        years = [str(currentYear)]
else:
    years = [str(currentYear)]

print("Gathering meetings from ", years)
schedule = []
for year in years:
    scraper_file = "../website/scraped/year" + str(year) + ".csv"
    print("Scraping", scraper_file)
    schedule = read_csv_file(scraper_file, schedule)

print()
numrows = len(schedule)
today = datetime.now()
lastdate = today - timedelta(days=1)
tomorrow = today + timedelta(days=1)
today_day = str(today.month) + '/' + str(today.day) + '/' + str(today.year)
tomorrow_day = str(tomorrow.month) + '/' + str(tomorrow.day) + '/' + str(tomorrow.year)

for i in range(numrows - 1, -1, -1):
    event_day = schedule[i][1]
    if lastdate != event_day:
        lastdate = event_day
        new_day = True
    else:
        new_day = False

    if new_day:
        day_datetime = datetime.strptime(event_day, '%m/%d/%Y')
        day_label = datetime.date(day_datetime).weekday()
        day_of_week = calendar.day_name[day_label]
        if event_day == today_day:
            day_of_week = "Today"
        elif event_day == tomorrow_day:
            day_of_week = "Tomorrow"
        print()
        print("New Day", event_day)


    committee = schedule[i][0]
    if "City Council" in committee:
        committee = "City Council - (" + committee + ")"
    #print("Meeting description")
    #print(committee)  # Committee
    #print(schedule[i][2])  # Calendar
    #print(schedule[i][3])  # Time
    #print(schedule[i][4])  # Room
    agenda = schedule[i][6]
    #ecomment = schedule[i][9]
    theTweet = "City of Oakland Meeting for " + committee + " on " + event_day + " at " + schedule[i][3] + \
               ': <a href="' + agenda + '">' + "AGENDA</a>"
    f1.write(theTweet+ "\n")
    print(theTweet)
    # MAKEATWEET = False
    tweet_meeting(key, theTweet, MAKEATWEET)


print("<----------------End of process - Tweeter.py----------------->")
print(" ")
quit()

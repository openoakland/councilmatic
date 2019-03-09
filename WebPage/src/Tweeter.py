
#   Post a message to twitter

import os
import sys
import twitter
import datetime
import calendar

import string
import random

import csv
from datetime import datetime, timedelta
import datetime as dt


VERSION = "1,0"
LOOKAHEAD = 7  # Number of the days to look ahead for meetings. Program witten for a week.
MAKEATWEET = True
MAXTWEETSIZE = 280      # Maximums size for a tweet#
TWEETURLSIZE = 23       # Size of a URL

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


def tweet_meeting(key, message, doatweet, the_image):    # Tweet to the world
    # Docs https://python-twitter.readthedocs.io/en/latest/twitter.html?highlight=postupdate
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
    status = ''
    if doatweet:
        did_tweet = False
        try:
            the_image = "http://councilmatic.aws.openoakland.org/images/tweets/image1.png"
            status = api.PostUpdate(message, verify_status_length=False, media=the_image)
        except UnicodeDecodeError:
            print("Your message could not be encoded.  Perhaps it contains non-ASCII characters? ")
            print("Try explicitly specifying the encoding with the --encoding flag")
        else:
            did_tweet = True

        if did_tweet:
           print("{0} just posted: {1}".format(status.user.name, status.text))
    else:
        print("Simulation of Tweeting")
        print(message)


def random_string(length):      # Return a random string
    return ''.join(random.choice(string.ascii_letters) for m in range(length))


print(" ")
print("<---------Running Software Version:", VERSION, "- Tweeter.py ----------->")


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
    print("Meeting Date:", event_day)
    day_datetime = datetime.strptime(event_day, '%m/%d/%Y')
    days = int((day_datetime - today).days)  # of days awas from today
    if days >= 0 and days < LOOKAHEAD:
        day_label = datetime.date(day_datetime).weekday()
        day_of_week = calendar.day_name[day_label]
        if event_day == today_day:
            day_of_week = "Today"
        elif event_day == tomorrow_day:
            day_of_week = "Tomorrow"

        committee = schedule[i][0]
        if "City Council" in committee:
            committee = "City Council - (" + committee + ")"
        agenda = schedule[i][6]
        theTweet1 = day_of_week + " at " + schedule[i][3]+ " Oakland " + committee
        if "CANCELLED" in theTweet1:   # Don't put the agenda if cancelled
            theTweetend = " Meeting, "+ random_string(2)
        else:
            theTweetend = " Meeting. Agenda is " + agenda + " " + random_string(2)
        theTweet = theTweet1 + theTweetend
        maximumCouncilTweet = MAXTWEETSIZE - min(TWEETURLSIZE - len(agenda), TWEETURLSIZE)  # Twitter has a fixed URL Size
        extra_chars = len(theTweet) - maximumCouncilTweet
        if extra_chars > 0:  # Trim the Tweet to the maximum size
            theTweet = theTweet1[:-extra_chars] + theTweetend
        print("The Tweet:", len(theTweet), theTweet)

        MAKEATWEET = False
        tweet_meeting(key, theTweet, MAKEATWEET, "temp")
        print()

print("<----------------End of process - Tweeter.py----------------->")
print(" ")
quit()

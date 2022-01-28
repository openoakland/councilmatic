#!/usr/bin/env bash

# The "new" version was created for parallel Tweeting while switching to a new Twitter 
# handle.  Also using this opportunity to clean up the code in this file.
#
# Scrape the Oakland Counmcil Legistar webpage and then Tweet upcoming meetings
# Written by Howard Matis - April 14, 2019

# Version 2.2 refelects moving code to different directory

VERSION="2.3"
source `dirname "$0"`/councilmatic.conf
echo "Scraper_Twitter.sh is NOT Running under Darwin, assuming Ubuntu/AWS"


DIR=`dirname "$0"` #/usr/local/councilmatic for production
export PATH=$PATH:`dirname "$0"`

#
cd $DIR
pwd
if [ -e  geckodriver.log ]
then
    rm geckodriver.log   #This file gets big quickly
    echo "Removed gecko log file!"
else
    echo "nok"
fi

# This works on both platforms

CURRENTYEAR=`date +"%Y"`
CURRENTMONTH=`date +"%m"`
CURRENTDAY=`date +"%d"`
FIRSTDAY=$CURRENTMONTH"/"$CURRENTDAY"/"$CURRENTYEAR   # uncomment for debug
echo "The starting day is "$FIRSTDAY

# Here is the DATE-RELATED year-gathering code.

echo "On Ubuntu"
    date --date="10 day" +"%Y" > year.tmp
    date --date="10 day" +"%m" > month.tmp
    date --date="10 day" +"%d" > day.tmp
    LASTYEAR=$(<year.tmp)
    LASTMONTH=$(<month.tmp)
    LASTDAY=$(<day.tmp)
    rm year.tmp month.tmp day.tmp

FINALDAY=$LASTMONTH"/"$LASTDAY"/"$LASTYEAR   # uncomment for debug
echo "The final day is "$FINALDAY

echo "[Diag] The Python path is: $PYTHON"
export MOZ_HEADLESS=1 #Needed to run Firefox Headless

echo "Version "$VERSION" of Scraoer_Twitter.sh" 			#Clear cron log file

#
#Preparing to run the scraper
#
## source set_json_scraper_symlink.sh # Set environment for json
date
echo "Doing the JSON Scrape"
COMMAND="src-Scraper/run_meeting_json.py --days 7 --output WebPage/website/scraped/TwitterTEMP.json --calendars WebPage/website/calendars/"
echo "Starting the Scrape with the command:" $COMMAND
$PYTHON $COMMAND
retVal=$?
if [ $retVal -ne 0 ]; then
    echo "Scraper error. Will ignore"
else
    mv  WebPage/website/scraped/TwitterTEMP.json  WebPage/website/scraped/Twitter.json
    echo "Successful scraper file"
fi
date
if [[ $WEBSITEPATH == *"dev"* ]]; then
    # if 'dev' version then don't actually tweet
    $PYTHON src-Tweeter/Tweeter-new.py FALSE
else
    # otherwise, go ahead and tweet
    $PYTHON src-Tweeter/Tweeter-new.py TRUE
fi
echo "Scraper_Twitter.sh completed"
#

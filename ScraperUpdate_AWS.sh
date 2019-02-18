#!/usr/bin/env bash
#
# Update CSV Database - To be run be a cron job daily
#
# Written by Howard Matis - October 30, 2018
#
# This script only works on Ubuntu Linux
# The command "date" is different depending on flavor of UNIX
# In December the script will run the script for next year;  In January the script will run the previous year.
#
# This run using cron
# m h  dom mon dow   command
#2 0 * * * /home/howard/Councilmatic/ScraperUpdate_AWS.sh > /home/howard/Councilmatic/WebPage/website/logs/scraperdailyupdate.log 2>&1
#04 18 * * * /home/howard/Councilmatic/ScraperUpdate_AWS.sh > /home/howard/Councilmatic/WebPage/website/logs/scraperdailyupdate.log 2>&1
#53 20 * * * /home/howard/Councilmatic/ScraperUpdate_AWS.sh > /home/howard/Councilmatic/WebPage/website/logs/scraperdailyupdate.log 2>&1
#
# ------------------------------------------------------------------
#
#   This is machine dependant
#
DIR=/home/howard/Councilmatic
CRONDIR=/home/howard/Councilmatic/WebPage/website/logs
export PATH=$PATH:/home/howard/Councilmatic
#
#
cd $DIR
pwd
date --date="1 year ago" +"%Y" > last.tmp
LASTYEAR=$(<last.tmp)
CURRENTYEAR=`date +"%Y"`
date --date="1 year" +"%Y" > next.tmp
NEXTYEAR=$(<next.tmp)
rm last.tmp
rm next.tmp
CURRENTMONTH=`date +"%m"`
PYTHON=/home/howard/miniconda3/bin/python  #Must specify correct version of Python
echo $PYTHON
export MOZ_HEADLESS=1 #Needed to run Firefox Headless
#
# for GECKO
#PATH="/Users/matis/.drivers:${PATH}"   #This is system dependent
#export PATH
#
#Get a list of current dates
#

VERSION="3.5"
echo "Version "$VERSION" of ScraperUpdate_AWS.sh" 			#Clear cron log file
date

$PYTHON run_calendar.py --show_dates > $CRONDIR/temp.tmp
#
# Scrape the current year if it exists
#
if `grep -q "$CURRENTYEAR" "$CRONDIR/temp.tmp"`; then
    echo "Processing current year scraper file"
   $PYTHON  run_calendar.py -d "$CURRENTYEAR"  > WebPage/website/scraped/year"$CURRENTYEAR".csv
fi
#
# Check if December
#
if [ "$CURRENTMONTH" == "12" ];then
        echo "This month is December"
    if `grep -q "$NEXTYEAR" "$CRONDIR/temp.tmp"`; then
        echo "Processing next year"
        $PYTHON  run_calendar.py -d "$NEXTYEAR"  > WebPage/website/scraped/year"$NEXTYEAR".csv
    else
        echo "Next year file not ready"
    fi
elif [ "$CURRENTMONTH" == "1" ];then
    if `grep -q "$LASTYEAR" "$CRONDIR/temp.tmp"`; then
        echo "Current month is January - Processing last year"
        $PYTHON  run_calendar.py -d "$LASTYEAR"  > WebPage/website/scraped/year"$LASTYEAR".csv
    else
        echo "Previous year not available"
    fi
else
    echo "No need to process any adjacent year"
fi
#
# Now make the webpage
#
pwd
cd WebPage/src
echo " "
echo "Running Web Programs"
$PYTHON  main.py  #Run the main program
echo " "
cd $DIR #Go back to councilmatis directory
# Add an index.html file for easier entry into the site
cp WebPage/website/$CURRENTYEAR/city-council.html WebPage/website/$CURRENTYEAR/index.html
#
# Copy files to actual website
#
echo "Copying files to actual website"
sudo cp -R /home/howard/Councilmatic/WebPage/website/* /var/www/councilmatic/
#
date
echo "ScraperUpdate_AWS.sh completed"
#

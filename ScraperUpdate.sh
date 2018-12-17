#!/usr/bin/env bash
#
# Update CSV Database - To be run be a cron job daily
#
# Written by Howard Matis - October 30, 2018
#
# This script only works on Mac OSX (BSD)
# The command "date" is different depending on flavor of UNIX
# In December the script will run the script for next year;  In January the script will run the previous year.
#
# This run using cron
#   0 2 * * * /Users/matis/Documents/OpenOakland/Councilmatic-master/Councilmatic/ScraperUpdate.sh
#
# ------------------------------------------------------------------
#
#   This is machine dependant
#
DIR=/Users/matis/Documents/OpenOakland/Councilmatic-master/Councilmatic
CRONDIR=/Users/matis/Documents/OpenOakland/Councilmatic-master/Councilmatic/WebPage/website/logs
#
#
cd $DIR
LASTYEAR=`date -v-1y  +"%Y"`
CURRENTYEAR=`date +"%Y"`
NEXTYEAR=`date -v+1y  +"%Y"`
CURRENTMONTH=`date +"%m"`
PYTHON=/Users/matis/anaconda3/bin/python     #Must specify correct version of Python
VERSION="3.3"
export MOZ_HEADLESS=1 #Needed to run Firefox Headless
#
# for GECKO
PATH="/Users/matis/.drivers:${PATH}"   #This is system dependent
export PATH
#
#Get a list of current dates
#
echo "Version "$VERSION" of ScraperUpdate.sh" 			#Clear cron log file
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
cd Webpage
cd src
echo " "
echo "Running Web Programs"
$PYTHON  sidebar.py  #Get the sidebar
$PYTHON  main.py  #Run the main program
echo " "
date
echo "ScraperUpdate.sh completed"
#

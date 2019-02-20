#!/usr/bin/env bash
#
# Update CSV Database - To be run be a cron job daily
#
# Written by Howard Matis - October 30, 2018

# ScraperUpdate2.sh - Rudy Trubitt Feb 2018, merged ScraperUpdate.sh and ScraperUpdateAWS.sh,
# adds tests for Darwin so script works on both MacOSX/Darwin and AWS/Ubuntu. See variable LINUXTYPE

# In December the script will run the script for next year.
# In January the script will run the previous year.
#
# This run using cron under OSX
#   0 2 * * * /Users/matis/Documents/OpenOakland/Councilmatic-master/Councilmatic/ScraperUpdate.sh
#   ...
# This run using cron under UBUNTU
# m h  dom mon dow   command
#2 0 * * * /home/howard/Councilmatic/ScraperUpdate_AWS.sh > /home/howard/Councilmatic/WebPage/website/logs/scraperdailyupdate.log 2>&1
#04 18 * * * /home/howard/Councilmatic/ScraperUpdate_AWS.sh > /home/howard/Councilmatic/WebPage/website/logs/scraperdailyupdate.log 2>&1
#53 20 * * * /home/howard/Councilmatic/ScraperUpdate_AWS.sh > /home/howard/Councilmatic/WebPage/website/logs/scraperdailyupdate.log 2>&1


# To determine the current host (Mac/Darwin vs. AWS/Ubuntu): 
# Assign ISDARWIN to string 'Darwin'.
# Run the system command $(uname -s) and assign the result to LINUXTYPE. 
# Finally, compare $LINUXTYPE to $ISDARWIN.
# if equal, we are running local Mac OSX/Darwin, else assume Ubuntu/AWS

ISDARWIN='Darwin' 
LINUXTYPE=$(uname -s) # If equals ISDARWIN then we are running under OSX on a local development Mac
if [ $LINUXTYPE = $ISDARWIN ]; then
	echo "ScraperUpdate2.sh is Running under Mac OSX/Darwin"
else
	echo "ScraperUpdate2.sh is NOT Running under Darwin, assuming Ubuntu/AWS"
fi


if [ $LINUXTYPE = $ISDARWIN ]; then
	DIR=/Users/matis/Documents/OpenOakland/Councilmatic-master/Councilmatic
	CRONDIR=/Users/matis/Documents/OpenOakland/Councilmatic-master/Councilmatic/WebPage/website/logs
else
	DIR=/home/howard/Councilmatic
	CRONDIR=/home/howard/Councilmatic/WebPage/website/logs
	export PATH=$PATH:/home/howard/Councilmatic
fi

#
cd $DIR
pwd

# Here is the DATE-RELATED year-gathering code, deal with differences in Darwin vs. Ubuntu date command.

if [ $LINUXTYPE = $ISDARWIN ]; then
	LASTYEAR=`date -v-1y  +"%Y"`
	NEXTYEAR=`date -v+1y  +"%Y"`
else
	date --date="1 year ago" +"%Y" > last.tmp
	LASTYEAR=$(<last.tmp)
	date --date="1 year" +"%Y" > next.tmp
	NEXTYEAR=$(<next.tmp)
	rm last.tmp
	rm next.tmp
fi
CURRENTYEAR=`date +"%Y"`
CURRENTMONTH=`date +"%m"`

# echo $LASTYEAR $CURRENTYEAR $NEXTYEAR $CURRENTMONTH #uncomment for debug 

if [ $LINUXTYPE = $ISDARWIN ]; then
	PYTHON=/Users/matis/anaconda3/bin/python     #Must specify correct version of Python
else
	PYTHON=/home/howard/miniconda3/bin/python  #Must specify correct version of Python
fi

echo $PYTHON
export MOZ_HEADLESS=1 #Needed to run Firefox Headless

# for GECKO
if [ $LINUXTYPE = $ISDARWIN ]; then
	PATH="/Users/matis/.drivers:${PATH}"   #PATH set and export ONLY necessary when ISDARWIN
	export PATH
fi

# VERSION was set differently for OSX vs. Ubuntu, but I think this is just the version 
# of this shell script
# Last ScraperUpdate.sh OSX was #VERSION="3.3"
# Last ScraperUpdateAWS.sh Ubuntu was VERSION="3.5"
VERSION="3.6" # for ScraperUpdate2.sh

echo "Version "$VERSION" of ScraperUpdate2.sh" 			#Clear cron log file

#
#Get a list of current dates
#
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
$PYTHON  sidebar.py  #Get the sidebar
$PYTHON  main.py  #Run the main program
echo " "

if [ $LINUXTYPE = $ISDARWIN ]; then
	echo 'skipping CopyFiles step because LINUXTYPE = ISDARWIN'
else
	cd $DIR #Go back to councilmatis directory
	# Copy files to actual website
	echo "Copying files to actual website"
	sudo cp -R /home/howard/Councilmatic/WebPage/website/* /var/www/councilmatic/
fi


date
echo "ScraperUpdate2.sh completed"
#

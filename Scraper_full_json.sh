#!/usr/bin/env bash
#
# Update JSON Database - To be run to establish a baseline of files
#
# Written by Howard Matis - April 2, 2019

# To determine the current host (Mac/Darwin vs. AWS/Ubuntu): 
# Assign ISDARWIN to string 'Darwin'.
# Run the system command $(uname -s) and assign the result to LINUXTYPE. 
# Finally, compare $LINUXTYPE to $ISDARWIN.
# if equal, we are running local Mac OSX/Darwin, else assume Ubuntu/AWS


VERSION="1.2.1"
ISDARWIN='Darwin'
LINUXTYPE=$(uname -s) # If equals ISDARWIN then we are running under OSX on a local development Mac
if [ $LINUXTYPE = $ISDARWIN ]; then
	echo "Scraper_full_jason.sh is Running under Mac OSX/Darwin"
else
	echo "Scraper_full_jason.sh is NOT Running under Darwin, assuming Ubuntu/AWS"
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


if [ -e  geckodriver.log ]
then
    rm geckodriver.log   #This file gets big quickly
    echo "Removed gecko log file!"
else
    echo "nok"
fi


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


echo "Version "$VERSION" of Scraoer_full_jason.sh" 			#Clear cron log file

#
#Get a list of current dates
#
source set_json_scraper_symlink.sh
ls -a scraper    # Just to check if it is working
CHOICE="json"
echo "Creating a "$CHOICE" file"
date
#
YEAR="2014"
echo "JSON Scrape of ""$YEAR"
$PYTHON  run_calendar.py -d "$YEAR"  > WebPage/website/scraped/temp"$YEAR"."$CHOICE"
retVal=$?
if [ $retVal -ne 0 ]; then
    echo "Scraper error for ""YEAR"". Will ignore"
else
    mv WebPage/website/scraped/temp"$YEAR"."$CHOICE" WebPage/website/scraped/year"$YEAR"."$CHOICE"
    echo "Successful scrape of YEAR ""$YEAR"
fi
date
echo "Scraper_full_json.sh completed"
#
YEAR="2015"
echo "JSON Scrape of ""$YEAR"
$PYTHON  run_calendar.py -d "$YEAR"  > WebPage/website/scraped/temp"$YEAR"."$CHOICE"
retVal=$?
if [ $retVal -ne 0 ]; then
    echo "Scraper error for ""YEAR"". Will ignore"
else
    mv WebPage/website/scraped/temp"$YEAR"."$CHOICE" WebPage/website/scraped/year"$YEAR"."$CHOICE"
    echo "Successful scrape of YEAR ""$YEAR"
fi
date
echo "Scraper_full_json.sh completed"
#
YEAR="2016"
echo "JSON Scrape of ""$YEAR"
$PYTHON  run_calendar.py -d "$YEAR"  > WebPage/website/scraped/temp"$YEAR"."$CHOICE"
retVal=$?
if [ $retVal -ne 0 ]; then
    echo "Scraper error for ""YEAR"". Will ignore"
else
    mv WebPage/website/scraped/temp"$YEAR"."$CHOICE" WebPage/website/scraped/year"$YEAR"."$CHOICE"
    echo "Successful scrape of YEAR ""$YEAR"
fi
date
echo "Scraper_full_json.sh completed"
#
YEAR="2017"
echo "JSON Scrape of ""$YEAR"
$PYTHON  run_calendar.py -d "$YEAR"  > WebPage/website/scraped/temp"$YEAR"."$CHOICE"
retVal=$?
if [ $retVal -ne 0 ]; then
    echo "Scraper error for ""YEAR"". Will ignore"
else
    mv WebPage/website/scraped/temp"$YEAR"."$CHOICE" WebPage/website/scraped/year"$YEAR"."$CHOICE"
    echo "Successful scrape of YEAR ""$YEAR"
fi
date
echo "Scraper_full_json.sh completed"
#
#
YEAR="2018"  System information as of Sat Apr 20 16:09:26 PDT 2019
echo "JSON Scrape of ""$YEAR"
$PYTHON  run_calendar.py -d "$YEAR"  > WebPage/website/scraped/temp"$YEAR"."$CHOICE"
retVal=$?
if [ $retVal -ne 0 ]; then
    echo "Scraper error for ""YEAR"". Will ignore"
else
    mv WebPage/website/scraped/temp"$YEAR"."$CHOICE" WebPage/website/scraped/year"$YEAR"."$CHOICE"
    echo "Successful scrape of YEAR ""$YEAR"
fi
date
echo "Scraper_full_json.sh completed"
#
YEAR="2019"
echo "JSON Scrape of ""$YEAR"
$PYTHON  run_calendar.py -d "$YEAR"  > WebPage/website/scraped/temp"$YEAR"."$CHOICE"
retVal=$?
if [ $retVal -ne 0 ]; then
    echo "Scraper error for ""YEAR"". Will ignore"
else
    mv WebPage/website/scraped/temp"$YEAR"."$CHOICE" WebPage/website/scraped/year"$YEAR"."$CHOICE"
    echo "Successful scrape of YEAR ""$YEAR"
fi
date
echo "Scraper_full_json.sh completed"

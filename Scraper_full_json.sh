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


VERSION="1.0"
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
unlink scraper
ROOT="scraper_"
CHOICE="json"
SCRAPER_DIRECTORY=$ROOT$CHOICE
echo "Creating a "$CHOICE" file"
ln -s $SCRAPER_DIRECTORY scraper
date
echo "JSON Scrape of 2018"
$PYTHON  run_calendar.py -d 2018  > WebPage/website/scraped/year2018."$CHOICE"
date
echo "JSON Scrape of 2017"
$PYTHON  run_calendar.py -d 2017  > WebPage/website/scraped/year2017."$CHOICE"
date
echo "JSON Scrape of 2016"
$PYTHON  run_calendar.py -d 2016  > WebPage/website/scraped/year2016."$CHOICE"
date
echo "JSON Scrape of 2015"
$PYTHON  run_calendar.py -d 2015  > WebPage/website/scraped/year2015."$CHOICE"
date
echo "JSON Scrape of 2014"
$PYTHON  run_calendar.py -d 2014  > WebPage/website/scraped/year2014."$CHOICE"
date
echo "JSON Scrape of 2019"
$PYTHON  run_calendar.py -d 2019  > WebPage/website/scraped/year2019."$CHOICE"
date
echo "Scraper_full_json.sh completed"
#
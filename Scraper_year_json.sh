#!/usr/bin/env bash
#
# Scrape a year and produce json file.  The year is indicated by the argument of this script
#
# Written by Howard Matis - April 21, 2019

echo " "
echo "Beginning scrape of "$1
date
if [ -e  geckodriver.log ]
then
    rm geckodriver.log   #This file gets big quickly
fi

ISDARWIN='Darwin'
LINUXTYPE=$(uname -s) # If equals ISDARWIN then we are running under OSX on a local development Mac
if [ $LINUXTYPE = $ISDARWIN ]; then
	PYTHON=/Users/matis/anaconda3/bin/python   # Must specify correct version of Python
else
	PYTHON=/home/howard/miniconda3/bin/python  # Must specify correct version of Python
fi

echo $PYTHON
export MOZ_HEADLESS=1 # Needed to run Firefox Headless

# for GECKO
if [ $LINUXTYPE = $ISDARWIN ]; then
	PATH="/Users/matis/.drivers:${PATH}"   # PATH set and export ONLY necessary when ISDARWIN
	export PATH
fi
source set_json_scraper_symlink.sh
# ls -a scraper    # Just to check if it is working
$PYTHON  run_calendar.py -d "$1"  > WebPage/website/scraped/temp"$1".json
retVal=$?
if [ $retVal -ne 0 ]; then
    echo "Scraper error for "$1". Will ignore"
else
    mv WebPage/website/scraped/temp"$1".json WebPage/website/scraped/year"$1".json
    echo "Successful scrape of "$1
fi
date

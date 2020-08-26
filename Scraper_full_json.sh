#!/usr/bin/env bash
#
# Update JSON Database - To be run to establish a baseline of files
#
# Written by Howard Matis - April 2, 2019

# Now using API scraper
# This does a full update from 2014 to the current year

VERSION="3.1"
ISDARWIN='Darwin'
LINUXTYPE=$(uname -s) # If equals ISDARWIN then we are running under OSX on a local development Mac

if [ $LINUXTYPE = $ISDARWIN ]; then
	echo "Running under Mac OSX/Darwin"
	DIR=/Users/matis/Documents/OpenOakland/Councilmatic-master/Councilmatic
else
	echo "NOT Running under Darwin, assuming Ubuntu/AWS"
	DIR=/home/howard/Councilmatic
fi

if [ $LINUXTYPE = $ISDARWIN ]; then
	PYTHON=/Users/matis/anaconda3/bin/python   #Must specify correct version of Python
else
	# PYTHON=/home/howard/miniconda3/bin/python  #Must specify correct version of Python
    PYTHON=C:/Users/Peter/Documents/Projects/councilmatic/councilmatic_venv/Scripts/python.exe
    DIR=C:/Users/Peter/Documents/Projects/councilmatic
fi

echo $PYTHON


echo "Beginning full json scrape. Version "$VERSION
cd $DIR
pwd

CURRENTYEAR=`date +"%Y"`

for ((YEAR=2014; YEAR<=CURRENTYEAR; YEAR++)); do      # Start the loop from 2014
        echo "Doing the JSON Scrape for YEAR $YEAR"
        COMMAND="src-Scraper/run_meeting_json.py --year $YEAR --output WebPage/website/scraped/ScraperTEMP.json"
        echo "Starting the Scrape with the command:" $COMMAND
        $PYTHON $COMMAND
        retVal=$?
        if [ $retVal -ne 0 ]; then
            echo "Scraper error. Will ignore"
        else
            mv  WebPage/website/scraped/ScraperTEMP.json  WebPage/website/scraped/Scraper$YEAR.json
            echo "Successful scraper file for year $YEAR"
        fi
        echo ""
done

echo "Scraper_full_json.sh completed"
#



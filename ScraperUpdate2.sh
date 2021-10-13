#!/usr/bin/env bash
#
# Update JSON Database and then create a webpage
#
# Written by Howard Matis - October 30, 2018

# ScraperUpdate2.sh - Rudy Trubitt Feb 2018, merged ScraperUpdate.sh and ScraperUpdateAWS.sh,
# adds tests for Darwin so script works on both MacOSX/Darwin and AWS/Ubuntu. See variable LINUXTYPE

# In December the script will run the script for next year.
# In January the script will run the previous year.
#
# To determine the current host (Mac/Darwin vs. AWS/Ubuntu): 
# Assign ISDARWIN to string 'Darwin'.
# Run the system command $(uname -s) and assign 0the result to LINUXTYPE.
# Finally, compare $LINUXTYPE to $ISDARWIN.
# if equal, we are running local Mac OSX/Darwin, else assume Ubuntu/AWS


# VERSION was set differently for OSX vs. Ubuntu, but I think this is just the version
# of this shell script

# Last ScraperUpdate.sh OSX was #VERSION="3.3"
# Last ScraperUpdateAWS.sh Ubuntu was VERSION="3.5"
# Version 3.8 introduces images for tweets
# Version 3.9 allows for csv or jason.  Does not produce a file if a crash
# Version 3.10 uses run_calendar2.py
# Version 4.0 switching to JSON scraper.  4.0 does csv and json scrape.  Analysis program uses CSV file
# Version 4.6 stops csv scraper
# Version 4.9 - Removing old csv stuff
# Version 5.0 - Moving code to individual directories
# Version 5.1 - Howard moved files on his home computer - need to deal with spaces
# Version 5.2 - Fixing scraper.  It will now work for all years

cd "$(dirname "$0")" # sets the current working directory to the directory of the script.
VERSION="5.2" # for ScraperUpdate2.sh
CHOICE="csv"
source `dirname "$0"`/councilmatic.conf
ISDARWIN='Darwin'

if [ "$LINUXTYPE" == "$ISDARWIN" ]; then
	echo "ScraperUpdate2.sh is Running under Mac OSX/Darwin"
else
	echo "ScraperUpdate2.sh is NOT Running under Darwin, assuming Ubuntu/AWS"
fi

if [ "$LINUXTYPE" == "$ISDARWIN" ]; then
	DIR=/Users/matis/Library/Mobile\ Documents/com\~apple\~CloudDocs/Home\ Files/Councilmatic
    CRONDIR=/Users/matis/Library/Mobile\ Documents/com\~apple\~CloudDocs/Home\ Files/Councilmatic/WebPage/website/logs
else
	DIR=`dirname "$0"` #$PWD #/usr/local/councilmatic/dev/councilmatic #/home/howard/Councilmatic
    #CRONDIR=/home/howard/Councilmatic/WebPage/website/logs
	export PATH=$PATH:`dirname "$0"` #/usr/local/councilmatic/dev/councilmatic #/home/howard/Councilmatic
fi

#
cd "$DIR"
pwd
rm -rf geckodriver.log || true  #This file gets big quickly

# Here is the DATE-RELATED year-gathering code, deal with differences in Darwin vs. Ubuntu date command.

if [ "$LINUXTYPE" == "$ISDARWIN" ]; then
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

# prevfilename="WebPage/website/scraped/Scraper{}-holdprevious.json".format$(CURRENTYEAR)
# dwnldfilename="WebPage/website/scraped/Scraper{}.json".format$(CURRENTYEAR)
prevfilename="WebPage/website/scraped/Scraper-holdprevious.json"
printf -v currentdwnldfilename "WebPage/website/scraped/Scraper%s.json" "$CURRENTYEAR"

# ##### Rename the last download file to a generic "prev" name. (Scraper-holdprevious.json)
mv $currentdwnldfilename $prevfilename

# echo $LASTYEAR $CURRENTYEAR $NEXTYEAR $CURRENTMONTH #uncomment for debug 

export MOZ_HEADLESS=1 #Needed to run Firefox Headless

# for GECKO
if [ "$LINUXTYPE" == "$ISDARWIN" ]; then
	PATH="/Users/matis/.drivers:${PATH}"   #PATH set and export ONLY necessary when ISDARWIN
	export PATH
fi

echo "Version "$VERSION" of ScraperUpdate2.sh" 			#Clear cron log file

#
#Get a list of current dates
#
date
#
# Scrape the current year if it exists
#
echo "Doing the JSON Scrape for YEAR $CURRENTYEAR"
COMMAND="src-Scraper/run_meeting_json.py --year $CURRENTYEAR --output WebPage/website/scraped/ScraperTEMP.json --calendars WebPage/website/calendars/"
echo "Starting the JSON Scrape with the command:" $COMMAND
$PYTHON $COMMAND
retVal=$?
  if [ $retVal -ne 0 ]; then
      echo "JSON Scraper error. Will ignore"
  else
      mv  WebPage/website/scraped/ScraperTEMP.json  $currentdwnldfilename
      echo "JSON Successful scraper file for year $CURRENTYEAR"
  fi
  echo ""

echo "Workaround: Scraping Granicus to fix empty Video links in $currentdwnldfilename"
COMMAND="src-Scraper/scrape_granicus.py --file $currentdwnldfilename"
echo "Starting the JSON Scrape with the command:" $COMMAND
$PYTHON $COMMAND
retVal=$?
  if [ $retVal -ne 0 ]; then
      echo "Granicus error. Will ignore"
  else
      echo "Granicus successfully scraped."
  fi
  echo ""


# Code from diffbatch.sh but using Bash cmp for an initial check for changes.
# USE PARAMS for the years in the two file names below.

# Compare files to see if copy should be saved
if cmp -s "$prevfilename" "$currentdwnldfilename" ; then
    echo "Nothing changed between last and newly downloaded JSON data file."
    echo ''
    rm -f $prevfilename
else
    echo "Something changed between last and newly downloaded JSON data file. Labeling and saving the previous file."
    echo ''
#   ##### Change the generic "previous" name to a dated file to hold for testing and verification.
    mv $prevfilename "${prevfilename%.*}_$(date -d@$(stat --printf='%Y' "$prevfilename") +%Y%m%d%H%M%S).${prevfilename##*.}"
fi

#
# Check if December
#
if [ "$CURRENTMONTH" == "12" ];then
    echo "This month is December"     #This code has not been tested for December

    #echo "Processing next year"
    #$PYTHON  run_calendar2.py -d "$NEXTYEAR"  > WebPage/website/scraped/temp2."$CHOICE"
    #retVal=$?
    #if [ $retVal -ne 0 ]; then
    #    echo "CSV Scraper error. Will ignore"
    #else
    #    mv WebPage/website/scraped/temp2."$CHOICE" WebPage/website/scraped/year"$NEXTYEAR"."$CHOICE"
    #    echo "CSV Successful scraper file"
    #fi
    #

    echo "Doing the JSON Scrape for YEAR $NEXTYEAR"
    COMMAND="src-Scraper/run_meeting_json.py --year $NEXTYEAR --output WebPage/website/scraped/ScraperTEMP.json --calendars WebPage/website/calendars/"
    echo "Starting the JSON Scrape with the command:" $COMMAND
    $PYTHON $COMMAND
    retVal=$?
    if [ $retVal -ne 0 ]; then
        echo "JSON Scraper error. Will ignore"
    else
        mv  WebPage/website/scraped/ScraperTEMP.json  WebPage/website/scraped/Scraper$NEXTYEAR.json
        echo "JSON Successful scraper file for year $NEXTYEAR"
    fi
    echo ""

elif [ "$CURRENTMONTH" == "1" ];then

    echo "Doing the JSON Scrape for YEAR $LASTYEAR"
    COMMAND="src-Scraper/run_meeting_json.py --year $LASTYEAR --output WebPage/website/scraped/ScraperTEMP.json --calendars WebPage/website/calendars/"
    echo "Starting the JSON Scrape with the command:" $COMMAND
    $PYTHON $COMMAND
    retVal=$?
        if [ $retVal -ne 0 ]; then
            echo "JSON Scraper error. Will ignore"
        else
            mv  WebPage/website/scraped/ScraperTEMP.json  WebPage/website/scraped/Scraper$LASTYEAR.json
            echo "JSON Successful scraper file for year $LASTYEAR"
        fi
    echo ""

else
    echo "No need to process any adjacent year"
fi

#
# Now make the webpage
#
pwd
echo " "
echo "Running Web Programs"

$PYTHON  src-Webpage/main.py  #Run the main program
echo " "

#cd Webpage/website    #Go back to Webpage

#cp upcoming/all-meetings.html index.html  # make a default page

#if id -nG | grep -qw "dev"; then
#    chgrp dev WebPage/website/scraped/*
#fi
if [ ! -z "$WEBSITEPATH" ]; then  #if [ $HOSTNAME = 'ip-172-31-38-33' ]; then
	cd "$DIR" #Go back to councilmatic directory
	# Copy files to actual dev website
	echo "Copying files to actual dev website"
	rm -f $WEBSITEPATH/calendars/* # remove old calendar files from website directory
	cp -R --preserve=ownership ./WebPage/website/* $WEBSITEPATH #/var/www/councilmatic/dev
	rm -f ./WebPage/website/images/tweets/*   #remove files from local tweet directory
	rm -f ./WebPage/website/calendars/*       #remove calendar files from calendar directory
	
#	sh -c 'ls --format single-column /var/www/councilmatic/dev/images/tweets/ > /var/www/councilmatic/dev/images/tweets/filelist.txt' 
        sh -c "ls --format single-column $WEBSITEPATH/images/tweets/ > $WEBSITEPATH/images/tweets/filelist.txt"
else
	echo 'Skipping CopyFiles step because not on AWS instance'
fi

date
echo "ScraperUpdate2.sh completed"
#

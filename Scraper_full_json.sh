#!/usr/bin/env bash
#
# Update JSON Database - To be run to establish a baseline of files
#
# Written by Howard Matis - April 2, 2019

VERSION="2.3.1"
ISDARWIN='Darwin'
LINUXTYPE=$(uname -s) # If equals ISDARWIN then we are running under OSX on a local development Mac

if [ $LINUXTYPE = $ISDARWIN ]; then
	echo "Running under Mac OSX/Darwin"
	DIR=/Users/matis/Documents/OpenOakland/Councilmatic-master/Councilmatic
else
	echo "NOT Running under Darwin, assuming Ubuntu/AWS"
	DIR=/home/howard/Councilmatic
fi

echo "Beginning full json scrape. Version "$VERSION
cd $DIR
pwd
./Scraper_year_json.sh 2014
./Scraper_year_json.sh 2015
./Scraper_year_json.sh 2016
./Scraper_year_json.sh 2017
./Scraper_year_json.sh 2018
./Scraper_year_json.sh 2019
echo "Scraper_full_json.sh completed"
#



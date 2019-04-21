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


VERSION="2.1"
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
set $DIR
./Scraper_year_json.sh 2014
./Scraper_year_json.sh 2015
./Scraper_year_json.sh 2016
./Scraper_year_json.sh 2017
./Scraper_year_json.sh 2018
./Scraper_year_json.sh 2019
echo "Scraper_full_json.sh completed"
#



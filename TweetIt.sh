#!/usr/bin/env bash
#
# Tweet upcoming meetings - assumes scraper output
#
# Written by Howard Matis - March 12, 2019

#   ...
# This run using cron under UBUNTU
# m h  dom mon dow   command
#0  * * * /home/howard/Councilmatic/TweetIt.sh > /home/howard/Councilmatic/WebPage/website/logs/TweetIt.log 2>&1
# for test 30 20 * * * /home/howard/Councilmatic/TweetIt.sh > /home/howard/Councilmatic/WebPage/website/logs/TweetIt.log 2>&1

VERSION="1.1" # for ScraperUpdate2.sh

echo "Version "$VERSION" of TweetIt.sh" 			#Clear cron log file

ISDARWIN='Darwin'
LINUXTYPE=$(uname -s) # If equals ISDARWIN then we are running under OSX on a local development Mac
if [ $LINUXTYPE = $ISDARWIN ]; then
	echo "Tweetit.sh is Running under Mac OSX/Darwin"
else
	echo "Tweetit.sh is NOT Running under Darwin, assuming Ubuntu/AWS"
fi

if [ $LINUXTYPE = $ISDARWIN ]; then
	PYTHON=/Users/matis/anaconda3/bin/python     #Must specify correct version of Python
else
	PYTHON=/home/howard/miniconda3/bin/python  #Must specify correct version of Python
fi

echo $PYTHON

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
#
# Now make the webpage
#
pwd
cd WebPage/src
echo " "
echo "Tweeting"
$PYTHON  Tweeter.py  #Get the sidebar
echo " "
date
echo "Tweetit completed"
#

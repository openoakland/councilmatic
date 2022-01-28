# Councilmatic

## Active Notices

The Councilmatic repository is currently being overhauled. Cloned installations currently seem to be throwing an error that we are tracing.  If there are any questions regarding the code base while these issues are being resolved please contact us at councilmatic@openoakland.org.

## The Production Site

Website –> https://OaklandCouncil.net
Twitter handle for notices of upcoming meetings -> @OCouncilmatic

## Affiliations
**Councilmatic** is a project of OpenOakland which is a brigade of Code for America. Project leads for this project can be contacted at councilmatic@openoakland.org

## Platform Requirements

Councilmatic runs using Linux shell scripts to execute python scripts which collect and organize the data before usng Jinja2 templates to format the resulting HTML pages. The minimum version of Python is 3.7.

The Python module tqdm should be installed to produce progress bars at stages in the processing. This module, however, is not required  to run this code.

## Notes for cloning

The repository contains a file councilmatic.conf.model. This file should be copied to councilmatic.conf then edited for the current operating environment.

When a site is newly cloned there will be empty placeholder files for the data downloaded from the Oakland Legistar API site.  Before running the script that performs routine updates (ScraperUpdate2.sh) for the 1st time, the script Scraper_full_json.sh should be run to load these placeholder files.

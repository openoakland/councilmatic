# Councilmatic

## The Production Site

Website –> https://OaklandCouncil.net
Twitter handle for notices of upcoming meetings -> @OaklandCityCncl

## Affiliations
**Councilmatic** is a project of OpenOakland which is a brigade of Code for America. Project leads for this project can be contacted at councilmatic@openoakland.org

## Platform Requirements

Councilmatic runs using Linux shell scripts to execute python scripts which collect and organize the data before usng Jinja2 templates to format the resulting HTML pages. The minimum version of Python is 3.7.

The Python module tqdm should be installed to produce progress bars at stages in the processing. This module, however, is not required  to run this code.

## Notes for cloning

The repository contains a file councilmatic.conf.model. This file should be copied to councilmatic.conf then edited for the current operating environment.  Documentation is found within the .conf file.

When a site is newly cloned the script Scraper_full_json.sh must be run first to download all required historical data.  The newly created site can then be regularly updated by running ScraperUpdate2.sh at intervals.  The Councilmatic production site update schedule is midnight, 6am, and 6pm.

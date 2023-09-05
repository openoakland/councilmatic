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

# Sept 5, 2023 Councilmatic Presentation
## About Councilmatic
### History of Councilmatic (CM)
* Earliest data files contain 2014 meeting information.
* As the story goes...this project started as a fork/clone of a project running in New York. ChatGPT currently states that Councilmatic was started by the civic tech organization DataMade and was first developed for the City of Chicago. Anyone into software archaeology?
* Very early on the OpenOakland version was rebuilt almost entirely to use Bash and Python.
* The earliest OpenOakland version would initially scrape data from the Oakland City website but [most] data later became more easyly accessible via an API and Councilmatic was modified accordingly.
* The official Oakland City meetings calendar can be viewed at https://oakland.legistar.com/calendar.aspx

### Mission & Vision
To foster openness of policy making in Oakland Government. This is to be accomplished by improving the accessibility of City Council meeting information and by promoting interest in City Council activities.

### Core Functionality
Reformat & publish public information on Oakland City Council and the seven subcommittees of:
* Finance & Management
* Public Safety
* Life Enrichment
* Public Works
* Community & Economic Development
* Oakland Redevelopment
* Rules And Legislation

### Current construction
* Linux shell scripts and Python
* HTML is assembled with the Jinja2 templating language.
* Data is obtained mostly via API of Legistar with the exception of some video * links.
* Legistar is the software used by the City of Oakland (and SF and SJ) for council administration.
* Data files correspond to calendar years. The current file is updated through the year and a new file is created at the start of each new year.
### Current Front-end
* Opening page is the schedule from today forward.
Options to view all meeting of the current year or any previous years.
* Individual meeting types (City Council or one of 7 subcommittees) can be selected.

### Recent Developments
1. New user interface 3 years ago.
2. Clean up code and file organization.
3. Organization of permissions.
4. Capture and processing of links to meeting videos.
5. Building into GitHub's Actions and Pages for a no-charge site.
  * The prototype production pages are generating to https://oaklandcitycouncil.org
  * GitHub repository is currently at https://github.com/rightonyourtail/oaklandcouncil/ though this is likely change before we're done.

### Ideas for expansion
* Make the meeting history more easily accessible with search or ???
* Gamification - can we add a feature to create interest in the "sausage making"?
* Create interface to link in other meetings i.e. Bicyclist and Pedestrian Advisory Commission (BPAC) or the 40+ similar boards and commissions. (see https://www.oaklandca.gov/boards-commissions/)
* Determine whether we can inks to another opensource site that has been able to generate transcripts from the videos. (See https://github.com/CouncilDataProject)
* There is another local developer who has build an engine to acquire and structure meeting minutes for Oakland City Council - and Berkeley and Alameda. (See Phillip James description of his work at https://phildini.dev/digitizing-55-000-pages-of-civic-meetings or his Oakland City Council data set at https://data.oakland.works/oakland_minutes/pages)
* We need to assess the value of the Twitter (X) link such as Threads or Mastodon social networking service.

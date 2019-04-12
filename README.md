# Councilmatic

# Setup

1. Install Anaconda 
  * https://www.anaconda.com/download
2. Create conda env
  * conda env create -f environment.yml
3. Download geckodriver and add to path. Make sure to install Firefox if you don't have it as well.
  * https://github.com/mozilla/geckodriver/releases
  <br>
note: We used Katalon IDE brower plugin to easy generate some of python selenium statements the normal selenium IDE no longer supports Python code exports.
  
# start up conda env
```
source activate new_councilmatic
```

# update conda env
```
source activate new_councilmatic
conda env update -f=environment.yml
```

# install conda env into jupyter notebook
```
source activate new_councilmatic
python -m ipykernel install --user --name new_councilmatic --display-name "new councilmatic"
```

# To run:

## To scrape and generate website:
```
make scrape generate
```

## Calendar Scraper

### Help

```
python run_calendar.py -h
```

### Scrape a single year

```
python run_calendar.py -d 2018 > WebPage/website/scraped/year2018.json
```

### Scrape a single year and filter by date range

```
python run_calendar.py -d 2019 -sdt 1/1/2019 -edt 1/14/2019 > WebPage/website/scraped/cal01012019_01142019.json
```

### By Search Words Example (2018)

```
python run_calendar.py -s "parking"
```

### By Year and Search Words Example (2018)

```
python run_calendar.py -d 2018 -s "parking"
```

### Save as CSV Example (deprecated)

```
python run_calendar.py -d 2018 -s "parking" > parking2018.csv
```

### To create the web page

```
Run ScraperUpdate_AWS.sh on Amazon Server
```


# To run in jupyter notebook
```
jupyter notebook calendar.ipynb
```
# Web location of production site

1. PC access
  http://councilmatic.aws.openoakland.org/pc/
2. Mobile access
http://councilmatic.aws.openoakland.org/mobile/

# Milestones:
1. to have a web scraping library.
  * scraping from https://oakland.legistar.com/Calendar.aspx.
  * need to scrape data from the city council table, city council events(aka city meetings, the calendar page) table and the legislation page.
  * scrapers inherit from the scraper class and use selenium to naviagate to the pages, which might require javascript and access web content inside tables on the page.
  * store in models(that are decoupled from DB).
  
 next milestones...
 might want to have some kind of user interface.(note: almost done with the first milestone)


# Councilmatic

# Setup
# 
# IF pip (My prefered method):
  1. Download Python
  2. make sure you're in the project directory
     and download the packages like so:
  ```
  pip install -r requirements.txt
  ```

  Disregard below
# IF Conda:

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

https://oaklandcouncil.net



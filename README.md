# Councilmatic
## Changes in process
### 2021-02-23
#### Renaming the "develop" branch

The branch **develop** has been renamed to **main**.  Therefore the following three lines need to be run on your local **develop** repository to resync with GitHub.

```
$ sudo git branch -m develop main
$ sudo git fetch origin
$ git branch -u origin/main main
```

*(note: the "sudo" command is for Ubuntu distros)*

A bit of background: at some point in history the default branch was changed from **master** to **develop**.  At that time all testing of code changes was done on a PC (on a MAC which explains the reference to "Darwin" in the code).

A branch name of **main** is the new GitHub standard for default branches.  Using **main** for CM meant that we didn't need to figure out what to do with the old **master** branch.

The next step is to clone **main** to a new **develop** branch within GitHub.  A **develop**ment area will be set up on the CM server with code cloned from the new GitHub **develop** branch (which should set up the local **develop** branch to track the GitHub **develop** branch as origin.

These mods will then allow the testing of changes from pull requests on the server before pulling into production code of the new **main** branches.

#### Set up of development folders for code testing on the CM server

* Created directories /usr/local/councilmatic and /usr/local/councilmatic/dev for the constructor files (Bash and Python) from /home/howard/Councilmatic. The new dev/ folder will be loaded by cloning from a new **develop** repository. The dev/ directory is owned by root:dev.
* Web files from /var/www/councilmatic were copied into /var/www/councilmatic/dev.
* Changed the group of 
* Todo: After cloning constructor code into /usr/local/councilmatic/dev then check for paths tha determine where the generated pages are placed.  The dev/ constructor code will need to generate pages to /var/www/councilmatic/dev. This path may need to be carried by a configuration variable.

------
###### Everything below will be deleted soon
------

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



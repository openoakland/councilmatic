# commoncode.sh

# Check whether files exist to received data for the 2014 thru the current yeear.  This check is performed
# because a new clone will throw an error if these files are missing.  Because these files are updated
# when ScraperUpdae2.sh or Scraper_full_json.sh are run we don't want to create a slow download by
# carrying these files loaded with data when the site is cloned.

function check_for_json_data_files()
{
    echo 'Checking for the existence of data files (whether empty or loaded)...'

    created_a_file=0
    curryear=`date +'%Y'`

    for i in $(seq 2014 $curryear); do
        targetfile="WebPage/website/scraped/Scraper$i.json"

        if [[ ! -f "$targetfile" ]]; then
            echo "The file $targetfile does not exist and will be created."
            touch "$targetfile"
            created_a_file=1
        fi
    done

    if [ $created_a_file -eq 0 ]
        then
        echo "All files present.  Nothing created."
    fi
}

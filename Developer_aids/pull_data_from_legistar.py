# The output of this Python script is a pretty print of the JSON formatted meeting file (file of 
# Oakland City Council meetings).  The code pieces were copied from the src-Scraper/run_meeting_json.py file.
#
# An output file is generated.  Set the name accordingly below or comment out the "print to file" section.
import requests
import json
import datetime as dt
 
API_URL = 'http://webapi.legistar.com/v1/oakland/'
 
days=30
 
today = dt.date.today()
date_cutoff = (today - dt.timedelta(days=days)).strftime('%Y-%m-%d')
 
meetings = requests.get(
        API_URL + 'Events?$filter=EventDate+ge+datetime%27{}%27'.format(date_cutoff)
        ).json()
 
print(json.dumps(meetings, indent=4, sort_keys=True))
 
# If you want to print to a file:
fh = open( "legistar_api_json_output.txt",'w' )
print(json.dumps(meetings, indent=4, sort_keys=True),file=fh)
fh.close()

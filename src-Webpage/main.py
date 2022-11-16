# Creates a webpage for Councilmatic
# Uses Jinja2 to produce the HTML
#
#
import os
import json
import re
from pprint import pprint
import itertools
from jinja2 import Environment, FileSystemLoader, select_autoescape
from datetime import datetime, timedelta

from emoji import twitter_read_json

VERSION = "8.21"    # Version of Program
MAXYEARS = 10       # Maximum number of years to output
FIRSTYEAR = 2014    # First year to start
COMMITTEES = ["All Meetings", "City Council", "Rules & Legislation", "Public Works", "Life Enrichment", "Public Safety",
              "Oakland Redevelopment", "Community & Economic Development", "Finance & Management"]
CURRENT_DIRECTORY = os.path.abspath(os.path.dirname(__file__))
CURRENT_YEAR = datetime.now().year
PATH_FROM_ROOT = os.environ["WEBSITEPATHRELATIVETOROOT"]


def councilmatic_date(mydate):  # function used in Jinja2
    #  The input of the routine is a date in datetime format that you want to display
    #  The output is the text that we want to display
    today = datetime.now()
    tomorrow = today + timedelta(days=1)
    weekdiff = int(mydate.strftime('%U')) - int(today.strftime('%U'))

    if weekdiff < 0: # Check for last week
        timestamp = mydate.strftime('%A')
    elif weekdiff == 0: # Check for dates for this week
        if today.strftime('%A') == mydate.strftime('%A'):
            timestamp = "Today"
        elif tomorrow.strftime('%A') == mydate.strftime('%A'):
            if tomorrow.strftime('%d') == mydate.strftime('%d'): # Overlapping a week
                timestamp = "Tomorrow"
            else:
                timestamp = mydate.strftime('%A')
        else:
            timestamp = mydate.strftime('%A')
    elif weekdiff == 1: # Check for next week
        if tomorrow.strftime('%d') == mydate.strftime('%d'): # Overlapping a week
            timestamp = "Tomorrow"
        else:
            timestamp = mydate.strftime('%A') + " - Next Week"
    else:
        timestamp = mydate.strftime('%A') + " - in " + str(weekdiff) + " Weeks"

    return timestamp


def format_date(date):  # Function used in Jinja2
    """
    format a date object in month/day/year format, but convert dates like:
        01/02/2013
    to:
        1/2/2013
    """
    return re.sub("\\b0(\\d)", "\\1", date.strftime("%m/%d/%Y"))

def format_date_google_calendar(date):  # Jinja2 calls this to get the date in the format for Google Calendar links
    """
    format a date object for Google Calendar
    - for now assumes that the events all last an hour
    eg: 20180512
    """
    return date.strftime("%Y%m%d")

def format_time_google_calendar(time):  # Jinja2 calls this to get the date in the format for Google Calendar links
    """
    format a date object for Google Calendar
    - for now assumes that the events all last an hour
    eg: 20180512
    """
    timeobj = datetime.strptime(time, "%I:%M %p")
    return timeobj.strftime("%H%M%S")

def format_date_outlook_calendar(date):  # Jinja2 calls this to get the date in the format for Outlook Calendar links
    """
    format a date object for Outlook Calendar
    - for now assumes that the events all last an hour
    eg: 20180512
    """
    return date.strftime("%Y-%m-%d")

def format_starttime_outlook_calendar(time):  # Jinja2 calls this to get the date in the format for Outlook Calendar links
    """
    format a date object for Outlook Calendar
    - for now assumes that the events all last an hour
    eg: 20180512
    """
    timeobj = datetime.strptime(time, "%I:%M %p")
    return timeobj.strftime("%H:%M:%S+00:00")

def format_endtime_outlook_calendar(time):  # Jinja2 calls this to get the date in the format for Outlook Calendar links
    """
    format a date object for Outlook Calendar
    - for now assumes that the events all last an hour
    eg: 20180512
    """
    timeobj = datetime.strptime(time, "%I:%M %p")
    timeobj += timedelta(hours=1)
    return timeobj.strftime("%H:%M:%S+00:00")

def committee_name_to_url(committee_name):  # e.g. "Rules & Legislation" -> 'rules-and-legislation'
    return re.sub(r'[^a-z]+', '-', committee_name.lower().replace('&', 'and'))



def load_meetings(scraped_data, committee_name_filter=None, upcoming_only=False, skip_cancellations=False):
    """
    given a parsed JSON file (scraped_data), returns a dict that can be used in the
    sidebar and main content area that looks like:

    {
        (date): [{meeting row dict}, {meeting row dict}, ...]
    }
    """
    today = datetime.now()
    midnight = datetime.combine(today, datetime.min.time())
    meetings_by_date = {}
    for meeting in scraped_data:
        # skip the meeting if the meeting name doesn't match the committee filter
        if committee_name_filter != "All Meetings":
            if committee_name_filter:
                normalized_meeting_name = meeting['EventBodyName'].replace(' & ', ' and ')
                normalized_filter = committee_name_filter.replace(' & ', ' and ')
                if normalized_meeting_name.find(normalized_filter) == -1:
                    continue

        # skip the meeting if only upcoming meetings were requested
        meeting_date = datetime.strptime(meeting['EventDate'], '%Y-%m-%dT%H:%M:%S')
        daydiff = (meeting_date - midnight).days
        if upcoming_only:
            if daydiff < 0:
                continue
        # skip upcoming meeting if only upcoming meetings were not requested
        else:
            if daydiff > 0:
                continue

        # Make agenda items more presentable
        for agendaItem in meeting.get('EventAgenda', []):
            title = agendaItem.get('EventItemTitle', '')
            if title and title.startswith('Subject:'):
                agendaItem['EventItemSubject'] = title.split("\n")[0].replace("Subject:","")
                meeting['EventAgendaDisplayable'] = True

        # Do not skip upcoming meetings in the Calendar if they are cancelled
        if not upcoming_only:
            # skip the meeting if it's a cancellation
            if skip_cancellations and 'cancel' in str(meeting['EventBodyName']).lower():  # different spelling of Cancel...
                continue

            # skip the meeting if there's no `EventDate` in the agenda:
            if not meeting['EventDate']:
                continue

            # skip if the word cancel is in the comments
            if "cancel" in str(meeting["EventComment"]).lower():
                continue

            # skip is desiginated a test meeting is in the comments
            if "THIS IS NOT A REAL MEETING" in str(meeting["EventComment"]):
                continue
        
        
        schedule = twitter_read_json([meeting], printit=False)
        meeting['TopicHashtags'] = schedule[0][-2]
        meeting['TopicEmojis'] = schedule[0][-1]

        # add the meeting to the calendar
        if not meeting_date in meetings_by_date:
            meetings_by_date[meeting_date] = []
        meetings_by_date[meeting_date].append(meeting)

    for meeting_date in meetings_by_date.keys():
        meetings_by_date[meeting_date].sort(
                key=lambda m: datetime.strptime(m['EventDate'], "%Y-%m-%dT%H:%M:%S"))

    return meetings_by_date


def render_committee_page(committee_name, year, meetings=[], sidebar_items=[]):
    slug = committee_name_to_url(committee_name)
    outfile = os.path.join(CURRENT_DIRECTORY, '../WebPage/website/{}/{}.html'.format(year, slug))

    # populate the list of "Other Years" for the page navigation
    other_years = {}
    for other_year in YEARS:
        link = '/{}{}/{}.html'.format(PATH_FROM_ROOT, other_year, slug)
        other_years[other_year] = link

    # populate the list of "Other Committees" for the page navigation
    other_committees = {}
    for other_committee_name in COMMITTEES:
        #link = '/{}{}/{}.html'.format(PATH_FROM_ROOT, year, committee_name_to_url(other_committee_name))
        link = '{}.html'.format(committee_name_to_url(other_committee_name))
        other_committees[other_committee_name] = link

    jinja_env = Environment(
        loader=FileSystemLoader(os.path.abspath(os.path.join(__file__, '../template'))),
        autoescape=select_autoescape(['html']),
    )
    jinja_env.globals.update(zip=zip)
    jinja_env.globals.update(str=str)
    jinja_env.globals.update(int=int)
    jinja_env.globals.update(re=re)

    jinja_env.filters['format_date'] = format_date
    jinja_env.filters['format_date_google_calendar'] = format_date_google_calendar
    jinja_env.filters['format_time_google_calendar'] = format_time_google_calendar
    jinja_env.filters['format_date_outlook_calendar'] = format_date_outlook_calendar
    jinja_env.filters['format_starttime_outlook_calendar'] = format_starttime_outlook_calendar
    jinja_env.filters['format_endtime_outlook_calendar'] = format_endtime_outlook_calendar
    jinja_env.filters['councilmatic_date'] = councilmatic_date
    template = jinja_env.get_template('committee.html')


    os.makedirs(os.path.dirname(os.path.abspath(outfile)), exist_ok=True)
    if year != 'upcoming':
        past_year = year
    else:
        past_year = False

    with open(outfile, 'w', encoding="utf-8") as f:
        template_args = {
            "other_years": other_years,
            "other_committees": other_committees,
            "committee": {
                "name": committee_name,
                "slug": slug,
            },
            "meetings": meetings,
            "past_year": past_year,
            "now": datetime.now(),
            "path_from_root": PATH_FROM_ROOT,
        }
        f.write(template.render(**template_args))


print(" ")
print("<------------------Running main.py - Version", VERSION, "------------>")
current_directory = os.path.abspath(os.path.dirname(__file__))

# determine the list of years that we'll render pages for

int_current_year = int(CURRENT_YEAR) + 1
if int_current_year - FIRSTYEAR > MAXYEARS:
    FIRSTYEAR = int_current_year - MAXYEARS
YEARS = list(range(FIRSTYEAR, int_current_year))
YEARS.reverse()

# load the data produced by `make scrape` the command
DATA_BY_YEAR = {}
for year in YEARS:
    try:
        # load the JSON for the year
        scraped_file = os.path.abspath(os.path.join(CURRENT_DIRECTORY, '../WebPage/website/scraped/Scraper{}.json'.format(year)))
        with open(scraped_file) as f:
            scraped_data = json.load(f)
        DATA_BY_YEAR[year] = scraped_data
    except Exception as e:
         raise Exception("Could not process {}: {}".format(scraped_file, e))

# generate a page for each committee in that year
for committee_name in COMMITTEES:
    # render the "Upcoming" page for that meeting
    upcoming_meetings = load_meetings(
            DATA_BY_YEAR[CURRENT_YEAR],
            committee_name_filter=committee_name,
            skip_cancellations=True,
            upcoming_only=True)
    render_committee_page(committee_name, 'upcoming', meetings=upcoming_meetings)

    for (year, scraped_data) in DATA_BY_YEAR.items():
        past_meetings = load_meetings(
                scraped_data,
                committee_name_filter=committee_name,
                skip_cancellations=True)
        render_committee_page(committee_name, year, meetings=past_meetings)

# generate symlinks for index.html files
index_path = os.path.abspath(os.path.join(CURRENT_DIRECTORY, "../WebPage/website/index.html"))
if not os.path.exists(index_path):
    os.symlink("upcoming/all-meetings.html", index_path)
# check
print("<------------------Program main.py completed------------------>")

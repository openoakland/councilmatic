# Creates a webpage
import os
import json
import re

from jinja2 import Template
from datetime import datetime

VERSION = "5.3"     # Version of Program
MAXYEARS = 10       # Maximum number of years to output
FIRSTYEAR = 2014    # First year to start
COMMITTEES = ["City Council", "Rules & Legislation", "Public Works", "Life Enrichment", "Public Safety",
              "Oakland Redevelopment", "Community & Economic Development", "Finance & Management"]
CURRENT_DIRECTORY = os.path.abspath(os.path.dirname(__file__))


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
        if committee_name_filter:
            normalized_meeting_name = meeting['name'].replace(' & ', ' and ')
            normalized_filter = committee_name_filter.replace(' & ', ' and ')
            if normalized_meeting_name.find(normalized_filter) == -1:
                continue

        # skip the meeting if only upcoming meetings were requested
        meeting_date = datetime.strptime(meeting['meeting_date'], '%m/%d/%Y')
        if upcoming_only:
            daydiff = (meeting_date - midnight).days
            if daydiff < 0:
                continue

        # Do not skip upcoming meetings in the Calendar if they are cancelled
        if not upcoming_only:
            # skip the meeting if it's a cancellation
            if skip_cancellations and 'cancellation' in meeting['name'].lower():
                continue

            # skip the meeting if there's no `meeting_time` in the agenda:
            if not meeting['meeting_time']:
                continue

        # add the meeting to the calendar
        if not meeting_date in meetings_by_date:
            meetings_by_date[meeting_date] = []
        meetings_by_date[meeting_date].append(meeting)

    for meeting_date in meetings_by_date.keys():
        meetings_by_date[meeting_date].sort(
                key=lambda m: datetime.strptime(m['meeting_time'], "%I:%M %p"))
    return meetings_by_date


def render_committee_page(output_filename, committee_name, year, meetings=[], sidebar_items=[]):
    # populate the list of "Other Committees" for the page navigation
    other_committees = {}
    for other_committee_name in COMMITTEES:
        link = '/{}/{}.html'.format(year, committee_name_to_url(other_committee_name))
        other_committees[other_committee_name] = link

    # populate the list of "Other Years" for the page navigation
    other_years = {}
    for other_year in YEARS:
        link = '/{}/{}.html'.format(other_year, slug)
        other_years[other_year] = link

    template = Template(open(os.path.join(CURRENT_DIRECTORY, './template/committee.html')).read())
    with open(output_filename, 'w') as f:
        template_args = {
            "other_years": other_years,
            "other_committees": other_committees,
            "sidebar_items": sidebar_items,
            "committee": {
                "name": committee_name,
            },
            "meetings": [meeting[0] for meeting in meetings.values()],
            "year": year,
            "now": datetime.now()
        }
        f.write(template.render(**template_args))


print(" ")
print("<------------------Running main.py - Version", VERSION, "------------------>")
current_directory = os.path.abspath(os.path.dirname(__file__))

# determine the list of years that we'll render pages for
CURRENT_YEAR = datetime.now().year
int_current_year = int(CURRENT_YEAR) + 1
if int_current_year - FIRSTYEAR > MAXYEARS:
    FIRSTYEAR = int_current_year - MAXYEARS
YEARS = list(range(FIRSTYEAR, int_current_year))
YEARS.reverse()

# load the data produced by `make scrape` the command
DATA_BY_YEAR = {}
for year in YEARS:
    # load the JSON for the year
    scraped_file = os.path.join(CURRENT_DIRECTORY, '../website/scraped/year{}.csv'.format(CURRENT_YEAR))
    with open(scraped_file) as f:
        scraped_data = json.load(f)
    DATA_BY_YEAR[year] = scraped_data

# the sidebar is identical regardless of the year; let's load the data for it
# first.
SIDEBAR_ITEMS = load_meetings(DATA_BY_YEAR[CURRENT_YEAR], upcoming_only=True)

# then, generate a page for each committee in that year
for (year, scraped_data) in DATA_BY_YEAR.items():
    for committee_name in COMMITTEES:
        slug = committee_name_to_url(committee_name)
        outfile = os.path.join(CURRENT_DIRECTORY, '../website/{}/{}.html'.format(year, slug))

        render_committee_page(outfile, committee_name, year, sidebar_items = SIDEBAR_ITEMS,
                              meetings=load_meetings(scraped_data, committee_name_filter=committee_name,
                                                skip_cancellations=True),)   # Don't know what this comma is for - HSM
        if committee_name == COMMITTEES[0]:
            outfile = os.path.join(CURRENT_DIRECTORY, '../website/{}/index.html'.format(year))
            render_committee_page(outfile, committee_name, year, sidebar_items = SIDEBAR_ITEMS,
                                  meetings=load_meetings(scraped_data, committee_name_filter=committee_name,
                                                         skip_cancellations=True),)
            if year == YEARS[0]:
                outfile = os.path.join(CURRENT_DIRECTORY, '../website/pc/index.html')
                render_committee_page(outfile, committee_name, year, sidebar_items = SIDEBAR_ITEMS,
                                  meetings=load_meetings(scraped_data, committee_name_filter=committee_name,
                                                         skip_cancellations=True),)


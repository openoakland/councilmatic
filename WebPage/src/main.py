# Creates a webpage
import os
import csv
import re

from jinja2 import Template
from datetime import datetime

YEARS = [2019, 2018, 2017, 2016, 2015, 2014]
COMMITTEES = ["City Council", "Rules & Legislation", "Public Works", "Life Enrichment", "Public Safety",
              "Oakland Redevelopment", "Community & Economic Development", "Finance & Management"]
CURRENT_DIRECTORY = os.path.abspath(os.path.dirname(__file__))


def committee_name_to_url(committee_name):
    ''' e.g. "Rules & Legislation" -> 'rules-and-legislation' '''
    return re.sub(r'[^a-z]+', '-', committee_name.lower().replace('&', 'and'))


def load_meetings(scraped_data, committee_name_filter=None, upcoming_only=False, skip_cancellations=False):
    '''
    given a parsed CSV (scraped_data), returns a dict that can be used in the
    sidebar and main content area that looks like:

    {
        (date): [{meeting row dict}, {meeting row dict}, ...]
    }
    '''

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
        link = '../../website/{}/{}.html'.format(year, committee_name_to_url(other_committee_name))
        other_committees[other_committee_name] = link

    # populate the list of "Other Years" for the page navigation
    other_years = {}
    for other_year in YEARS:
        link = '../../website/{}/{}.html'.format(other_year, slug)
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


# the sidebar is identical regardless of the year; let's load the data for it
# first.
current_year = datetime.now().year
scraped_file = os.path.join(CURRENT_DIRECTORY, '../website/scraped/year{}.csv'.format(current_year))
scraped_data = list(csv.DictReader(open(scraped_file, encoding="utf-8"),
    delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL, skipinitialspace=True))
sidebar_items = load_meetings(scraped_data, upcoming_only=True)

# generate the pages for other years
for year in YEARS:
    # load the CSV for the year
    scraped_file = os.path.join(CURRENT_DIRECTORY, '../website/scraped/year{}.csv'.format(year))
    scraped_data = list(csv.DictReader(open(scraped_file, encoding="utf-8"),
        delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL, skipinitialspace=True))

    # generate a page for each committee in that year
    for committee_name in COMMITTEES:
        slug = committee_name_to_url(committee_name)
        outfile = os.path.join(CURRENT_DIRECTORY, '../website/{}/{}.html'.format(year, slug))

        render_committee_page(outfile, committee_name, year,
            sidebar_items=sidebar_items,
            meetings=load_meetings(scraped_data, committee_name_filter=committee_name, skip_cancellations=True),
        )

# This program creates a sidebar for Councilmatic
# Create by Howard Matis for OpenOakland - October 23, 2018
#
# Takes data scraped from Oakland Legistar web page - https://oakland.legistar.com/Calendar.aspx
#

import csv
from datetime import datetime, timedelta
import calendar
from create_html import create_html


def read_csv_file(datafile, elements):
    data = list(csv.reader(open(datafile,encoding="utf-8"), delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL,
                           skipinitialspace=True))
    numrows = len(data)
    present = datetime.now()
    today = present.strftime('%m/%d/%Y')

    for i in range(numrows):  # Find out which meetings have not occurred
        if i > 0:  # Don't read headers
            if len(data[i][:]) >= 8:
                meeting_daytime = datetime.strptime(data[i][1], '%m/%d/%Y')  # Convert to daytime format to compare
                meeting_day = meeting_daytime.strftime('%m/%d/%Y')
                future_meeting = meeting_day >= today
                if not future_meeting:
                    break
                elements.append([])
                for j in range(0, 10):
                    elements[i - 1].append(0)
                    elements[i - 1][j] = data[i][j]


def write_day_header(f2, day1, day2):
    f2.write('<div class="calendar_plan">' + "\n")
    f2.write('<div class="cl_plan">' + "\n")
    f2.write('<div class="cl_title"> <font size="+3">' + day1 + '</font> </div>' + "\n")
    f2.write('<div class="cl_copy">' + day2 + '</div>' "\n")
    f2.write('</div>' + "\n")
    f2.write('</div>' + "\n")

#
# write out an icon with link and tooltip
#


def write_image_link(f2, alt_value, image_loc, html_link, tool_tip):
    f2.write('<a href="' + html_link + '" data-toggle="tooltip" title="' + tool_tip+ '">' + "\n")
    f2.write('<img alt="' + alt_value + '" src="' + image_loc + '" width="32" height="32">'
             + "</a>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" + "\n")


def write_event_header(f2, time_event, link_calendar, name_committee, name_location, link_agenda, link_ecoomment):
    f2.write('<div class="event_item">' + "\n")
    f2.write('<div class="ei_Dot"></div>' + "\n")
    f2.write('<div class="ei_Title">' + time_event + "&nbsp;&nbsp&nbsp;&nbsp;&nbsp;&nbsp;" + "\n")

    write_image_link(f2, "calendar", "../images/iCal-icon-32.png", link_calendar, "Add to Calendar")

    if "https" in link_agenda:
        write_image_link(f2, "agenda", "../images/agenda-32.png", link_agenda, "Agenda")

    if "https" in link_ecoomment:
        write_image_link(f2, "Comment Online", "../images/comment-32.png", link_ecoomment, "Comment Online")

    f2.write("</div>" + "\n")
    f2.write('<div class="ei_Copy"> <font size="+1">' + name_committee + '</font> <br/> ' + name_location + "\n")
    f2.write('</div>' + "\n")
    f2.write('</div>' + "\n")
    f2.write(' ' + "\n")


version = "4.0"
lookAhead = 21  # Number of the days to look ahead for meetings

print(" ")
print("<---------Running Software Version:", version, "- sidebar.py ----------->")

dynamic = "temp/dynamic_calendar.txt"
f1 = open(dynamic, 'w+')

#
#   write the top section of the column
url = "template/template_sidebar.txt"
create_html(url, f1)  # Create  template for HTML page
f1.write(" " + "\n")

currentDay = datetime.now().day
currentMonth = datetime.now().month
currentYear = datetime.now().year
formatedDay = datetime.now().strftime("%A, %B %d,  %Y %I:%M %p")
theDate = '<font size="-1">Updated: ' + str(formatedDay) + '<br> </font></p>'
f1.write(theDate + "\n")

# Check if close to a new year

if currentMonth == 12:  # See if need to look at next year's record
    if currentDay > 31 - lookAhead:
        years = [str(currentYear + 1), str(currentYear)]  # Allows reading later file first
    else:
        years = [str(currentYear)]
else:
    years = [str(currentYear)]

schedule = []
for year in years:
    scraper_file = "../website/scraped/year" + str(year) + ".csv"
    print("Scraping", scraper_file)
    read_csv_file(scraper_file, schedule)

numrows = len(schedule)
today = datetime.now()
lastdate = today - timedelta(days=1)
tomorrow = today + timedelta(days=1)
today_day = str(today.month) + '/' + str(today.day) + '/' + str(today.year)
tomorrow_day = str(tomorrow.month) + '/' + str(tomorrow.day) + '/' + str(tomorrow.year)
for i in range(numrows - 1, 0, -1):
    event_day = schedule[i][1]

    if lastdate != event_day:
        lastdate = event_day
        new_day = True
    else:
        new_day = False

    if new_day:
        day_datetime = datetime.strptime(event_day, '%m/%d/%Y')
        day_label = datetime.date(day_datetime).weekday()
        day_of_week = calendar.day_name[day_label]
        if event_day == today_day:
            day_of_week = "Today"
        elif event_day == tomorrow_day:
            day_of_week = "Tomorrow"

        print(event_day)
        print("New Day")
        write_day_header(f1, day_of_week, event_day)

    committee = schedule[i][0]
    if "City Council" in committee:
        committee = "City Council - (" + committee + ")"
    print("Meeting description")
    print(committee)  # Committee
    print(schedule[i][2])  # Calendar
    print(schedule[i][3])  # Time
    print(schedule[i][4])  # Room
    agenda = schedule[i][6]
    ecomment = schedule[i][9]
    write_event_header(f1, schedule[i][3], schedule[i][2], committee, schedule[i][4], agenda, ecomment)

#
#   write closing section
url = "template/template_sidebar_bottom.txt"
create_html(url, f1)  # Finish the sidebar
f1.write(" " + "\n")

f1.close()  # Close the file

# Now make the HTML Code

outfile = "../website/mobile/index.html"
f2 = open(outfile, 'w+')

#   write style section of the web page
url = "template/template_style.txt"
create_html(url, f2)  # Create  template for HTML page
f2.write(" " + "\n")
#
#   write the sidebar
url = dynamic
create_html(url, f2)  # Create  body of HTML page
f2.write(" " + "\n")
#
#   write end of webpage
url = "template/template_sidebar_end.txt"
create_html(url, f2)  # end of HTML page
f2.write(" " + "\n")
#
f2.close()  # Close the file

print("<----------------End of process - sidebar.py----------------->")
print(" ")
quit()

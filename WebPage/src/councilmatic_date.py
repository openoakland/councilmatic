
#
# Written by Howard Matis - June 6, 2019
# 
# Code looks at the day of the week and adds text to make clear which week it represents
# It also labels today and tomorrow.
#
#  The input of the routine is a date in datetime format that you want to display
#  The output is the text that we want to display
import datetime


def councilmatic_date(mydate):
    today = datetime.datetime.now()
    tomorrow = today + datetime.timedelta(days=1)
    weekdiff =  int(mydate.strftime('%U')) - int(today.strftime('%U'))

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


# Compare two files acquired from the Legistar API to produce a list of changed items.
# Command line arguments:
# arg1: older file to compare.
# arg2: newer of the files to compare.

# Run: python legistar_json_file_compare.py  Scraper20200811_1434.json.json
# These files can be pulled from 
# http://datawhim.net/Scraper20200731_2126.json
# http://datawhim.net/Scraper20200811_1434.json

# This dumps to the console but can be redirected to a file on the command line.



import sys
import json
import os
import re
from datetime import datetime

'''
Function to find max LastModifiedUtc in a dict of Event Items or Matter Attachments.
Parameters:
    data_array (array): 
    datasetid (str): This will be 'EventAgenda' or 'EventItemMatterAttachments', the name containing the data_array.
    currentmaxdt (datetime): A datetime value that acts as a minimum value for the result from this function. 
'''
def max_modified_datetime(data_array, datasetid, currentmaxdt):
    #print ('The datasetid is ' + datasetid)
    if (datasetid == 'EventAgenda'):
        key_for_modified_utc = 'EventItemLastModifiedUtc'
    else:  # assumed EventItemMatterAttachments
        key_for_modified_utc = 'MatterAttachmentLastModifiedUtc'
    modtime_generator = (oneelement[key_for_modified_utc][0:19] for oneelement in data_array)
    in_process_max = currentmaxdt
    for modtime in modtime_generator:
        #print('in_process_max: ' + in_process_max + '  modtime: ' + modtime)
        in_process_max = max(in_process_max, modtime)
        #print('new in_process_max: ' + in_process_max)
    return in_process_max
# - - - - - - - - - - - - - - - - - - - -


# - - - - - - - - - - - - - - - - - - - -
# Check that two arguments are present.
# - - - - - - - - - - - - - - - - - - - -
if len(sys.argv) < 2:
    print ('Two arguments are required, one for each of the files to be compared. These '\
          'are strings including full path and file name.') 
    sys.exit(1)  # abort because of error

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Find which file has the earlier mod date and name it accordingly.
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Acquire the values of the arguments
file1 = sys.argv[1]
file2 = sys.argv[2]

# Find the Modified dates for the files
#file1_timestamp = os.stat( file1 ).st_mtime  # stat dates change as files are copied
#file2_timestamp = os.stat( file2 ).st_mtime  # stat dates change as files are copied
dtpattern = re.compile(r"(\d{4})(\d{2})(\d{2})(\d{2})(\d{2})(\d{2})")
datestringmatches = dtpattern.findall(file1)
# Todo: add error message here if len(datestringmatches) > 1
dsmatch = datestringmatches[0]
file1_timestamp = datetime( int(dsmatch[0]), int(dsmatch[1]), int(dsmatch[2]),
                                     int(dsmatch[3]), int(dsmatch[4]), int(dsmatch[5]) ).timestamp()
datestringmatches = dtpattern.findall(file2)
# Todo: add error message here if len(datestringmatches) > 1
dsmatch = datestringmatches[0]
file2_timestamp = datetime( int(dsmatch[0]), int(dsmatch[1]), int(dsmatch[2]),
                                     int(dsmatch[3]), int(dsmatch[4]), int(dsmatch[5]) ).timestamp()
#print('The timestamp of the first file is: ',file1_timestamp)
#print('The timestamp of the second file is: ',file2_timestamp)

# Determine which time stamp is older.
if (file1_timestamp < file2_timestamp):
    prior_file = open(file1)
    latest_file = open(file2)
    #prior_file_dt = datetime.utcfromtimestamp(file1_timestamp).strftime('%Y-%m-%dT%H:%M:%S')
    #latest_file_dt = datetime.utcfromtimestamp(file2_timestamp).strftime('%Y-%m-%dT%H:%M:%S')
    # Test files have UTC modified times.  Test PC has -7 timezoneOffset. :: Above function 'overcorrects' on PC
    prior_file_dt = datetime.fromtimestamp(file1_timestamp).strftime('%Y-%m-%dT%H:%M:%S')
    latest_file_dt = datetime.fromtimestamp(file2_timestamp).strftime('%Y-%m-%dT%H:%M:%S')
else:
    prior_file = open(file2)
    latest_file = open(file1)
    #prior_file_dt = datetime.utcfromtimestamp(file2_timestamp).strftime('%Y-%m-%dT%H:%M:%S')
    #latest_file_dt = datetime.utcfromtimestamp(file1_timestamp).strftime('%Y-%m-%dT%H:%M:%S')
    prior_file_dt = datetime.fromtimestamp(file2_timestamp).strftime('%Y-%m-%dT%H:%M:%S')
    latest_file_dt = datetime.fromtimestamp(file1_timestamp).strftime('%Y-%m-%dT%H:%M:%S')

# print('Timestamp of oldest file:' + datetime.utcfromtimestamp(file1_timestamp).strftime('%Y-%m-%dT%H:%M:%S'))
# print('Timestamp of newest file:' + datetime.utcfromtimestamp(file2_timestamp).strftime('%Y-%m-%dT%H:%M:%S'))

latest_json_array = json.load(latest_file)
prior_json_array = json.load(prior_file)

# ipython test code - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# filename1 = "F:\Data\JetBrains\PyCharmProjects\OpenOakland\councilmatic_project\PythonFileDiffWork\Scraper2020(20200617_2330).json"
# file1 = open(filename1)
# import json
# jsondata1 = json.load(file1)
# dir(jsondata1)
# len(jsondata1)
# type(jsondata1)
# type(jsondata1[0])
# dir(jsondata1[0])
# jsondata1[0].keys()
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# print('prior_file_dt: ' + prior_file_dt)

# ! Remember that we also need to also detect additions and deletions.

item_exception_list = ['EventActualLastModifiedUtc', 'EventAgenda', 'EventAgendaLastPublishedUTC',
                       'EventAgendaStatusId', 'EventBodyId', 'EventComment', 'EventGuid', 'EventId',
                       'EventInSiteURL', 'EventItemAccelaRecordId', 'EventItemActionId', 'EventItemActionName',
                       'EventItemActionText', 'EventItemAgendaNumber', 'EventItemEventId', 'EventItemFlagExtra',
                       'EventItemGuid', 'EventItemId', 'EventItemLastModifiedUtc', 'EventItemMatterAttachments',
                       'EventItemMatterGuid', 'EventItemMatterId', 'EventItemMinutesSequence',
                       'EventItemMoverId', 'EventItemPassedFlag', 'EventItemPassedFlagName',
                       'EventItemRollCallFlag', 'EventItemRowVersion', 'EventItems', 'EventItemSeconderId',
                       'EventItemTally', 'EventItemVersion', 'EventItemVideoIndex', 'EventLastModifiedUtc',
                       'EventMinutesLastPublishedUTC', 'EventMinutesStatusId', 'EventRowVersion',
                       'MatterAttachmentAgiloftId', 'MatterAttachmentBinary', 'MatterAttachmentDescription',
                       'MatterAttachmentFileName', 'MatterAttachmentGuid', 'MatterAttachmentIsBoardLetter',
                       'MatterAttachmentId', 'MatterAttachmentIsHyperlink', 'MatterAttachmentIsMinuteOrder',
                       'MatterAttachmentIsSupportingDocument', 'MatterAttachmentLastModifiedUtc',
                       'MatterAttachmentMatterVersion', 'MatterAttachmentPrintWithReports',
                       'MatterAttachmentRowVersion', 'MatterAttachmentShowOnInternetPage', 'MatterAttachmentSort']

results_list = []

# @ @ @ @ @ @ @ @ Loop Through All Modified Dates To Find True LastModifiedUtc Date For Each Event  @ @ @ @ @ @ @ @ @
for i,event_dict in enumerate(latest_json_array):
    max_mod_dtstr = event_dict['EventLastModifiedUtc'][0:19]
    newmax = max_modified_datetime(event_dict['EventAgenda'], 'EventAgenda', max_mod_dtstr)
    if event_dict['EventAgenda']:
        for event_item_dict in event_dict['EventAgenda']:
            newmax = max_modified_datetime(event_item_dict['EventItemMatterAttachments'], 'EventItemMatterAttachments', newmax)
    #if (newmax != max_mod_dtstr):
        #print('Tests for finding the latest mod datetime: ' + newmax + '  The Event Last Mod DT was ' + max_mod_dtstr + '  For EventId: ' + str(event_dict['EventId']) + '  Enumerator: ' + str(i))
    # Store the Actual Last Mod DT in the JSON structure.
    latest_json_array[i]['EventActualLastModifiedUtc'] = newmax

#print ('The Actual Last Mod DT for the 3rd event is ' + latest_json_array[3]['EventActualLastModifiedUtc'])
#print ('The Actual Last Mod DT for the 9th event is ' + latest_json_array[9]['EventActualLastModifiedUtc'])
#sys.exit()


# @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @  EVENTS  @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @
# Loop through event dictionaries
for latest_event_dict in latest_json_array:
    # Find those with a change date AFTER the prior file date.
    #chngdtstr = latest_event_dict['EventLastModifiedUtc'][0:19]
    chngdtstr = latest_event_dict['EventActualLastModifiedUtc']
    if (chngdtstr > prior_file_dt):
        # Get the dict for the same event from the "prior" array (which is from the prior file).
        prior_event_dict = next((pitem for pitem in prior_json_array if pitem["EventId"] == latest_event_dict['EventId']),-1)

        # Check if above iterator above reached its end (didn't find a match... which means new EI)
        if prior_event_dict == -1:
            print('***New EventId: ' + str(latest_event_dict['EventId']) + '  Event title: ' +
                  latest_event_dict['EventBodyName'])
            print()
            results_list.append({"DataElementFamily":"Event",
                                 "ChangeDetected":latest_file_dt,
                                 "ChangeType": 'New',
                                 "DataElementKey": evkey,
                                 "OldValue":None,
                                 "NewValue":"new",
                                 "EventId":latest_event_dict['EventId'],
                                 "EventBodyId":latest_event_dict['EventBodyId'],
                                 "EventBodyName":latest_event_dict['EventBodyName'],
                                 "EventDT":latest_event_dict['EventDate'][0:10] + ' ' + latest_event_dict['EventTime'],
                                 "EventItemId":None,
                                 "EventItemTitle": None,
                                 "MatterAttachmentId":None,
                                 "MatterAttachmentName": None})
            continue

        # Find changes in event data by loop through dict elements.
        # Loop through the name-value pairs for the event (meeting).  Convert the dict to list of tuples for looping.
        for evkey,evvalue in latest_event_dict.items():
            if evkey in item_exception_list:
                continue
            # If the element is an agenda and its not empty then loop through.
            # Todo: first check the value of "EventItemLastModifiedUtc" against prior_file_dt like above.

            # @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @  EVENT ITEMS  @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @
            # - - - - - - - - - - If Event Agenda, look for diffs in the Event Items - - - - - - - - - -
            if evkey == 'EventAgenda' and len(evvalue) > 0:
                # print('The type of the var "evvalue" is ' + str(type(evvalue)))
                # The var 'evvalue' now contains the list of agenda items (event_item)[dict] within the EventAgenda [list].
                for event_item_dict in evvalue:

                    # - - - - - - - - - - Qualify the Event Item - - - - - - - - - -
                    # Find event items with a change date AFTER the prior file date.
                    eichngdtstr = event_item_dict['EventItemLastModifiedUtc'][0:19]
                    if (eichngdtstr > prior_file_dt):
                        # print("First event item with a later change date: EventItemId = " + str(event_item_dict['EventItemId']))
                        # sys.exit(94)

                        # Get the dict of the corresponding event item id from the 'prior' dict
                        prior_ei_dict = next(
                            (peitem for peitem in prior_event_dict['EventAgenda'] if
                             peitem["EventItemId"] == event_item_dict['EventItemId']), -1)

                        # Check if above iterator above reached its end (didn't find a match... which means new EI)
                        if prior_ei_dict == -1:
                            print('+++New EventItemId: ' + str(event_item_dict['EventItemId']) + '  Event title: ' +
                                  (event_item_dict['EventItemTitle'] or '<em>This event item currently has no title.</em>'))
                            print()
                            results_list.append({"DataElementFamily": "EventItem",
                                                 "ChangeDetected":latest_file_dt,
                                                 "ChangeType": 'New',
                                                 "DataElementKey": evkey,
                                                 "OldValue": None,
                                                 "NewValue": "new",
                                                 "EventId": latest_event_dict['EventId'],
                                                 "EventBodyId": latest_event_dict['EventBodyId'],
                                                 "EventBodyName": latest_event_dict['EventBodyName'],
                                                 "EventDT":latest_event_dict['EventDate'][0:10] + ' ' + latest_event_dict['EventTime'],
                                                 "EventItemId": event_item_dict['EventItemId'],
                                                 "EventItemTitle": event_item_dict['EventItemTitle'],
                                                 "MatterAttachmentId": None,
                                                 "MatterAttachmentName": None})
                            continue

                        # Loop through the dict pair of accepted Event Items
                        for eikey,eivalue in event_item_dict.items():
                            # Skip if name of the event item name-value pairs is in exception list.
                            if eikey in item_exception_list:
                                continue

# @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @  EVENT ITEM MATTER ATTACHMENTS  @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @
                            # - - - - - - - - - - If Event Agenda, look for diffs in the Event Items - - - - - - - - - -
                            if eikey == 'EventItemMatterAttachments' and len(evvalue) > 0:
                                for eima_dict in eivalue:

                                    # - - - - - - - - Qualify the Event Item Matter Attachment (EIMA) - - - - - - - -
                                    # Find EIMAs with a change date AFTER the prior file date.
                                    eimachngdtstr = eima_dict['MatterAttachmentLastModifiedUtc'][0:19]
                                    if (eimachngdtstr > prior_file_dt):
                                        # print("First event item with a later change date: EventItemId = " + str(event_item_dict['EventItemId']))
                                        # sys.exit(94)

                                        # Get the dict of the corresponding event item id from the 'prior' dict
                                        prior_eima_dict = next(
                                            (peima for peima in prior_ei_dict['EventItemMatterAttachments'] if
                                             peima["MatterAttachmentId"] == eima_dict['MatterAttachmentId']), -1)

                                        # Check if iterator above reached its end (didn't find a match... which means new EI)
                                        if prior_eima_dict == -1:
                                            print('~/~New MatterAttachmentId: ' +
                                                  str(eima_dict['MatterAttachmentId']) + '  Matter attachment name: ' +
                                                  eima_dict['MatterAttachmentName'])
                                            print()
                                            results_list.append({"DataElementFamily": "MatterAttachment",
                                                                 "ChangeDetected":latest_file_dt,
                                                                 "ChangeType": 'New',
                                                                 "DataElementKey": 'EventItemMatterAttachmentId',
                                                                 "OldValue": None,
                                                                 "NewValue": str(eima_dict['MatterAttachmentId']),
                                                                 "EventId": latest_event_dict['EventId'],
                                                                 "EventBodyId": latest_event_dict['EventBodyId'],
                                                                 "EventBodyName": latest_event_dict['EventBodyName'],
                                                                 "EventDT":latest_event_dict['EventDate'][0:10] + ' ' + latest_event_dict['EventTime'],
                                                                 "EventItemId": event_item_dict['EventItemId'],
                                                                 "EventItemTitle": event_item_dict['EventItemTitle'],
                                                                 "MatterAttachmentId": eima_dict['MatterAttachmentId'],
                                                                 "MatterAttachmentName": eima_dict['MatterAttachmentName']})
                                            continue

                                        # Loop through the dict pair of accepted Event Items
                                        for eimakey,eimavalue in eima_dict.items():
                                            # Skip if name of the event item name-value pairs is in exception list.
                                            if eimakey in item_exception_list:
                                                continue

                                            # Print Matter Attachment data if the eimavalue is not the same between latest and prior
                                            if type(eimavalue) is not list and eimavalue != prior_eima_dict[eimakey]:
                                                print('~~~MatterAttachmentId: ' + str(eima_dict['MatterAttachmentId']))
                                                print(eimakey + ': ' + str(prior_eima_dict[eimakey]) + ' ==> ' + str(eimavalue) + ' ::')
                                                print()
                                                changetype = 'Added' if prior_eima_dict[eimakey] == None else 'Update'
                                                results_list.append({"DataElementFamily": 'EventItemMatterAttachment',
                                                                     "ChangeDetected": latest_file_dt,
                                                                     "ChangeType": 'Update',
                                                                     "DataElementKey": eimakey,
                                                                     "OldValue": str(prior_eima_dict[eimakey]),
                                                                     "NewValue": str(eimavalue),
                                                                     "EventId": latest_event_dict['EventId'],
                                                                     "EventBodyId": latest_event_dict['EventBodyId'],
                                                                     "EventBodyName": latest_event_dict['EventBodyName'],
                                                                     "EventDT":latest_event_dict['EventDate'][0:10] + ' ' + latest_event_dict['EventTime'],
                                                                     "EventItemId": event_item_dict['EventItemId'],
                                                                     "EventItemTitle": event_item_dict['EventItemTitle'],
                                                                     "MatterAttachmentId": eima_dict['MatterAttachmentId'],
                                                                     "MatterAttachmentName": eima_dict['MatterAttachmentName']})

                            # Print Event Item data if the eivalue is not the same between latest and prior
                            # Todo: Is the following "not list" needed.  It was initially to rule out
                            #  "EventItemMatterAttachments".  May want to keep in case new sublists are added in the future.
                            if type(eivalue) is not list and eivalue != prior_ei_dict[eikey]:
                                print('+++EventItemId: ' + str(event_item_dict['EventItemId']))
                                print(eikey + ': ' + str(prior_ei_dict[eikey]) + ' ===> ' + str(eivalue))
                                print()
                                changetype = 'Added' if prior_ei_dict[eikey] == None else 'Update'
                                results_list.append({"DataElementFamily": "EventItem",
                                                     "ChangeDetected":latest_file_dt,
                                                     "ChangeType": changetype,
                                                     "DataElementKey": eikey,
                                                     "OldValue": str(prior_ei_dict[eikey]),
                                                     "NewValue": str(eivalue),
                                                     "EventId": latest_event_dict['EventId'],
                                                     "EventBodyId": latest_event_dict['EventBodyId'],
                                                     "EventBodyName": latest_event_dict['EventBodyName'],
                                                     "EventDT":latest_event_dict['EventDate'][0:10] + ' ' + latest_event_dict['EventTime'],
                                                     "EventItemId": event_item_dict['EventItemId'],
                                                     "EventItemTitle": event_item_dict['EventItemTitle'],
                                                     "MatterAttachmentId": None,
                                                     "MatterAttachmentName": None})
            if type (latest_event_dict[evkey]) is not list and latest_event_dict[evkey] != prior_event_dict[evkey]:
                print('***EventId: ' + str(latest_event_dict['EventId']))
                print('***EventBodyName: ' + str(latest_event_dict['EventBodyName']))
                print(evkey + ': ' + str(prior_event_dict[evkey]) + ' ====> ' + str(evvalue))
                print()
                changetype = 'Added' if prior_event_dict[evkey] == None else 'Update'
                results_list.append({"DataElementFamily":"Event",
                                     "ChangeDetected":latest_file_dt,
                                     "ChangeType": changetype,
                                     "DataElementKey": evkey,
                                     "OldValue":prior_event_dict[evkey],
                                     "NewValue":latest_event_dict[evkey],
                                     "EventId":latest_event_dict['EventId'],
                                     "EventBodyId":latest_event_dict['EventBodyId'],
                                     "EventBodyName":latest_event_dict['EventBodyName'],
                                     "EventDT":latest_event_dict['EventDate'][0:10] + ' ' + latest_event_dict['EventTime'],
                                     "EventItemId":None,
                                     "EventItemTitle": None,
                                     "MatterAttachmentId":None,
                                     "MatterAttachmentName": None})
        print()

# results_list = {"1 and 2":results_list}  if I need to put a list identifier
# now write output to a file
resultJSONFile = open("results.json", "w")
# magic happens here to make it pretty-printed
resultJSONFile.write(json.dumps(results_list, sort_keys=False, indent=4))
resultJSONFile.close()
#print(json.dumps(results_list, sort_keys=True, indent=4))
print('Done with file of ' + latest_file_dt)

"""
Check for changes in these event items accessed in the ./src-Webpage/main.py script.
EventAgendaDisplayable
EventItemSubject // Not found in the 2020 example files
EventDate
EventBodyName
EventItemMatterType
EventItemSubject // Not found in the 2020 example files

See F:\Data\JetBrains\PyCharmProjects\councilmatic\src-Webpage\template\committee.html near line 117
for how elements of the json file are used. This should help to determine which are relevant and 
need to be monitored for changes.

Can use PowerGREP on directory
F:\Data\JetBrains\PyCharmProjects\councilmatic
with grep search of 
(\[|\()\'(EventAgendaDisplayable |EventItemSubject|EventDate|EventBodyName )
"""



    


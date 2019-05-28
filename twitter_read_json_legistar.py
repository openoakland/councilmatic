import json


def parse_timestamp(ts):
    year, month, day = ts[:10].split('-')
    return f"{month}/{day}/{year}"


def twitter_read_json(printit=False):
    with open('meetings.json') as f:
        meetings = json.load(f)

    csv = [[m['EventBodyName'],
            parse_timestamp(m['EventDate']),
            m['EventTime'],
            m['EventAgendaFile'] or '']
         for m in meetings]

    if printit:
        for m in csv:
            print('\n'.join(m))

    return csv

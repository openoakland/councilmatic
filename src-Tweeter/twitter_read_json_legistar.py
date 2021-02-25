# Written by Max Flander
# Scrapes data by using Legistar API

import json
import re


def parse_timestamp(ts):
    year, month, day = ts[:10].split("-")
    return f"{month}/{day}/{year}"


def read_topics(filename):
    with open(filename) as f:
        data = f.read()

    rows = data.split("\n")[1:-1]
    keyword_map = {}
    for row in rows:
        topic, keywords, emoji = row.split("\t")
        for keyword in keywords.split(","):
            keyword_map[keyword] = {"topic": topic, "emoji": emoji}

    return keyword_map


def get_topics(meeting, keyword_map):
    topics = set()  # Tells this is an Oakland meeting
    topics.add("#oakmtg ")
    emojis = set()
    agenda = (
        meeting["EventBodyName"]
        + " "
        + " ".join(a["EventItemTitle"] or "" for a in meeting["EventAgenda"])
    )
    for k, v in keyword_map.items():
        if re.search("\\b" + k + "\\b", agenda, re.IGNORECASE):
            # topics.add("#" + v['topic'].replace(' ', ''))
            topics.add(
                "#" + v["topic"].replace(" ", "") + " "
            )  # HSM adding a space afterwards
            emojis.add(v["emoji"])

    return "".join(topics), "".join(emojis)


def twitter_read_json(filename, printit=False):
    with open(filename) as f:
        meetings = json.load(f)

    topics = read_topics("src-Tweeter/topics.tsv")

    csv = [
        [
            m["EventBodyName"],
            parse_timestamp(m["EventDate"]),
            m["EventTime"],
            m["EventAgendaFile"] or "",
        ]
        + list(get_topics(m, topics))
        for m in meetings
    ]

    if printit:
        for m in csv:
            print("\n".join(m))

    return csv

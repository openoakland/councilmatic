# These are all the settings that are specific to a jurisdiction

###############################
# These settings are required #
###############################

OCD_JURISDICTION_ID = 'ocd-jurisdiction/country:us/state:ca/place:oakland/legislature'
OCD_CITY_COUNCIL_ID = 'ocd-organization/c1113ace-40db-4a92-8202-9d5f97bf5916'
CITY_COUNCIL_NAME = 'Oakland City Council'
LEGISLATIVE_SESSIONS = ['2007', '2011', '2015'] # the last one in this list should be the current legislative session
CITY_NAME = 'Oakland'
CITY_NAME_SHORT = 'Oakland'

# VOCAB SETTINGS FOR FRONT-END DISPLAY
CITY_VOCAB = {
    'MUNICIPAL_DISTRICT': 'District',       # e.g. 'District'
    'SOURCE': 'Oakland City Clerk',
    'COUNCIL_MEMBER': 'Council Member',       # e.g. 'Council Member'
    'COUNCIL_MEMBERS': 'Council Members',      # e.g. 'Council Members'
    'EVENTS': 'Meetings',               # label for the events listing, e.g. 'Events'
}

APP_NAME = 'oakland'


#########################
# The rest are optional #
#########################

# this is for populating meta tags
SITE_META = {
    'site_name' : 'Oakland Councilmatic',       # e.g. 'Chicago Councilmatc'
    'site_desc' : 'Oakland City Council activity, simplified. Keep tabs on city council meetings and activity and the activities of your council members.',       # e.g. 'City Council, demystified. Keep tabs on Chicago legislation, aldermen, & meetings.'
    'site_author' : 'OpenOakland',     # e.g. 'DataMade'
    'site_url' : 'https://opencouncil.openoakland.org/',        # e.g. 'https://chicago.councilmatic.org'
    'twitter_site': '@Oakland',     # e.g. '@DataMadeCo'
    'twitter_creator': '@Oakland',  # e.g. '@DataMadeCo'
}

LEGISTAR_URL = 'https://oakland.legistar.com/Legislation.aspx'           # e.g. 'https://chicago.legistar.com/Legislation.aspx'


# this is for the boundaries of municipal districts, to add
# shapes to posts & ultimately display a map with the council
# member listing. the boundary set should be the relevant
# slug from the ocd api's boundary service
# available boundary sets here: http://ocd.datamade.us/boundary-sets/
BOUNDARY_SET = ''           # e.g. 'chicago-wards-2015'

# this is for configuring a map of council districts using data from the posts
# set MAP_CONFIG = None to hide map
MAP_CONFIG = {
    'center': [37.80532, -122.272544],
    'zoom': 10,
    'color': "#54afe8",
    'highlight_color': "#C00000",
}


FOOTER_CREDITS = [
    {
        'name':     'OpenOakland', # e.g. 'DataMade'
        'url':      'http://openoakland.org/', # e.g. 'http://datamade.us'
        'image':    'logo_openoakland.png', # e.g. 'datamade-logo.png'
    },
]

# this is the default text in search bars
SEARCH_PLACEHOLDER_TEXT = 'zoning, tenants, Libby Schaaf, Free Food' # e.g. 'police, zoning, O2015-7825, etc.'

# these should live in oakland/static/
IMAGES = {
    'favicon': 'images/icons/favicon.ico',
    'logo': 'images/logo_oakland.png',
}




# THE FOLLOWING ARE VOCAB SETTINGS RELEVANT TO DATA MODELS, LOGIC
# (this is diff from VOCAB above, which is all for the front end)

# this is the name of the meetings where the entire city council meets
# as stored in legistar
CITY_COUNCIL_MEETING_NAME = 'City Council'

# this is the name of the role of committee chairs, e.g. 'CHAIRPERSON' or 'Chair'
# as stored in legistar
# if this is set, committees will display chairs
COMMITTEE_CHAIR_TITLE = 'President'

# this is the anme of the role of committee members,
# as stored in legistar
COMMITTEE_MEMBER_TITLE = 'Member'




# this is for convenience, & used to populate a table
# describing legislation types on the default about page template
LEGISLATION_TYPE_DESCRIPTIONS = [
    {
        'name': 'Ordinance',
        'search_term': 'ordinance',
        'fa_icon': 'file-text-o',
        'html_desc': True,
        'desc': '',
    },
    {
        'name': 'Proclamation',
        'search_term': 'proclamation',
        'fa_icon': 'file-text-o',
        'html_desc': True,
        'desc': '',
    },
    {
        'name': 'City Resolution',
        'search_term': 'resolution',
        'fa_icon': 'file-text-o',
        'html_desc': True,
        'desc': '',
    },
]

# these keys should match committee slugs
COMMITTEE_DESCRIPTIONS = {
    # "committee-on-aviation" : "The Committee on Aviation has jurisdiction over matters relating to aviation and airports.",
}

# these blurbs populate the wells on the committees, events, & council members pages
ABOUT_BLURBS = {
    "COMMITTEES" :      "Committees",
    "EVENTS":           "Events",
    "COUNCIL_MEMBERS":  "Council Members",
}

# these override the headshots that are automatically populated
# the keys should match a person's slug
MANUAL_HEADSHOTS = {
    # 'libby-shaaf': {'source': 'http://www2.oaklandnet.com/', 'image': 'manual-headshots/libby-shaaf.jpg' },
}

# notable positions that aren't district representatives, e.g. mayor & city clerk
# keys should match person slugs
EXTRA_TITLES = {
    'libby-shaaf': 'Mayor'
}

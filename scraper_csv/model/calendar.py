from scraper.model.json_model import JsonModel
from scraper.model.csv_model import CSVModel

class Calendar(JsonModel, CSVModel):
    field_names = [
        'name', 
        'meeting_date', 
        'calendar_link', 
        'meeting_time', 
        'meeting_location', 
        'meeting_details', 
        'agenda', 
        'minutes', 
        'video', 
        'eComment']    

    def __init__(self, name, meeting_date, calendar_link, 
        meeting_time, meeting_location, meeting_details, agenda, 
        minutes, video, eComment):
        super().__init__()

        self._name = name
        self.meeting_date = meeting_date
        self.calendar_link = calendar_link
        self.meeting_time = meeting_time
        self._meeting_location = meeting_location 
        self._meeting_details = meeting_details
        self.agenda = agenda
        self.minutes = minutes
        self.video = video
        self.eComment = eComment

    def filter_newlines(self, text_str):
        if text_str is None:
            return None
            
        return text_str.replace('\n', ' ')

    def remove_starting_asterisk(self, text_str):
        if text_str is None:
            return None

        if text_str.startswith('*'):
            return text_str[1:]
        else:
            return text_str    

    @property
    def name(self):
        return self.remove_starting_asterisk(self.filter_newlines(self._name))

    @name.setter
    def name(self, raw_name):
        self._name = raw_name

    @property
    def meeting_location(self):
        return self.filter_newlines(self._meeting_location)

    @meeting_location.setter
    def meeting_location (self, raw_meeting_location):
        self._meeting_location = raw_meeting_location 

    @property
    def meeting_details(self):
        return self.filter_newlines(self._meeting_details)

    @meeting_details.setter
    def meeting_details(self, raw_meeting_details):
        self._meeting_details = raw_meeting_details

    def to_map(self):
        return {
            'name': self.name, 
            'meeting_date': self.meeting_date, 
            'calendar_link': self.calendar_link, 
            'meeting_time': self.meeting_time, 
            'meeting_location': self.meeting_location, 
            'meeting_details': self.meeting_details, 
            'agenda': self.agenda, 
            'minutes': self.minutes, 
            'video': self.video, 
            'eComment': self.eComment
        }

    

        





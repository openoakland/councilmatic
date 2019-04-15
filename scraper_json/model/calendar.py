from scraper.model import ModelBase, CSVModel, JsonModel
from scraper.model.meeting_details import MeetingDetails

class Calendar(ModelBase, JsonModel, CSVModel):
    def __init__(self, name=None, meeting_date=None, calendar_link=None, 
        meeting_time=None, meeting_location=None, meeting_details=None, agenda=None, 
        minutes=None, video=None, eComment=None, cancelled=None):
        super().__init__()

        self.field_names = [
            'name', 
            'meeting_date', 
            'calendar_link', 
            'meeting_time', 
            'meeting_location', 
            'meeting_details', 
            'agenda', 
            'minutes', 
            'video', 
            'eComment',
            'cancelled']    

        self.field_class_dict = {"meeting_details": MeetingDetails}

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
        self._cancelled = cancelled

    @property
    def name(self):
        return self.remove_starting_asterisk(self.filter_newlines(self._name))

    @property
    def cancelled(self):
        if ((self.name is not None and 'CANCELLED' in self.name.upper()) or
            (self.meeting_location is not None and 'CANCELLED' in self.meeting_location.upper())):
            self._cancelled = True
        else:
            self._cancelled = False

        return self._cancelled

    @cancelled.setter
    def cancelled(self, val):
        self._cancelled = val

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
        return self._meeting_details

    @meeting_details.setter
    def meeting_details(self, raw_meeting_details):
        self._meeting_details = raw_meeting_details

    def to_map(self):
        map = super().to_map()

        if map is not None and 'meeting_details' in map and map['meeting_details'] is not None:
            map['meeting_details'] = map['meeting_details'].to_map()           

        return map

    

        





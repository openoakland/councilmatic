from scraper.model import ModelBase, CSVModel, JsonModel
from scraper.model.meeting_item import MeetingItem 

class MeetingDetails(ModelBase, JsonModel, CSVModel):
    def __init__(self, meeting_name=None, meeting_datetime=None, meeting_location=None, 
                    published_agenda=None, agenda_packet=None, meeting_video=None,
                    agenda_status=None, minutes_status=None, published_minutes=None,
                    eComment=None, additional_notes=None, meeting_items=None):
        super().__init__()

        self.field_names = [
            'meeting_name', 
            'meeting_datetime', 
            'meeting_location', 
            'published_agenda', 
            'agenda_packet', 

            'meeting_video',
            'agenda_status',
            'minutes_status',
            'published_minutes',
        
            'eComment',
            'additional_notes',
            'meeting_items'
            ]    

        self._meeting_name = meeting_name
        self.meeting_datetime = meeting_datetime
        self._meeting_location = meeting_location
        self.published_agenda = published_agenda
        self.agenda_packet = agenda_packet
        self.meeting_video = meeting_video
        self.agenda_status = agenda_status
        self.minutes_status = minutes_status
        self.published_minutes = published_minutes
        self.eComment = eComment 
        self.additional_notes = additional_notes 
        self.meeting_items = meeting_items

    @property
    def meeting_name(self):
        return self.remove_starting_asterisk(self.filter_newlines(self._meeting_name))

    @meeting_name.setter
    def meeting_name(self, raw_name):
        self._meeting_name = raw_name

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
        map = super().to_map()

        if map is not None and map.get('meeting_items', None) is not None:
            map['meeting_items'] = MeetingItem.to_map_list(map['meeting_items'])   

        return map

    

        





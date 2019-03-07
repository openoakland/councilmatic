from scraper.model import ModelBase, CSVModel, JsonModel
from scraper.model.action_details import ActionDetails

class MeetingItem(ModelBase, JsonModel, CSVModel):
    def __init__(self, file_num, file_url, version, agenda_num, meeting_item_name, meeting_type,
                  title, action, result, action_details, video):
        super().__init__()

        self.field_names = [
            "file_num", "file_url", "version", 
            "agenda_num", "meeting_type",
            "title", "action", "result", "action_details", "video"]    
        self.file_num = file_num
        self.file_url = file_url
        self.version = version

        self.agenda_num = agenda_num 
        self.meeting_item_name = meeting_item_name
        self.meeting_type = meeting_type
        self.title = title
        self.action = action 
        self.result = result 
        self.action_details = action_details
        self.video = video

    def to_map(self):
        map = super().to_map()

        if map is not None and map.get('action_details', None) is not None:
            map['action_details'] = map['action_details'].to_map() 

        return map



    

        





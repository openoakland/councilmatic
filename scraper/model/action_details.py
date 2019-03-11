from scraper.model import ModelBase, CSVModel, JsonModel
from scraper.model.vote_item import VoteItem 

class ActionDetails(ModelBase, JsonModel, CSVModel):
    def __init__(self, file_num=None, file_url=None, version=None, action_type=None, title=None, 
                mover=None, seconder=None, result=None, agenda_note=None, minute_note=None,
                action=None, action_text=None, vote_items=None):
        super().__init__()

        self.field_names = [
            "file_num", "file_url", "version", "action_type", "title", 
            "mover", "seconder", "result", "agenda_note", "minute_note",
            "action", "action_text", "vote_items"]    

        self.list_field_class_dict = {"vote_items": VoteItem}

        self.file_num = file_num
        self.file_url = file_url
        self.version = version
        self.action_type = action_type
        self.title = title 
        self.mover = mover
        self.seconder = seconder 
        self.result = result 
        self.agenda_note = agenda_note 
        self.minute_note = minute_note
        self.action = action 
        self.action_text = action_text
        self.vote_items = vote_items

    def to_map(self):
        map = super().to_map()

        if map is not None and map.get('vote_items', None) is not None:
            map['vote_items'] = VoteItem.to_map_list(map['vote_items'])   

        return map
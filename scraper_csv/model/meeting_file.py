from scraper.model.json_model import JsonModel
from scraper.model.csv_model import CSVModel

class MeetingFile(JsonModel, CSVModel):
  field_names = [
    'number', 
    'version', 
    'agenda_number', 
    'name', 
    'type', 
    'title', 
    'action', 
    'result', 
    'action_details', 
    'video',
    'link'
    ]  

  def __init__(self, number, version, agenda_number, 
    name, doc_type, title, action, 
    result, action_details, video, link):
    super().__init__()

    self.number = number
    self.version = version
    self.agenda_number = agenda_number
    self.name = name
    self.type = doc_type 
    self.title = title
    self.action = action
    self.result = result
    self.action_details = action_details
    self.video = video
    self.link = link
    

  def to_map(self):
    return {
        'number' : number,
        'version' : version,
        'agenda_number' : agenda_number,
        'name' : name,
        'type' : doc_type,
        'title' : title,
        'action' : action,
        'result' : result,
        'action_details' : action_details,
        'video' : video,
        'link' : link
    }

  

    





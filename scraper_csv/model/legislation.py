from model.json_model import JsonModel

class Legislation(JsonModel):
  def __init__(self, file_num, file_link, legislation_type, 
                                        status, file_created, 
                                        final_action, title):
    super().__init__()

    self.file_num = file_num
    self.file_link = file_link

    self.legislation_type = legislation_type

    self.status = status

    self.file_created = file_created

    self.final_action = final_action
    self.title = title

  def to_map(self):
    return {
      'file_num': self.file_num, 
      'file_link': self.file_link, 
      'legislation_type': self.legislation_type, 
      'status': self.status, 
      'file_created': self.file_created, 
      'final_action': self.final_action, 
      'title': self.title
    }


from .json_model import JsonModel

class CouncilMember(JsonModel):
  def __init__(self, name, email, website, 
                departments = {}, 
                last_member_start_date = None):
    super().__init__()

    self.name = name
    self.email = email
    self.website = website
    self.departments = departments
    self.last_member_start_date = last_member_start_date

  def to_map(self):
    return {
      'name': self.name, 
      'email': self.email, 
      'website': self.website, 
      # TODO: fix serialization for departments
      'departments': [x for x in self.departments.keys()],
      'last_member_start_date': str(self.last_member_start_date)
    }





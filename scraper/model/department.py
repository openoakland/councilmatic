from .json_model import JsonModel

# This really should be something like "Department_Membership". 
# Maybe change this later.
class Department(JsonModel):
  def __init__(self, name, title,
                member_start_date=None, member_end_date=None,
                appointed_by=None):
    self.name = name
    self.title = title
    self.member_start_date = member_start_date
    self.member_end_date = member_end_date
    self.appointed_by = appointed_by

  def to_map(self):
    return {
      'name': self.name,
      'member_start_date': self.member_start_date,
      'member_end_date': self.member_end_date,
      'appointed_by': self.appointed_by
    }

  def jsonable(self):
    return self.to_map()
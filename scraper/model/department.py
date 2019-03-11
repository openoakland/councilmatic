from scraper.model import ModelBase, CSVModel, JsonModel

# This really should be something like "Department_Membership". 
# Maybe change this later.
class Department(ModelBase, JsonModel):
    def __init__(self, name=None, title=None, member_start_date=None, 
                    member_end_date=None, appointed_by=None):
        self.defined_fields = [
            'name',
            'member_start_date',
            'member_end_date',
            'appointed_by'
        ]

        self.name = name
        self.title = title
        self.member_start_date = member_start_date
        self.member_end_date = member_end_date
        self.appointed_by = appointed_by

    """
    def to_map(self):
        return {
            'name': self.name,
            'member_start_date': self.member_start_date,
            'member_end_date': self.member_end_date,
            'appointed_by': self.appointed_by
        }
    """
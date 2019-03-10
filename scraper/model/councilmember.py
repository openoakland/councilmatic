from scraper.model import ModelBase, CSVModel, JsonModel

class CouncilMember(ModelBase, JsonModel, CSVModel):
    def __init__(self, name, email, website, 
                                departments = {}, 
                                last_member_start_date = None):
        super().__init__()

        self.field_names = [
            'name', 
            'email', 
            'website', 
            'departments', 
            'last_member_start_date']   

        self.name = name
        self.email = email
        self.website = website
        self.departments = departments
        self.last_member_start_date = last_member_start_date

    def to_map(self):
        map = super().to_map()

        map['departments'] = [x for x in map['departments'].keys()]

        if 'last_member_start_date' in map:
            map['last_member_start_date'] = str(map['last_member_start_date'])

        return map
        





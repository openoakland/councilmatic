from scraper.model import ModelBase, CSVModel, JsonModel

class VoteItem(ModelBase, JsonModel, CSVModel):
    def __init__(self, person_name, vote):
        super().__init__()

        self.field_names = ["person_name", "vote"]    

        self.person_name = person_name
        self.vote = vote
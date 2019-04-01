from scraper.model import ModelBase, CSVModel, JsonModel

class Legislation(ModelBase, JsonModel):
    def __init__(self, file_num=None, file_link=None, legislation_type=None, status=None,
                    file_created=None, final_action=None, title=None):
        super().__init__()

        self.defined_fields = [
            'file_num',
            'file_link', 
            'legislation_type', 
            'status', 
            'file_created', 
            'final_action', 
            'title'
        ]

        self.file_num = file_num
        self.file_link = file_link

        self.legislation_type = legislation_type

        self.status = status

        self.file_created = file_created

        self.final_action = final_action
        self.title = title

    """
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
        """


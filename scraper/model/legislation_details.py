from scraper.model import ModelBase, CSVModel, JsonModel

class LegislationDetails(ModelBase, JsonModel, CSVModel):
    def __init__(self, file_num=None, version=None, legislation_details_name=None,
                  legislation_detail_type=None, status=None, file_created=None,
                  in_control=None, on_agenda=None, final_action=None,
                  title=None, attachments=None, legislation_details_history=None):
        super().__init__()

        self.field_names = [
            "file_num", "version", "legislation_details_name",
            "legislation_detail_type", "status", "file_created",
            "in_control", "on_agenda", "final_action",
            "title", "attachments", "legislation_details_history"]  

        self.file_num = file_num
        self.version = version
        self.legislation_details_name = legislation_details_name
        self.legislation_detail_type = legislation_detail_type
        self.status = status
        self.file_created = file_created
        self.in_control = in_control
        self.on_agenda = on_agenda
        self.final_action = final_action
        self.title = title
        self.attachments = attachments
        self.legislation_details_history = legislation_details_history 





    

        





from abc import ABC, abstractmethod
import json

class JsonModel(object):
    def __init__(self):
        pass

    @abstractmethod
    def to_map(self):
        pass

    def to_json(self):
        #return json.dumps(self.to_map())
        return json.dumps(self, cls=PythonObjectEncoder, indent=4)

    @classmethod
    def to_map_list(cls, l):
        return [x.to_map() for x in l]

    @classmethod
    def to_map_list_json(cls, l):
        ml = JsonModel.to_map_list(l)

        return json.dumps(ml)

    
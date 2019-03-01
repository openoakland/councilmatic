from abc import ABC, abstractmethod
import json    

class ModelBase(object):
    def __init__(self):
        self.field_names = []

    def filter_newlines(self, text_str):
        if text_str is None:
            return None
            
        return text_str.replace('\n', ' ')

    def remove_starting_asterisk(self, text_str):
        if text_str is None:
            return None

        if text_str.startswith('*'):
            return text_str[1:]
        else:
            return text_str   

    def to_map(self):
        return {field_name: getattr(self, field_name) for field_name in self.field_names}

class CSVModel(object):
  def __init__(self):
    self.field_names = []

  @abstractmethod
  def to_map(self):
    pass

  def escape_double_quotes(self, text_str):
    if text_str is None:
      return None

    return text_str.replace("\"", "\\\"")    

  def to_csv_str(self):
    m = self.to_map()
    val_list = ["\"%s\"" % self.escape_double_quotes(m[x]) for x in self.field_names]
    
    return ", ".join(val_list)

  @classmethod
  def to_csv(cls, l):
    if l is None or len(l) == 0:
        return None

    field_names = l[0].field_names
    ret_str_list = [",".join(field_names)]

    for elt in l:
      ret_str_list.append(elt.to_csv_str())

    return "\n".join(ret_str_list)

class JsonModel(object):
    def __init__(self):
        pass

    @abstractmethod
    def to_map(self):
        pass

    def to_json(self):
        map = self.to_map()
        return json.dumps(map, indent=4, ensure_ascii=False)

    @classmethod
    def to_map_list(cls, l):
        return [x.to_map() for x in l]

    @classmethod
    def to_map_list_json(cls, l):
        ml = JsonModel.to_map_list(l)

        return json.dumps(ml, indent=4, ensure_ascii=False)

    
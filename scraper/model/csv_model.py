from abc import ABC, abstractmethod
import json

class CSVModel(object):
  field_names = []

  def __init__(self):
    pass

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
    ret_str_list = [",".join(cls.field_names)]

    for elt in l:
      ret_str_list.append(elt.to_csv_str())

    return "\n".join(ret_str_list)


from abc import ABC, abstractmethod
import json    
import traceback

class ModelBase(object):
    def __init__(self):
        self.field_names = []
        self.field_class_dict = {}
        self.list_field_class_dict = {}

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

    def __str__(self):
        str_list = []
        for field_name in self.field_names:
            curr_val = getattr(self, field_name)
            if field_name in self.list_field_class_dict.keys():
                str_val = self.list_field_class_dict[field_name].get_str_from_list(curr_val)
            else:
                str_val = "   %s: %s" % (field_name, curr_val.__str__())
            

            str_list.append(str_val)

        return "\n".join(str_list)

    @classmethod
    def get_str_from_list(cls, l):
        str_list = []

        if l is not None:
            for i, elt in enumerate(l):
                str_list.append("%d: %s" % (i, elt.__str__()))

        return "\n".join(str_list)


class CSVModel(object):
  def __init__(self):
    self.field_names = []
    self.field_class_dict = {}
    self.list_field_class_dict = {}

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
        self.field_class_dict = {}
        self.list_field_class_dict = {}

    @abstractmethod
    def to_map(self):
        pass

    def to_json(self):
        map = self.to_map()
        return json.dumps(map, indent=4, ensure_ascii=False)

    @classmethod
    def from_json(cls, json_elt, warn_on_err = True):
        obj = cls()

        if json_elt is not None:
            for field_name in obj.field_names:
                try:    
                    if field_name in json_elt:
                        if field_name in obj.list_field_class_dict:
                            l = json_elt[field_name]
                            subobj_list = obj.list_field_class_dict[field_name].from_list_json(l)
                            setattr(obj, field_name, subobj_list)
                        elif field_name in obj.field_class_dict:
                            subobj = obj.field_class_dict[field_name].from_json(json_elt[field_name])
                            setattr(obj, field_name, subobj)
                        else:
                            setattr(obj, field_name, json_elt[field_name])
                except Exception as e:
                    print(traceback.format_exc())
                    if not warn_on_err:
                        raise ValueError(e)

        return obj

    @classmethod
    def from_list_json(cls, l, warn_on_err = True):
        objs = []

        for i, elt in enumerate(l):
            try:
                obj = cls.from_json(elt, warn_on_err = warn_on_err)
                objs.append(obj)
            except ValueError as e:
                print(traceback.format_exc())
                if not warn_on_err:
                    raise ValueError(e)

        return objs

    @classmethod
    def to_map_list(cls, l):
        return [x.to_map() for x in l]

    @classmethod
    def to_map_list_json(cls, l):
        ml = JsonModel.to_map_list(l)

        return json.dumps(ml, indent=4, ensure_ascii=False)


    
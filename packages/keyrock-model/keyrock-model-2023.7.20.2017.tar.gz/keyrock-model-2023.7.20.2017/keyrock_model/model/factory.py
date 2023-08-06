from pydantic import parse_obj_as

class Factory():
    def __init__(self, root_type):
        self.root_type = root_type

    def get_instance(self, config):
        return parse_obj_as(self.root_type, config)

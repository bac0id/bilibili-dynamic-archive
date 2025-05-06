from .dynamic import Dynamic


class DynamicParser:
    def __init__(self, item):
        self.item = item

    def get_dynamic(self):
        id = self.get_id()
        dy = Dynamic(id=id)
        return dy


class Player:
    def __init__(self, name):
        self.name = name
        self.current_room = 0
        self.inventory = []

    def add_item(self, item):
        self.inventory.append(item)

import json


class Room:
    def __init__(self, roomId, name, description):
        self.roomId = roomId
        self.name = f"\u001b[31m{name}\u001b[0m"
        self.description = description
        self.exits = {}
        self.inventory = []
        self.hiding_places = {}

    def __str__(self):
        exits = 'Exits: ['
        for room_exit in self.exits.keys():
            exits += f" {room_exit} "
        exits += ']'
        items = ""
        for item in self.inventory:
            items += f"{item.short_desc}\n"
        return f"{self.name}\n\n{self.description}\n\n{exits}\n\n{items}"

    def toJson(self):
        return json.dumps([self.roomId, self.name, self.description])

    def add_exit(self, direction, id):
        self.exits[direction] = id

    def add_item(self, item):
        self.inventory.append(item)

    def get_item(self, args):
        item_to_find = args[1:]
        items_found = []
        for item in self.inventory:
            if any(keyword in item.keywords.split(' ') for keyword in item_to_find):
                items_found.append(item)
        return items_found

    def remove_item(self, item):
        self.inventory.remove(item)

    def add_hiding_place(self, name, hide_desc):
        self.hiding_places[name] = hide_desc

    def has_hiding_place(self, name):
        if name in self.hiding_places:
            return True
        else:
            return False

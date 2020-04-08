import json
from item import Item
from room import Room
from player import Player
from command import Command
from ansi import ansi_table

# Declare all the rooms

rooms = [
    Room(0, "A dilapidated shack", """ Roughly hewn plank walls surround you, offering little protection
from the weather and even less from the light. The floor is slotted
and speckled with the sun from the varied gaps between planks and
the holes that adorn the walls. Little furniture resides here, aside
from a single wooden table that shares the floor with a crude stool.
An oversized door, more finely made than the walls, sits to the north.
A lone window, opposite the door, breaks the monotony of the garish
walls and offers a view of a nondescript alley."""),

    Room(1, "Foyer", """Dim light filters in from the south. Dusty
passages run north and east."""),

    Room(2, "Grand Overlook", """A steep cliff appears before you, falling
into the darkness. Ahead to the north, a light flickers in
the distance, but there is no way across the chasm."""),

    Room(3, "Narrow Passage", """The narrow passage bends here from west
to north. The smell of gold permeates the air."""),

    Room(4, "Treasure Chamber", """You've found the long-lost treasure
chamber! Sadly, it has already been completely emptied by
earlier adventurers. The only exit is to the south."""),
    Room(5, "A cramped alley", """ This is an alley and it needs a better
description""")
]

items = [
    Item(0, "rusty iron key", "a rusty iron key", "~ya key of iron lies here, adorned with rust and dust.~e",
         """A large loop has been ornately fashioned at the base of this key.
        It bears the marks of years of use but the iron work and complexity
        belies the talent of its creator."""),
    Item(1, "soft leather boots", "a pair of soft leather boots", "~Xa well worn pair of leather boots rest here.~e",
         """The leather of these boots has worn soft and they barely hold a shape. The
         lances appear to be new, and they have been meticulously cleaned.""")
]


# Link rooms together

def save_rooms():
    for room in rooms:
        print(json.dumps(room.toJson()))


rooms[0].add_exit('north', 1)
rooms[0].add_exit('window', 5)
rooms[0].add_hiding_place(
    'table', "You dash under the table and hide as best you can.")
rooms[0].add_item(items[0])
rooms[0].add_item(items[1])
rooms[1].add_exit('south', 0)
rooms[1].add_exit('north', 2)
rooms[1].add_exit('east', 3)
rooms[2].add_exit('south', 1)
rooms[3].add_exit('west', 1)
rooms[3].add_exit('north', 4)
rooms[4].add_exit('south', 3)
rooms[5].add_exit('window', 0)


def show_room():
    print(parse_color(str(rooms[player.current_room])))


def bust_a_prompt():
    return parse_color("~bHealth~w: ~b5~w/~b5 ~w- ~pMana~w: ~p1~w/~p2 ~w- ~gStamina~w: ~g6~w/~g10~e >> ")


def do_move(direction):
    if direction in (rooms[player.current_room].exits):
        player.current_room = rooms[player.current_room].exits[direction]
        show_room()
    else:
        print("You cannot go that way.")


def do_look(args):
    show_room()


def do_quit(args):
    global GAME_RUNNING
    print("Goodbye!")
    GAME_RUNNING = False


def do_hide(args):
    room = rooms[player.current_room]
    if len(args) == 1:
        print("Where do you want to hide?")
    elif room.has_hiding_place(args[1]):
        print(room.hiding_places[args[1]])
    else:
        print(f"There is no {args[1]} to hide behind.")


def do_get(args):
    room = rooms[player.current_room]
    if len(args) == 1:
        print("What are you trying to get?")
    else:
        items = room.get_item(args)
        if len(items) > 1:
            print("Which one are you trying to get?")
        elif len(items) < 1:
            print(f"There is no {str(' ').join(args[1:])} here.")
        else:
            print(f"You pick up {items[0].name}")
            room.remove_item(items[0])
            player.add_item(items[0])


commands = {
    'quit': Command(do_quit),
    'look': Command(do_look),
    'hide': Command(do_hide),
    'get': Command(do_get)
}


def get_command(input, command_list):
    result = [key for key, value in command_list.items() if input ==
              key[:len(input)]]
    if len(result) >= 1:
        return result[0]
    else:
        return None


def parse_color(string):
    out = ""
    found_color = False
    for index, value in enumerate(string):
        if value == "~":
            found_color = True
            next_char = string[index+1]
            if next_char in ansi_table:
                out += f"{ansi_table[next_char]}"
            else:
                print(ansi_table[next_char])
        elif found_color == True:
            found_color = False
        else:
            out += value
    return out

#
# Main
#

# Make a new player object that is currently in the 'outside' room.


# Write a loop that:
#
# * Prints the current room name
# * Prints the current description (the textwrap module might be useful here).
# * Waits for user input and decides what to do.
#
# If the user enters a cardinal direction, attempt to move to the room there.
# Print an error message if the movement isn't allowed.
#
# If the user enters "q", quit the game.
GAME_RUNNING = True
player = Player('Test')
print("\n\n\n\n\n")
show_room()

while GAME_RUNNING == True:
    print(bust_a_prompt())
    player_input = input()
    split_input = player_input.split(' ')
    command = get_command(split_input[0], rooms[player.current_room].exits)
    if command in rooms[player.current_room].exits:
        do_move(command)
    else:
        command = get_command(split_input[0], commands)
        if command in commands:
            commands[command].function(split_input)
        else:
            print("That is not a valid command.")

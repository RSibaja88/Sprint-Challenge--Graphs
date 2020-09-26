from room import Room
from player import Player
from world import World


import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)


"""
Plan:
move player into starting room
find all possible exits for room
move in a direction and repeat this process
Plan to keep track of visited rooms/paths
Set direction for reverse as well

Based on this problem: storage space isnt an issue, getting this task accomplished quickly and as efficiently as possible is the main goal. For this, DFS(t) is most likely the ideal solution. 


MY CODE STARTING HERE!!!

"""

reverse_move = {'n': 's', 's': 'n', 'w': 'e', 'e': 'w'}


def dftr_maze(current_room, visited=None):
    # list directions while moving
    directions = []
    # creating a set to hold visited rooms if visited is none.
    if visited == None:
        visited = set()

    # finding exits for current_room using player from player and get_exits from room
    for move in player.current_room.get_exits():
        # making moves using travel from player
        player.travel(move)

        # reverse_move if already visited to find new path
        if player.current_room in visited:
            player.travel(reverse_move[move])
        # if its a new room, do the following
        else:
            # add to visited stack
            visited.add(player.current_room)
            # adding this move to 'directions'
            directions.append(move)
            # recursive : repeating loop and adding directions (sidenote, '\' is an escape character in Python.)
            directions = directions + \
                dftr_maze(player.current_room, visited)
            # go_back to previous room
            player.travel(reverse_move[move])
            # appending this move to 'directions'
            directions.append(reverse_move[move])

    return directions


# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = dftr_maze(player.current_room)
print(dftr_maze)


# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(
        f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")


#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")

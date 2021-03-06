from room import Room
from player import Player
from world import World
from visitedgraph import VisitedGraph

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
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
traversal_path = []
visited_graph = VisitedGraph()
path_back_home = []

# starting room
current = world.starting_room
visited_graph.add_room(current.id, current.get_exits())

while len(visited_graph) < len(room_graph):
    # get new direction
    newdir = visited_graph.get_unexplored_exit_for_room(current.id)
    if newdir is not None:
        # going out, so record path back
        path_back_home.append(visited_graph.invertDirection(newdir))
    else:
        # walk back up
        newdir = path_back_home.pop()
    # get the new room and connect with previous
    prev = current
    current = current.get_room_in_direction(newdir)
    visited_graph.add_room(current.id, current.get_exits())
    visited_graph.connect_rooms(prev.id, newdir, current.id)
    # record what we did
    traversal_path.append(newdir)



# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")

from functools import reduce
from typing import Tuple, List, Set

INPUT_FILE = 'input'

COORDINATE = Tuple[int, int]

with open(INPUT_FILE) as input_file:
    wires = [l.strip() for l in input_file]


def connect_wires(command: str, starting_position: COORDINATE) -> List[COORDINATE]:
    OPS = {
        'R': (1, 0),
        'L': (-1, 0),
        'U': (0, 1),
        'D': (0, -1)
    }
    op, increment = command[0], int(command[1:])

    wired_coordinates = list()
    for i in range(1, increment + 1):
        new_coordinate = (starting_position[0] + OPS[op][0] * i, starting_position[1] + OPS[op][1] * i)
        wired_coordinates.append(new_coordinate)
    return wired_coordinates


def connect_whole_wire(wire: str) -> List[COORDINATE]:
    wire_instructions = wire.split(',')
    current_position = (0, 0)
    wired_coordinates = []
    for wire_instruction in wire_instructions:
        wired_coordinates += connect_wires(wire_instruction, current_position)
        current_position = wired_coordinates[-1]

    return list(wired_coordinates)


# Helpers
def intersect_sets(a: Set[COORDINATE], b: Set[COORDINATE]) -> Set[COORDINATE]:
    return a & b


def abs_coordinate(c: COORDINATE) -> COORDINATE:
    return abs(c[0]), abs(c[1])


connected_wires = [connect_whole_wire(wire) for wire in wires]

conflicts = reduce(intersect_sets, [set(connected_wire) for connected_wire in connected_wires])

# Part 1
nearest_conflicts = sorted(conflicts, key=lambda conflict: abs(conflict[0]) + abs(conflict[1]))
nearest_conflict = nearest_conflicts[0]
print(f"Nearest conflict (Manhattan: {abs(nearest_conflict[0] + nearest_conflict[1])}) ->",
      abs_coordinate(nearest_conflict))
print()

# Part 2
faster_conflict = sorted(nearest_conflicts,
                         key=lambda conflict: sum(connected_wire.index(conflict) + 1
                                                  for connected_wire in connected_wires))[0]
steps = sum(connected_wire.index(faster_conflict) + 1 for connected_wire in connected_wires)
print(f"Nearest conflict (Steps: {steps}) ->", abs_coordinate(faster_conflict))

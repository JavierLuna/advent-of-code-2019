import math
from collections import defaultdict
from typing import Set, Dict, Optional, List, Union

INPUT_FILE = 'input'
Universe = Dict[str, Set[str]]

with open(INPUT_FILE) as input_file:
    orbits = [line.strip() for line in input_file]

directed_universe = defaultdict(set)

for orbit in orbits:
    planet1, planet2 = orbit.split(')')
    directed_universe[planet1].add(planet2)


def get_n_orbits(directed_universe: Universe, starting_node: str, visited_orbits: Optional[List[str]] = None) -> int:
    visited_orbits = visited_orbits or []
    unvisited_orbits = directed_universe[starting_node] - set(visited_orbits)

    return len(visited_orbits) + sum(get_n_orbits(directed_universe,
                                                  unvisited_orbit,
                                                  visited_orbits[:] + [starting_node])
                                     for unvisited_orbit in unvisited_orbits)


# Part 1
print("Direct and indirect orbits in universe:", get_n_orbits(directed_universe, 'COM'))


# Part 2
def shortest_path(universe: Universe, starting_node: str, target_node: str,
                  visited_orbits: Optional[List[str]] = None) -> Union[int, float]:
    visited_orbits = visited_orbits or []
    unvisited_orbits = universe[starting_node] - set(visited_orbits)
    if target_node in universe[starting_node]:
        return len(visited_orbits)
    if not unvisited_orbits:
        return math.inf
    return min(shortest_path(universe,
                             unvisited_orbit,
                             target_node,
                             visited_orbits[:] + [starting_node])
               for unvisited_orbit in unvisited_orbits)


universe = defaultdict(set)
for planet, orbits in directed_universe.items():
    for orbit in orbits:
        universe[orbit].add(planet)
    [universe[planet].add(orbit) for orbit in orbits]

print("Nº Orbital transfers between 'YOU' and 'SAN':", shortest_path(universe, 'YOU', 'SAN') - 1)

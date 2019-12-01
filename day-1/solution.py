INPUT_FILE = 'input'


with open(INPUT_FILE) as input_file:
    masses = [int(line.strip()) for line in input_file]


def get_fuel_requirement(mass: int) -> int:
    return int(mass / 3) - 2

simple_fuel_requirements = map(get_fuel_requirement, masses)

print("Part 1 solution:", sum(total_fuel_requirement))

# Calculate the fuel's needed fuel

def get_recursive_fuel_requirement(fuel_requirement: int) -> int:
    fuel_requirement = max(get_fuel_requirement(fuel_requirement), 0)

    if fuel_requirement:
        fuel_requirement += get_recursive_fuel_requirement(fuel_requirement)
    return fuel_requirement

recursive_fuel_requirements = map(get_recursive_fuel_requirement, masses)

print("Part 2 solution:", sum(recursive_fuel_requirements))

from typing import List

INPUT_FILE = 'input'

with open(INPUT_FILE) as input_file:
    lower_bound, upper_bound = [int(bound) for bound in input_file.read().split('-')]


def complies_conditions(password: int) -> bool:
    password_chars = list(str(password))
    has_double_digits = False
    prev_char = password_chars.pop(0)
    while password_chars:
        if prev_char == password_chars[0]:
            has_double_digits = True
        if prev_char > password_chars[0]:
            return False
        prev_char = password_chars.pop(0)
    return has_double_digits


def password_generator(lower_bound: int, upper_bound: int):
    current_password = lower_bound
    while current_password <= upper_bound:
        if complies_conditions(current_password):
            yield current_password
        current_password += 1


accepted_passwords = list(password_generator(lower_bound, upper_bound))

# Part 1

print("Number of possible solutions:", len(accepted_passwords))


# Part 2
def group_password(password: int) -> List[str]:
    password_chars = list(str(password))
    grouped_password = []
    last_char = password_chars.pop(0)
    group = [last_char]
    while password_chars:
        if last_char == password_chars[0]:
            group.append(password_chars[0])
        else:
            grouped_password.append(group)
            group = [password_chars[0]]
        last_char = password_chars.pop(0)
    grouped_password.append(group)
    return ["".join(i) for i in grouped_password]


def complies_second_criteria(password: int) -> bool:
    return bool(any(len(password_group) == 2 for password_group in group_password(password)))


second_accepted_passwords = [password for password in accepted_passwords if complies_second_criteria(password)]
print("Number of possible solutions (second criteria):", len(second_accepted_passwords))

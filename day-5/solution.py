import logging
from typing import List, Dict, Union, Callable, Tuple

INPUT_FILE = 'input'

Opcode = Dict[str, Union[Callable, int, bool]]


class ParameterMode:
    POSITION_MODE = "0"
    INMEDIATE_MODE = "1"


with open(INPUT_FILE) as input_file:
    instructions = input_file.read().split(',')


class HaltProgram(Exception):
    pass


def op_99():
    raise HaltProgram()


OPCODES = {
    '01': {'op': lambda a, b: a + b,
           'opcode': 1,
           'n_params': 2,
           'needs_destination': True,
           'is_jump': False},
    '02': {'op': lambda a, b: a * b,
           'opcode': 2,
           'n_params': 2,
           'needs_destination': True,
           'is_jump': False},
    '03': {'op': lambda: input().strip(),
           'opcode': 3,
           'n_params': 0,
           'needs_destination': True,
           'is_jump': False},
    '04': {'op': lambda a: print(a, end='', flush=True),
           'opcode': 4,
           'n_params': 1,
           'needs_destination': False,
           'is_jump': False},
    '05': {'op': lambda a, b: b if a else None,
           'opcode': 5,
           'n_params': 2,
           'needs_destination': False,
           'is_jump': True},
    '06': {'op': lambda a, b: b if not a else None,
           'opcode': 6,
           'n_params': 2,
           'needs_destination': False,
           'is_jump': True},
    '07': {'op': lambda a, b: int(a < b),
           'opcode': 7,
           'n_params': 2,
           'needs_destination': True,
           'is_jump': False},
    '08': {'op': lambda a, b: int(a == b),
           'opcode': 8,
           'n_params': 2,
           'needs_destination': True,
           'is_jump': False},
    '99': {'op': op_99,
           'opcode': 99,
           'n_params': 0,
           'needs_destination': False,
           'is_jump': False
           }
}


def fix_int_opcode(int_opcode: str) -> str:
    return int_opcode.rjust(2, '0')


def get_opcode(opcode: str) -> Opcode:
    return OPCODES[opcode]


def get_opcode_meta(int_opcode: str) -> Tuple[Opcode, int, str]:
    int_opcode = fix_int_opcode(int_opcode)
    opcode = get_opcode(int_opcode[-2:])
    n_parameters = opcode['n_params'] + int(opcode['needs_destination'])
    param_modes = int_opcode[:-2].rjust(n_parameters, '0')[::-1]

    return opcode, n_parameters, param_modes


class IntOpcodeMachine:

    @classmethod
    def run_program(cls, program: List[str]) -> List[str]:
        program_pointer = 0
        try:
            while 1:
                logging.debug(f"[DEBUG] Program pointer is at {program_pointer}")
                int_opcode = program[program_pointer]
                logging.debug(f"[DEBUG] Read int_opcode: {int_opcode}")
                operation, n_parameters, param_modes = get_opcode_meta(int_opcode)
                logging.debug(f"[DEBUG] Opcode meta: {operation}, {n_parameters}, {param_modes}")
                params = program[program_pointer + 1:program_pointer + 1 + n_parameters]
                params_values = cls._get_parameter_values(program, params, param_modes)
                logging.debug(f"[DEBUG] Params parsed were: {params}")

                destination = None
                if operation['needs_destination']:
                    destination = params.pop()
                    params_values.pop()

                return_value = cls._execute_op(operation, params_values)
                logging.debug(f"[DEBUG] Result was: {return_value}")

                if destination is not None:
                    logging.debug(f"[DEBUG] Storing in {destination}...")
                    program[int(destination)] = return_value

                if operation['is_jump'] and return_value != 'None':
                    program_pointer = int(return_value)
                else:
                    program_pointer += n_parameters + 1

        except HaltProgram:
            print()
        return program

    @classmethod
    def _execute_op(cls, operation: Opcode, params: List[str]) -> str:
        int_params = [int(p) for p in params]
        logging.debug(f"[DEBUG] Executing OP {operation['opcode']} with params: {params}")
        return str(operation['op'](*int_params))

    @staticmethod
    def _get_parameter_values(program: List[str], parameters: List[str], param_modes: str) -> List[str]:
        logging.debug(f"[DEBUG] Retrieving parameter values: {param_modes} -> {parameters}")
        return [program[int(param)] if param_mode == ParameterMode.POSITION_MODE else param for param, param_mode in
                zip(parameters, param_modes)]


# Part 1
# Input '1' when asked
print(IntOpcodeMachine.run_program(instructions))

# Part 2
# Input '5' when asked
print(IntOpcodeMachine.run_program(instructions))

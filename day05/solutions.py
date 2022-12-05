import re
from collections import deque
from math import ceil
from typing import Deque, List, Tuple

from aocd import get_data
from dotenv import load_dotenv


class CratesProblem():
    def __init__(self, lists:List[Deque[str]]) -> None:
        self.columns = lists

    def move(self, from_col, to_col, how_many, model='CrateMover 9000'):
        '''
        Move `how_many` boxes from `from_col` to `to_col`, using the rules of
        a specific model of crane.
        '''
        from_col = from_col - 1
        to_col = to_col - 1
        if model == 'CrateMover 9000':
            # Add and remove at the same time
            for _ in range(how_many):
                self.columns[to_col].appendleft(
                    self.columns[from_col].popleft())
        elif model == 'CrateMover 9001':
            # First add to new column
            for i in range(how_many):
                self.columns[to_col].appendleft(
                    self.columns[from_col][how_many-1-i]
                )
            # Then remove from the old column
            for _ in range(how_many):
                self.columns[from_col].popleft()
        else:
            raise NotImplementedError('Implemented crane models are CrateMover 9000 and 9001.')

    def get_last_crates(self) -> str:
        '''
        Obtain the letters of the boxes on top, in order
        '''
        return ''.join([col[0] for col in self.columns])\
            .replace('[','')\
            .replace(']','')

    def __str__(self) -> str:
        '''
        Entirely unnecessary code for printing the crates problem neatly on stdin
        '''
        indices = [0 for _ in self.columns]
        max_height = max([len(col) for col in self.columns])
        lines = []
        for y in range(max_height):
            line_to_print = ''
            for x, col in enumerate(self.columns):
                if len(col) >= max_height-y:
                    line_to_print += f'{col[indices[x]]} '
                    indices[x] += 1
                else:
                    line_to_print += ' '*4
            lines.append(line_to_print)
        lines.append(' '.join([f' {str(i+1)} ' for i in range(len(self.columns))]))
        return '\n'.join(lines)


def process_input(lines:List[str]) -> Tuple[CratesProblem, List[str]]:
    crates_columns = ceil(len(lines[0])/4)  # "[X] " + last element does not have a space, so we use ceil
    columns = [deque([]) for _ in range(crates_columns)]    # This list will contain all of our columns
    for i, line in enumerate(lines):
        if line == '':
            # Start to parse instruction lines
            instruction_lines = lines[i+1:]
            break
        elif all([str(i+1) in line for i in range(crates_columns)]):
            # Last line of crates input contains all numbers (1...crates_columns): skip it
            continue
        else:
            # Parse the boxes from the line
            boxes = [line[(4*i):(4*i)+4].rstrip() for i in range(crates_columns)]
            for col in range(len(columns)):
                # The space may be empty
                if boxes[col] != '':
                    columns[col].append(boxes[col])
    crates_problem = CratesProblem(columns)
    return crates_problem, instruction_lines


def exec_instruction(problem:CratesProblem, instruction:str, model='CrateMover 9000'):
    # Use regex to obtain the parameters for the move function from the text
    m = re.match(r'move (?P<how_many>\d+) from (?P<from_col>\d+) to (?P<to_col>\d+)',
                instruction)
    params = {k: int(val) for k, val in m.groupdict().items()}
    problem.move(**params, model=model)


if __name__ == '__main__':
    load_dotenv()
    lines = get_data(day=5, year=2022).splitlines()
    # Problem #1
    crates, instructions = process_input(lines)
    for inst in instructions:
        exec_instruction(crates, inst)
    print(crates)
    print(f"The highest crates are {crates.get_last_crates()}")
    print("==========")
    # Problem #2
    crates, instructions = process_input(lines)
    for inst in instructions:
        exec_instruction(crates, inst, model='CrateMover 9000')
    print(crates)
    print(f"The highest crates are {crates.get_last_crates()}")
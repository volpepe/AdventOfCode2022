import operator
import re
from collections import deque
from math import floor, lcm
from typing import Callable, List

from aocd import get_data
from dotenv import load_dotenv

class MonkeyGroup():
    def __init__(self) -> None:
        self.monkeys = []
        self.round = 0

    def register_monkey(self, monkey):
        self.monkeys.append(monkey)
    
    def throw(self, item, to):
        for monkey in self.monkeys:
            if monkey.id == to:
                monkey.receive(item)
    
    def make_round(self, use_calm:bool=True):
        self.round += 1
        for monkey in self.monkeys:
            monkey.make_turn(use_calm)


class Monkey():
    def __init__(self, id:int, starting_items:List, operation:Callable, 
                 operation_el1:str, operation_el2:str, test_val:int, 
                 true_val:int, false_val:int, manager:MonkeyGroup) -> None:
        self.id = id
        self.items = deque(starting_items)
        self.manager = manager
        self.inspected_items = 0
        self.operation_el1 = operation_el1
        self.operation_el2 = operation_el2
        self.op = operation
        self.test_val = test_val
        self.true_val = true_val
        self.false_val = false_val

    def set_lcm(self, lcm:int):
        self.lcm = lcm

    def compute_new_worry_level(self, worry: int, modular=False):
        if modular:
            # We use modular arithmetic to reduce the worry levels
            # https://www.khanacademy.org/computing/computer-science/cryptography/modarithmetic/a/modular-addition-and-subtraction
            # and 
            # https://www.khanacademy.org/computing/computer-science/cryptography/modarithmetic/a/modular-multiplication
            # show that we just need to take the modulo of the components and the results of the operation
            return self.op(
                (worry if self.operation_el1 == 'old' else int(self.operation_el1)) % self.lcm,
                (worry if self.operation_el2 == 'old' else int(self.operation_el2)) % self.lcm) % self.lcm
        else:
            return self.op(
                (worry if self.operation_el1 == 'old' else int(self.operation_el1)), 
                (worry if self.operation_el2 == 'old' else int(self.operation_el2)))

    def test(self, worry: int):
        return self.true_val if (worry % self.test_val) == 0 else self.false_val

    def receive(self, item):
        self.items.append(item)
    
    def make_turn(self, use_calm:bool=True, verbose=False):
        num_items = len(self.items)
        for _ in range(num_items):
            # Take item removing it from queue
            item = self.items.popleft()
            self.inspected_items += 1
            if use_calm:
                # Compute new worry level according to operation
                new_worry_level = self.compute_new_worry_level(item, modular=False)
                # Divide by 3
                new_worry_level = floor(new_worry_level / 3)
            else:
                new_worry_level = self.compute_new_worry_level(item, modular=True)
            # Compute who to throw the item to based on test
            throw_to_id = self.test(new_worry_level)
            # Use manager to throw item to other monkeys
            self.manager.throw(new_worry_level, throw_to_id)
            if verbose:
                print(f"Monkey {self.id} inspects item with worry level {item}")
                print(f"  New worry level is {new_worry_level}")
                print(f"  The item is thrown to monkey {throw_to_id}")


def parse_input(lines:List[str]) -> MonkeyGroup:
    monkey_group = MonkeyGroup()
    current_monkey = {}

    monkey_regex = re.compile(r'Monkey (\d+):')
    items_match_regex = re.compile(r'  Starting items:( (\d+),?)+')
    items_regex  = re.compile(r' (\d+),?')
    op_regex     = re.compile(r'  Operation: new = (?P<el1>old|\d+) (?P<sign>.) (?P<el2>old|\d+)')
    op_lookup    = {'+': operator.add, '-': operator.sub, '*': operator.mul, '/': operator.truediv}
    test_regex   = re.compile(r'  Test: divisible by (\d+)')
    true_regex   = re.compile(r'    If true: throw to monkey (\d+)')
    false_regex  = re.compile(r'    If false: throw to monkey (\d+)')

    test_vals = []

    for line in lines:
        if monkey_regex.match(line):
            current_id = int(monkey_regex.match(line).group(1))
            current_monkey['id'] = current_id
        if items_match_regex.match(line):
            current_monkey['starting_items'] = [int(x) for x in items_regex.findall(line)]
        if op_regex.match(line):
            op_dict = op_regex.match(line).groupdict()
            current_monkey['operation'] = op_lookup[op_dict['sign']]
            current_monkey['operation_el1'] = op_dict['el1']
            current_monkey['operation_el2'] = op_dict['el2']
        if test_regex.match(line):
            current_monkey['test_val']  = int(test_regex.match(line).group(1))
            test_vals.append(current_monkey['test_val'])
        if true_regex.match(line):
            current_monkey['true_val']  = int(true_regex.match(line).group(1))
        if false_regex.match(line):
            current_monkey['false_val'] = int(false_regex.match(line).group(1))
            # Once the false regex is found the monkey can be finalised and inserted into the manager
            monkey_group.register_monkey(Monkey(**current_monkey, manager=monkey_group))

    for monkey in monkey_group.monkeys:
        # We need to set a common lcm to all monkeys for modulo operations
        monkey.set_lcm(lcm(*test_vals))

    return monkey_group


def run_simulation(monkey_group: MonkeyGroup, rounds:int, use_calm:bool=True) -> List[int]:
    for _ in range(rounds):
        monkey_group.make_round(use_calm)


if __name__ == '__main__':
    load_dotenv()
    lines = get_data(day=11, year=2022).splitlines()

    # Problem 1
    monkey_group = parse_input(lines)
    run_simulation(monkey_group, 20, use_calm=True)
    inspected_items = []
    for monkey in monkey_group.monkeys:
        inspected_items.append(monkey.inspected_items)
    inspected_items = sorted(inspected_items)
    print(f"The level of monkey business is: {inspected_items[-1]*inspected_items[-2]}")

    # Problem 2
    monkey_group = parse_input(lines)
    run_simulation(monkey_group, 10000, use_calm=False)
    inspected_items = []
    for monkey in monkey_group.monkeys:
        inspected_items.append(monkey.inspected_items)
    inspected_items = sorted(inspected_items)
    print(f"The level of monkey business is: {inspected_items[-1]*inspected_items[-2]}")

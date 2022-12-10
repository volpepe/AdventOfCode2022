from typing import List, Set
from enum import Enum

from aocd import get_data
from dotenv import load_dotenv


class Op(str, Enum):
    NOOP = 'noop'
    ADDX = 'addx'


class CPU():
    def __init__(self, interesting_ticks:Set) -> None:
        self.X = 1
        self.clock = 0
        self.interesting_ticks = interesting_ticks
        self.signal_strengths = []
        self.screen = Screen(40, 6, 3)

    def tick(self):
        # Update screen
        self.screen.update_screen(self.clock, self.X)
        # Increase clock count
        self.clock += 1
        # Check if time for logging
        if self.clock in self.interesting_ticks:
            self.signal_strengths.append(self.clock * self.X)
    
    def exec_op(self, op:Op, param=None):
        if op == Op.NOOP:
            self.tick()
        elif op == Op.ADDX:
            self.tick()
            self.tick()
            self.X += param


class Screen():
    def __init__(self, width:int=40, height:int=6, sprite_size:int=3) -> None:
        self.width = width
        self.height = height
        self.sprite_width = sprite_size
        self.sprite_pad = (self.sprite_width - 1) / 2
        self.pixels = [
            [None for _ in range(self.width)] 
            for _ in range(self.height)
        ]

    def tick_to_coord(self, tick:int):
        # Return row, column
        return (tick // self.width, tick % self.width)

    def update_screen(self, tick:int, sprite_pos:int):
        # Note: remember to update screen before updating tick count, so it starts
        # from 0
        y, x = self.tick_to_coord(tick)
        if (sprite_pos - self.sprite_pad) <= x <= (sprite_pos + self.sprite_pad):
            self.pixels[y][x] = '#'
        else:
            self.pixels[y][x] = '.'

    def __str__(self) -> str:
        return '\n'.join([''.join(row) for row in self.pixels])


def instruction_generator(lines:List[str]):
    for line in lines:
        elems = line.split(' ')
        if len(elems) > 1:
            yield {'op': elems[0], 'param': int(elems[1])}
        else:
            yield {'op': elems[0], 'param': None}


if __name__ == '__main__':
    load_dotenv()
    lines = get_data(day=10, year=2022).splitlines()
    instructions = list(instruction_generator(lines))

    # Problem 1
    interesting_ticks = list(range(20, 220+1, 40))
    cpu = CPU(set(interesting_ticks))
    for inst in instructions:
        cpu.exec_op(**inst)
    print(f"Signal strengths at ticks {interesting_ticks}: {cpu.signal_strengths}")
    print(f"Their sum is: {sum(cpu.signal_strengths)}")

    # Problem 2
    print(f"The following image is what is show on the display of "
          f"the device at the end of execution:")
    print(str(cpu.screen))


from enum import Enum
from typing import List

from aocd import get_data
from dotenv import load_dotenv

class Direction(str, Enum):
    RIGHT = 'R'
    LEFT  = 'L'
    DOWN  = 'D'
    UP    = 'U'


class Node():
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
        self.visited_positions = set((x,y))
    
    def move(self, direction:Direction, final:bool=True):
        match direction:
            case Direction.RIGHT:
                self.x += 1
            case Direction.LEFT:
                self.x -= 1
            case Direction.UP:
                self.y += 1
            case Direction.DOWN:
                self.y -= 1
        if final:
            self.visited_positions.add((self.x, self.y))

    def is_adjacent(self, connected_node):
        return abs(self.x - connected_node.x) <= 1 and \
               abs(self.y - connected_node.y) <= 1

    def on_same_row(self, connected_node):
        return connected_node.y == self.y
    
    def on_same_column(self, connected_node):
        return connected_node.x == self.x


class Rope():
    def __init__(self, nodes=2) -> None:
        self.nodes = [Node(0,0) for _ in range(nodes)]

    def run_instructions_on_simulation(self, instructions:List):
        for inst in instructions:
            for _ in range(inst['repeat']):
                self.nodes[0].move(inst['direction'])
                self.correct_other_nodes()

    def correct_other_nodes(self):
        for i in range(1, len(self.nodes)):
            # Node must follow its connected node
            node, connected_node = self.nodes[i], self.nodes[i-1]
            # We don't need correction if node and connected node are adjacent
            if not node.is_adjacent(connected_node):
                diff_x = connected_node.x - node.x
                diff_y = connected_node.y - node.y
                if not node.on_same_column(connected_node) and \
                   not node.on_same_row(connected_node):
                    node.move(Direction.RIGHT if diff_x > 0 else Direction.LEFT, final=False)
                    node.move(Direction.UP    if diff_y > 0 else Direction.DOWN)
                elif node.on_same_column(connected_node):
                    node.move(Direction.UP    if diff_y > 0 else Direction.DOWN)
                elif node.on_same_row(connected_node):
                    node.move(Direction.RIGHT if diff_x > 0 else Direction.LEFT)

    def __str__(self) -> str:
        resolution  = max([max([abs(n.x) for n in self.nodes]), 
                           max([abs(n.y) for n in self.nodes])]) + 1
        grid        = [['.' for _ in range(resolution*2)] for _ in range(resolution*2)]
        grid[resolution][resolution]  = 's'
        for i, node in enumerate(self.nodes[1:-1]):
            grid[node.y+resolution][node.x+resolution] = f'{i+1}'
        grid[self.nodes[0 ].y+resolution][self.nodes[0 ].x+resolution] = 'H'
        grid[self.nodes[-1].y+resolution][self.nodes[-1].x+resolution] = 'T'
        return '\n'.join(["".join(g) for g in grid])
    

def parse_instructions(lines:List[str]):
    instructions = []
    for line in lines:
        direction, how_many = line.split(' ')
        instructions.append({'direction': direction,
                             'repeat':    int(how_many)})
    return instructions
        
if __name__ == '__main__':
    load_dotenv()
    lines = get_data(day=9, year=2022).splitlines()
    instructions = parse_instructions(lines)

    # Problem 1
    rope = Rope(nodes=2)
    rope.run_instructions_on_simulation(instructions)
    print(f"The tail has visited {len(rope.nodes[-1].visited_positions)} positions.")

    # Problem 2
    rope = Rope(nodes=10)
    rope.run_instructions_on_simulation(instructions)
    print(f"The tail of the longer rope has visited {len(rope.nodes[-1].visited_positions)} positions.")
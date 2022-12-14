import re
from enum import Enum
from typing import List, Tuple

import numpy as np
from aocd import get_data
from dotenv import load_dotenv


class Tile(Enum):
    AIR         = 0
    ROCK        = 1
    SAND        = 2
    SAND_ORIGIN = 3

tile_char_map = {
    Tile.AIR: '.',
    Tile.ROCK: '#',
    Tile.SAND: 'o',
    Tile.SAND_ORIGIN: '+'
}

class Cave():
    def __init__(self, lines:List[str], with_floor:bool=False, 
                       check_void:bool=True, check_origin:bool=False) -> None:
        xy_reg = re.compile(r'(\d+),(\d+)')
        # Create grid
        xs = np.array([int(m[0]) for line in lines for m in xy_reg.findall(line)])
        ys = np.array([int(m[1]) for line in lines for m in xy_reg.findall(line)])
        min_x = xs.min() - (200 if with_floor else 0)
        max_x = xs.max() + (200 if with_floor else 0)
        max_y = ys.max() + (2 if with_floor else 0)
        self.grid = np.zeros((max_y+1, max_x-min_x+1), dtype=np.int8)
        self.grid_height = self.grid.shape[0]
        self.grid_width  = self.grid.shape[1]
        # Fill with rocks and origin
        self.start_pos = (0, 500-min_x)
        self.grid[self.start_pos] = Tile.SAND_ORIGIN.value
        for line in lines:
            line_xs = np.array([int(m[0]) for m in xy_reg.findall(line)])
            line_ys = np.array([int(m[1]) for m in xy_reg.findall(line)])
            for i in range(1, len(line_xs)):
                x1, x2, y1, y2 = line_xs[i-1], line_xs[i], line_ys[i-1], line_ys[i]
                if x1 == x2:
                    greater_y, smaller_y = max(y1, y2), min(y1, y2)
                    self.grid[smaller_y:greater_y+1, x1-min_x] = Tile.ROCK.value
                elif y1 == y2:
                    greater_x, smaller_x = max(x1, x2)-min_x, min(x1, x2)-min_x, 
                    self.grid[y1, smaller_x:greater_x+1] = Tile.ROCK.value
        if with_floor:
            self.grid[-1] = np.array([Tile.ROCK.value]*self.grid_width)
        self.check_void = check_void
        self.check_origin = check_origin
        self.resting_sand_blocks = 0

    def is_occupied(self, x, y):
        return self.grid[y,x] != Tile.AIR.value and self.grid[y,x] != Tile.SAND_ORIGIN.value

    def is_out_of_bounds(self, x, y):
        return x >= self.grid_width or y >= self.grid_height

    def place_sand_block_at(self, x, y):
        self.grid[y, x] = Tile.SAND.value
        self.resting_sand_blocks += 1

    def produce_sand_block(self):
        y, x = self.start_pos
        while True:
            # Try to go down:
            if not self.is_out_of_bounds(x,y+1) and not self.is_occupied(x, y+1):
                y = y+1; x = x
            # Try to go diagonally down-left
            elif not self.is_out_of_bounds(x-1,y+1) and not self.is_occupied(x-1, y+1):
                y = y+1; x = x-1
            # Try to go diagonally down-right
            elif not self.is_out_of_bounds(x+1,y+1) and not self.is_occupied(x+1, y+1):
                y = y+1; x = x+1
            else:
                if self.check_void:
                    # Check if the sand is going to the void
                    if y == self.grid_height-1:
                        return False
                    # Or if it is just normally stopping
                    else:
                        self.place_sand_block_at(x, y)
                        return True
                elif self.check_origin:
                    # Place the block and if it is at the origin return False
                    self.place_sand_block_at(x, y)
                    return not (y, x) == self.start_pos


    def __str__(self) -> str:
        with np.printoptions(threshold=np.inf, linewidth=np.inf):
            grid_str = str(self.grid)
        for tile in Tile:
            grid_str = grid_str.replace(str(tile.value), tile_char_map[tile])
        return grid_str


if __name__ == '__main__':
    load_dotenv()
    lines = get_data(year=2022, day=14).splitlines()
    
    # Problem 1
    print("Creating cave...")
    c = Cave(lines, with_floor=False, check_void=True, check_origin=False)
    print("Simulating sand blocks...")
    while c.produce_sand_block(): pass
    print(f"{c.resting_sand_blocks} sand blocks have rested before the sand started "
          "dropping into the void.")
    print("Saving map on file map_1.txt...")
    with open('day14/map_1.txt', 'w') as f:
        f.writelines(str(c))

    print()

    # Problem 2
    print("Creating cave...")
    c = Cave(lines, with_floor=True, check_void=False, check_origin=True)
    print("Simulating sand blocks...")
    i = 0
    while c.produce_sand_block(): pass
    print(f"{c.resting_sand_blocks} sand blocks have rested before the sand obstructed "
          "the origin.")
    print("Saving map on file map_2.txt...")
    with open('day14/map_2.txt', 'w') as f:
        f.writelines(str(c))

from typing import List, Tuple
import numpy as np

from aocd import get_data
from dotenv import load_dotenv


def create_grid(lines:List[str]) -> np.ndarray:
    grid = np.empty((len(lines[0]), len(lines[0])), dtype=np.int32)
    for i, line in enumerate(lines):
        row = [int(x) for x in list(line)]    # From string to List of ints
        grid[i] = np.asarray(row, dtype=np.int32)
    return grid  


def middle_grid_iterator(h_size:int, w_size:int):
    for y in range(1, h_size-1):
        for x in range(1, w_size-1):
            yield (y, x)


def is_visible(tree_index:Tuple[int, int], grid:np.ndarray):
    y, x = tree_index
    grid_height, grid_width = np.shape(grid)
    tree_val = grid[y,x]
    return (
        # Left
        all([grid[y, i] < tree_val for i in range(x)]) or 
        # Right
        all([grid[y, i] < tree_val for i in range(x+1, grid_width)]) or
        # Top
        all([grid[i, x] < tree_val for i in range(y)]) or
        # Bottom
        all([grid[i, x] < tree_val for i in range(y+1, grid_height)])
    )


def count_visible_trees(grid:np.ndarray) -> int:
    # Starting point is the sum of the two sides of the grid * 2
    # 4 because the angles are not to be repeated in the count
    # (all trees in the border are visible)
    h_size, w_size = np.shape(grid)[0], np.shape(grid)[1]
    visible_trees = ((w_size + h_size) * 2) - 4
    for tree_index in middle_grid_iterator(h_size, w_size):
        if is_visible(tree_index, grid):
            visible_trees += 1
    return visible_trees


def compute_scenic_score(tree_index:Tuple[int, int], grid:np.ndarray):
    y, x = tree_index
    tree_val = grid[y,x]
    h_size, w_size = np.shape(grid)[0], np.shape(grid)[1]
    scores = {'left': 0, 'right': 0, 'bottom': 0, 'top': 0}
    # Look up
    temp_y = y - 1
    while temp_y >= 0:
        scores['top'] += 1
        if grid[temp_y, x] < tree_val: temp_y -= 1     # Go on
        else: break         # That's the maximum number of trees that can be seen
    # Look down
    temp_y = y + 1
    while temp_y < h_size:
        scores['bottom'] += 1
        if grid[temp_y, x] < tree_val: temp_y += 1
        else: break
    # Look left
    temp_x = x - 1
    while temp_x >= 0:
        scores['left'] += 1
        if grid[y, temp_x] < tree_val: temp_x -= 1
        else: break
    # Look right
    temp_x = x + 1
    while temp_x < w_size:
        scores['right'] += 1
        if grid[y, temp_x] < tree_val: temp_x += 1
        else: break
    return scores['left'] * scores['right'] * scores['bottom'] * scores['top']
    

def get_best_scenic_score(grid:np.ndarray):
    h_size, w_size = np.shape(grid)[0], np.shape(grid)[1]
    best_scenic_score = 0
    best_index = (0,0)
    for tree_index in middle_grid_iterator(h_size, w_size):
        score = compute_scenic_score(tree_index, grid)
        if score > best_scenic_score:
            best_scenic_score = score
            best_index = tree_index
    return best_scenic_score, best_index


if __name__ == '__main__':
    load_dotenv()
    lines = get_data(day=8, year=2022).splitlines()
    grid = create_grid(lines)

    # Problem 1
    visible_trees = count_visible_trees(grid)
    print(f"There are {visible_trees} visible trees in the map")

    # Problem 2
    best_scenic_score, best_index = get_best_scenic_score(grid)
    print(f"The best scenic score ({best_scenic_score}) is at {best_index}")
    

    
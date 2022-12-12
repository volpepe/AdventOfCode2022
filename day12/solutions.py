from typing import Dict, List, Tuple
import numpy as np
from queue import Queue
from aocd import get_data
from dotenv import load_dotenv

def can_move_at(y, x, from_y, from_x, grid):
    # We are from end to start, so we need to check that between a node and its following
    # node there is a height difference of no more than 1.
    return y >= 0 and x >= 0 and y < np.shape(grid)[0] and x < np.shape(grid)[1] and \
            grid[y, x] - grid[from_y, from_x] >= -1


def shortest_path_to_E(grid:np.ndarray, S_pos:Tuple[int,int]|str, E_pos:Tuple[int,int]):
    # We use Djikstra's algorithm to find the shortest path from the starting position
    # to the end position, considering the grid as a graph.
    # 1) Nodes are positions in the graph
    # 2) Each weight is actually just 1
    # 3) We check whether the following node can be explored from the current one using the grid
    #    and the constraints on heights. In this way we can block exploration through some paths.
    # 4) It's actually better to start from the end node and reach the start node(s), because 
    #    Djikstra supports finding the minimum distance from ONE node to ANY other node, so 
    #    in this way we can account for multiple start nodes, as the case of problem 2)
    distances = np.ones_like(grid) * np.inf     # Currently known minimum distance from source for each weight
    distances[E_pos] = 0                        # The only known distance is the source distance (0)
    previous_mapping = {}                       # Keep a map of the previous nodes for each node
    Q = set([(i,j) for i in range(np.shape(grid)[0])    # Q is the set of unvisited nodes
                   for j in range(np.shape(grid)[1])])
    if S_pos == 'any_a':
        S_pos = set([])
        ys, xs = np.where(grid == 0)
        for y,x in zip(ys, xs):
            S_pos.add((y,x))
    # Stopping condition: when we visit S_pos (or all positions) 
    # we know that we would have found the shortest path to it (or them)
    while len(Q) > 0 and (S_pos in Q if isinstance(S_pos, tuple) else True):
        # Get node with shortest known path from the set of unvisited nodes
        u = min(Q, key = lambda x: distances[x])
        x, y = u[0], u[1]
        # Remove it from Q (it's being visited)
        Q.remove(u)
        # Check each neighbour of u still in Q to which we can move
        for neighbour in [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]:
            if can_move_at(neighbour[0], neighbour[1], x, y, grid) and \
                neighbour in Q:
                # The distance is simply the previous distance + 1 if we can move there
                temp_dist = distances[u] + 1
                # Then we compare this distance with the previously known distance for that node
                if temp_dist < distances[neighbour]:
                    distances[neighbour] = temp_dist
                    previous_mapping[neighbour] = u

    return previous_mapping


def collect_path(previous_mappings:Dict, start:Tuple[int,int], end:Tuple[int,int]):
    path = [start]
    current_pos = start
    while current_pos != end:
        try:
            current_pos = previous_mappings[current_pos]
        except:
            # Some 'a's are inaccessible
            return None
        path.append(current_pos)
    return path

def get_shortest_path(previous_mappings:Dict, start:Tuple[int,int]|str, end:Tuple[int,int]):
    if start == 'any_a':
        shortest_path_len = 1e10
        shortest_path = []
        start_set = set([])
        ys, xs = np.where(grid == 0)
        for y,x in zip(ys, xs):
            start_set.add((y,x))
        for s in start_set:
            path = collect_path(previous_mappings, s, end)
            if path is not None and len(path) < shortest_path_len:
                shortest_path_len = len(path)
                shortest_path = path
    else:
        shortest_path = collect_path(previous_mappings, start, end)
    return shortest_path


def parse_input(lines:List[str]):
    grid = np.empty((len(lines), len(lines[0])))
    S_pos = (0,0)
    E_pos = (0,0)
    for i, line in enumerate(lines):
        line_to_append = np.empty(len(line))
        for j, chara in enumerate(line):
            if chara == 'S':
                line_to_append[j] = ord('a') - 97
                S_pos = (i, j)
            elif chara == 'E':
                line_to_append[j] = ord('z') - 97
                E_pos = (i, j)
            else:
                line_to_append[j] = ord(chara) - 97
        grid[i] = line_to_append
    return grid, S_pos, E_pos 


if __name__ == '__main__':
    load_dotenv()
    lines = get_data(day=12, year=2022).splitlines()
    grid, S_pos, E_pos = parse_input(lines)

    # Problem 1
    previous_mappings = shortest_path_to_E(grid, S_pos, E_pos)
    shortest_path = get_shortest_path(previous_mappings, S_pos, E_pos)
    print(f"The shortest path to the end starting from 'S' is: {len(shortest_path) - 1}")

    # Problem 2
    previous_mappings = shortest_path_to_E(grid, 'any_a', E_pos)
    shortest_path = get_shortest_path(previous_mappings, 'any_a', E_pos)
    print(f"The shortest path to the end starting from any 'a' is: {len(shortest_path) - 1}")

from typing import Set, Tuple

from aocd import get_data
from dotenv import load_dotenv

def get_tuple_of_assignments(pair_assignment:str) -> str:
    return pair_assignment.split(',')

def get_set_of_ids(assignment:str) -> Set:
    id_range_limits = [int(x) for x in assignment.split('-')]
    id_set = set(range(id_range_limits[0], id_range_limits[1]+1))
    return id_set

def get_sets_of_assignments(pair_assignment:str) -> Tuple[Set, Set]:
    assignments = get_tuple_of_assignments(pair_assignment)
    return get_set_of_ids(assignments[0]),  get_set_of_ids(assignments[1])

def check_if_one_is_subset_of_other(pair_assignment:str) -> bool:
    id_set_A, id_set_B = get_sets_of_assignments(pair_assignment)
    return id_set_A.issubset(id_set_B) or id_set_B.issubset(id_set_A)

def check_for_overlaps(pair_assignment:str) -> bool:
    id_set_A, id_set_B = get_sets_of_assignments(pair_assignment)
    return len(id_set_A.intersection(id_set_B)) > 0

if __name__ == '__main__':
    load_dotenv()
    lines = get_data(day=4, year=2022).splitlines()
    # Problem #1
    is_pair_full_overlap = [int(check_if_one_is_subset_of_other(pair_ass)) for pair_ass in lines]
    print(f"Pairs where there is a total overlap are {sum(is_pair_full_overlap)}.")
    # Problem #2
    is_pair_partial_overlap = [int(check_for_overlaps(pair_ass)) for pair_ass in lines]
    print(f"Pairs where there is a partial or total overlap are {sum(is_pair_partial_overlap)}")

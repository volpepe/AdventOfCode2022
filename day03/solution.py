from math import floor
from typing import Tuple, Set

from aocd import get_data
from dotenv import load_dotenv

def get_duplicates(*sets) -> Set:
    inter_set = set(sets[0])
    for other_set in sets[1:]:
        inter_set = inter_set.intersection(set(other_set))
    return inter_set

def split_rucksack_compartments(rucksack:str) -> Tuple[str, str]:
    rucksack_capacity = len(rucksack)
    split_point = floor(rucksack_capacity/2)
    return rucksack[:split_point], rucksack[split_point:]

def get_character_score(char:str) -> int:
    # Get the ASCII value of the char
    unicode_val = ord(char)
    # a-z are 97 to 122, so we remove 96 from the ASCII code.
    # A-Z are 65 to 90, so we remove 65 from the ASCII code.
    # Additionally, for A-Z we add 27 because the scores start from there.
    baseline = 96 if char.islower() else (65-27)
    return unicode_val - baseline

def groups_iterator(lines, group_size=3):
    it = range(0, len(lines), group_size)
    for i in it:
        yield lines[i:i+group_size]

if __name__ == '__main__':
    load_dotenv()
    lines = get_data(day=3, year=2022).splitlines()
    # Problem #1
    scores = [
        get_character_score(
            get_duplicates(*
                split_rucksack_compartments(line)
            ).pop()
        ) for line in lines
    ]
    print(f"Score of duplicate elements: {sum(scores)}")
    # Problem #2
    scores = [
        get_character_score(
            get_duplicates(*group).pop()
        )
        for group in groups_iterator(lines)
    ]
    print(f"Score of group keys: {sum(scores)}")


    
    
    
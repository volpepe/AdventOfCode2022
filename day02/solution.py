import os
from enum import Enum
from typing import List, Tuple

from aocd import get_data
from dotenv import load_dotenv

class Results(Enum):
    WIN  = 6
    LOSS = 0
    DRAW = 3

class RPS(Enum):
    ROCK     = 1
    PAPER    = 2
    SCISSORS = 3

def get_points_for_choice(choice: RPS) -> int:
    return choice.value

def get_points_for_result(result: Results) -> int:
    return result.value

def get_counter_rps(rps:RPS) -> RPS:
    if rps == RPS.ROCK:
        return RPS.PAPER
    elif rps == RPS.PAPER:
        return RPS.SCISSORS
    else:
        return RPS.ROCK

def map_elements_to_rps(elem:str) -> RPS:
    if elem == 'A' or elem == 'X':
        return RPS.ROCK
    elif elem == 'B' or elem == 'Y':
        return RPS.PAPER
    elif elem == 'C' or elem == 'Z':
        return RPS.SCISSORS
    else:
        raise NotImplementedError

def map_prob2_tuples_to_rps(tup:Tuple[str, str]) -> Tuple[RPS, RPS]:
    enemy_choice = map_elements_to_rps(tup[0])
    if tup[1] == 'Y':
        # Draw
        # Map the first element to RPS and repeat it
        return (enemy_choice, enemy_choice)
    if tup[1] == 'Z':
        # Win
        return (enemy_choice, get_counter_rps(enemy_choice))
    else:
        # Lose! Which is the counter move to the counter move.
        return (enemy_choice, get_counter_rps(get_counter_rps(enemy_choice)))

def get_winner(choiceA: RPS, choiceB: RPS) -> Results:
    if choiceA == choiceB:
        return Results.DRAW
    if choiceA == get_counter_rps(choiceB): 
        # If our character chooses a type that counters the choice
        # of the adversary, it's a win
        return Results.WIN
    else:
        return Results.LOSS

def get_total_points(ruleset:List):
    winners        = [get_winner(line[1], line[0]) for line in ruleset]
    results_points = list(map(get_points_for_result, winners))
    choices_points = [get_points_for_choice(line[1]) for line in ruleset]
    return sum(results_points) + sum(choices_points)

if __name__ == '__main__':
    load_dotenv()
    lines = get_data(day=2, year=2022).splitlines()
    # Problem #1
    prob1_ruleset = [list(map(map_elements_to_rps, line.split(' '))) for line in lines]
    print(f"Total points if we consider rules as in problem 1: {get_total_points(prob1_ruleset)}")
    # Problem #2
    prob2_ruleset = list(map(map_prob2_tuples_to_rps, [line.split(' ') for line in lines]))
    print(f"Total points if we consider rules as in problem 1: {get_total_points(prob2_ruleset)}")
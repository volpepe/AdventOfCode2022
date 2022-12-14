import re
import functools
from typing import List, Tuple

from aocd import get_data
from dotenv import load_dotenv


def compare(pair:Tuple):
    l, r = pair
    if isinstance(l, int) and isinstance(r, int):
        return l < r   # Order: left should be less or equal than right
    elif isinstance(l, int) and isinstance(r, list):
        return compare(([l], r))  # Make lists out of single elements
    elif isinstance(l, list) and isinstance(r, int):
        return compare((l, [r]))  # Make lists out of single elements
    elif isinstance(l, list) and isinstance(r, list):
        # Iterate over the elements of l
        for i in range(len(l)):
            try:
                if l[i] == r[i]:    # If elements are equal, move to the next
                    continue
                else:
                    # Check if left is less than right or if it's undefined.
                    cmp = compare((l[i], r[i]))
                    if cmp is None:
                        continue
                    else:
                        return cmp
            except IndexError:
                # It means that r has less elements than l, so the elements are not in order
                return False
        # If we managed to finish this check it means that r has more elements
        # than l and that they are in the right order,
        # or that the two lists have the same lengths and we should move to the next elements
        # before making conclusions
        return None if len(r) == len(l) else True
    else:
        raise TypeError(f'Cannot compare types {type(l)} and {type(r)}')

def sort_packets(packets:List[List]):
    packets = sorted(packets, key=functools.cmp_to_key(lambda l, r: -1 if compare((l, r)) else 1))
    return packets

def parse_lines(lines:List[str]):
    packet_pairs = []
    has_chars_regex = r'[a-z]'
    for i in range(0, len(lines), 3):
        if not re.match(has_chars_regex, lines[i]) and \
           not re.match(has_chars_regex, lines[i+1]):
            packet_pairs.append((
                eval(lines[i]),     # I finally discovered eval
                eval(lines[i+1])    # Here I translate strings to lists
            ))
    return packet_pairs


if __name__ == '__main__':
    load_dotenv()
    lines = get_data(day=13, year=2022).splitlines()
    packet_pairs = parse_lines(lines)

    # # Examples
    # print("Examples:")
    # print(compare(([1,1,3,1,1], [1,1,5,1,1])))      # True
    # print(compare(([[1],[2,3,4]], [[1],4])))        # True
    # print(compare(([9], [[8,7,6]])))                # False
    # print(compare(([[4,4],4,4], [[4,4],4,4,4])))    # True
    # print(compare(([7,7,7,7], [7,7,7])))            # False
    # print(compare(([], [3])))                       # True
    # print(compare(([[[]]], [[]])))                  # False
    # print(compare(([1,[2,[3,[4,[5,6,7]]]],8,9], 
    #                [1,[2,[3,[4,[5,6,0]]]],8,9])))   # False
    # print(sort_packets([
    #     [1,1,3,1,1], [1,1,5,1,1], [[1],[2,3,4]], [[1],4], [9], [[8,7,6]],
    #     [[4,4],4,4], [[4,4],4,4,4], [7,7,7,7], [7,7,7], [], [3], [[[]]], [[]],
    #     [1,[2,[3,[4,[5,6,7]]]],8,9], [1,[2,[3,[4,[5,6,0]]]],8,9], [[2]], [[6]]
    # ]))
    # print("----------")

    # Problem 1
    correct_pairs = []
    for i in range(1, len(packet_pairs)+1):
        if compare(packet_pairs[i-1]):
            correct_pairs.append(i)    
    print(f"The sum of the indices of the correct pairs is {sum(correct_pairs)}")

    # Problem 2
    all_packets = [[[2]], [[6]]]        # Start with the divider packets
    for p in packet_pairs:
        all_packets.append(p[0])
        all_packets.append(p[1])
    sorted_packets = sort_packets(all_packets)
    for i in range(1, len(sorted_packets)+1):
        if sorted_packets[i-1] == [[2]]:
            idx1 = i
        elif sorted_packets[i-1] == [[6]]:
            idx2 = i    
    print(f"The indices of the sorted packets, mutliplied, are {idx1*idx2}")
    
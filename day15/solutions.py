import re
from tqdm import tqdm
import concurrent.futures
import numpy as np
from typing import List, Set, Tuple

from aocd import get_data
from dotenv import load_dotenv

class Cave():
    def __init__(self, lines:List[str]) -> None:
        self.sensors, self.beacons = self.parse_lines(lines)

    def compute_manhattan_distance(self, sensor, beacon) -> int:
        return abs(sensor[0] - beacon[0]) + abs(sensor[1] - beacon[1])

    def get_blocked_positions_in_line(self, line:int, xmin:int=-np.inf, 
                                            xmax:int=np.inf, ignore_sensors=True) -> Set[Tuple[int, int]]:
        blocked_positions = set()
        for sensor, beacon in zip(self.sensors, self.beacons):
            x, y = sensor
            dist = self.compute_manhattan_distance(sensor, beacon)
            sensor_line_dist = abs(y - line)    
            # If 0, y == line
            # Otherwise, it's the height distance between the two rows
            # On the line there will be exactly (dist - sensor_line_dist)*2 + 1
            # blocked positions around the x position of the sensor
            if x + dist < xmin or x - dist > xmax:
                continue
            for i in range((dist - sensor_line_dist)+1):
                if xmin <= x+i <= xmax:
                    blocked_positions.add((x+i, line))
                if xmin <= x-i <= xmax:
                    blocked_positions.add((x-i, line))
            if ignore_sensors:
                # Remove sensor and beacon if present on the line
                if sensor in blocked_positions:
                    blocked_positions.remove(sensor)
                if beacon in blocked_positions:
                    blocked_positions.remove(beacon)
        return blocked_positions

    def has_missing_position(self, y):
        xmin, xmax = 0, 4000000
        line_blocked_positions = self.get_blocked_positions_in_line(y, xmin, xmax, ignore_sensors=False)
        if len(line_blocked_positions) < (xmax-xmin):
            # Get missing x position
            missing_pos = set([(x, y) for x in range(xmin, xmax+1)]).difference(line_blocked_positions).pop()
            return missing_pos
        else:
            return None

    def find_distress_beacon(self) -> Tuple[int, int]:
        ymin, ymax = 0, 4000000
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
            future_to_y = {executor.submit(self.has_missing_position, y): y for y in range(ymin, ymax)}
            for future in concurrent.futures.as_completed(future_to_y):
                pos = future.result()
                if pos is not None:
                    # Stop all other jobs
                    executor.shutdown(wait=True, cancel_futures=True)
                    return pos
            

    def parse_lines(self, lines:List[str]) -> Tuple[List[Tuple[int, int]], List[Tuple[int, int]]]:
        el_reg = re.compile(r'Sensor at x=(-*\d+), y=(-*\d+): closest beacon is at x=(-*\d+), y=(-*\d+)')
        # We use lists because we need the association from each sensor to each beacon
        sensors, beacons = [], []
        for line in lines:
            sensor_x, sensor_y, beacon_x, beacon_y = el_reg.match(line).groups()
            sensors.append((int(sensor_x), int(sensor_y)))
            beacons.append((int(beacon_x), int(beacon_y)))
        return sensors, beacons


if __name__ == '__main__':
    load_dotenv()
    lines = get_data(year=2022, day=15).splitlines()

#     lines = '''Sensor at x=2, y=18: closest beacon is at x=-2, y=15
# Sensor at x=9, y=16: closest beacon is at x=10, y=16
# Sensor at x=13, y=2: closest beacon is at x=15, y=3
# Sensor at x=12, y=14: closest beacon is at x=10, y=16
# Sensor at x=10, y=20: closest beacon is at x=10, y=16
# Sensor at x=14, y=17: closest beacon is at x=10, y=16
# Sensor at x=8, y=7: closest beacon is at x=2, y=10
# Sensor at x=2, y=0: closest beacon is at x=2, y=10
# Sensor at x=0, y=11: closest beacon is at x=2, y=10
# Sensor at x=20, y=14: closest beacon is at x=25, y=17
# Sensor at x=17, y=20: closest beacon is at x=21, y=22
# Sensor at x=16, y=7: closest beacon is at x=15, y=3
# Sensor at x=14, y=3: closest beacon is at x=15, y=3
# Sensor at x=20, y=1: closest beacon is at x=15, y=3'''.splitlines()

    cave = Cave(lines)
    
    # Problem 1
    blocked_positions = cave.get_blocked_positions_in_line(2000000)
    print(f"There are {len(blocked_positions)} blocked positions on row 2,000,000")

    # Problem 2
    pos = cave.find_distress_beacon()
    print(f"The distress beacon should be at {len(pos)}.")

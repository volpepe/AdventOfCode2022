from aocd import get_data
from dotenv import load_dotenv

if __name__ == '__main__':
    load_dotenv()
    signal = get_data(day=6, year=2022)
    # Problem 1
    for i in range(len(signal)-3):
        # Iterate over the possible starting positions of the window
        # and check if removing duplicates the length remains the same:
        # in that case, the set of characters contains all different
        # chars and our starting point is i+4
        if len(set(signal[i:i+4])) == 4:
            break
    print(f"The packet starts from charater {i+4}")
    # Problem 2
    for i in range(len(signal)-13):
        # Very similar, but the number of characters is 14 rather than 4
        if len(set(signal[i:i+14])) == 14:
            break
    print(f"The message starts from charater {i+14}")

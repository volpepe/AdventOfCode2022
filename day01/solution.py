import os

if __name__ == '__main__':
    # Read input file
    with open(os.path.join('day01', 'input.txt'), 'r') as f:
        lines = [line.rstrip() for line in f.readlines()]
    # Iterate over lines
    elf_calories = {}
    elf_id = 0
    for line in lines:
        if line:
            # The line is a number of calories related to the current elf
            if elf_id in elf_calories:
                elf_calories[elf_id].append(int(line))
            else:
                # First time the elf id appears
                elf_calories[elf_id] = [int(line)]          
        else:
            # The line was "\n", so we need to consider the following calories
            # as related to the following elf
            elf_id += 1
    # Summing total calories
    total_calories = {
        elf_id: sum(elf_calories[elf_id])
        for elf_id in elf_calories.keys()
    }
    # Getting top elf and top calories
    top3_elves = sorted(total_calories, key=lambda e: -total_calories[e])[:3]
    top3_calories = [total_calories[top_elf] for top_elf in top3_elves]
    # Solution to problem #1
    print(f"Top elf: {top3_elves[0]}, top calories: {top3_calories[0]}")
    # Solution to problem #2
    print(f"Top 3 elves: {top3_elves}, sum of top 3 calories: {sum(top3_calories)}")
import csv
import sys

# parse the .csv file and build the ntm definition
def parse_csv(file_path):
    ntm = {"transitions": {}, "start_state": None, "accept_state": None, "reject_state": None}
    with open(file_path, mode='r') as file:
        reader = csv.reader(file)
        lines = list(reader)

        # parse the header
        ntm["name"] = lines[0][0]
        ntm["states"] = lines[1]
        ntm["input_alphabet"] = lines[2]
        ntm["tape_alphabet"] = lines[3]
        ntm["start_state"] = lines[4][0]
        ntm["accept_state"] = lines[5][0]
        ntm["reject_state"] = lines[6][0]

        # parse the transitions
        for transition in lines[7:]:
            current_state, input_symbol, next_state, write_symbol, direction = transition
            key = (current_state, input_symbol)
            if key not in ntm["transitions"]:
                ntm["transitions"][key] = []
            ntm["transitions"][key].append((next_state, write_symbol, direction))
    return ntm

# simulate the ntm
def simulate_ntm(ntm, input_string, max_depth):
    # initial config tree
    tree = [[["", ntm["start_state"], input_string]]]
    visited = set()
    total_steps = 0  # track the total number of steps
    for character in input_string: # check for unexpected characters
        if (character not in ntm["input_alphabet"]) and (character != "_"):
            return f"error: {character} not found in alphabet: {ntm["input_alphabet"]}"

    for steps in range(max_depth):
        current_level = tree[-1]  # get the configurations at the current level
        next_level = []  # prepare the next level of configurations
        total_steps += 1

        for config in current_level:
            left_of_head, state, right_of_head = config
            
            # stop if accept state is reached
            if state == ntm["accept_state"]:
                avg_nondeterminism = calc_nondeterminism(tree)
                return f"string accepted in {steps} steps. \ntree: {tree}. \ndegree of nondeterminism: {avg_nondeterminism:.2f}"

            # stop if no further exploration is possible
            if all(config[1] == ntm["reject_state"] for config in current_level):
                avg_nondeterminism = calc_nondeterminism(tree)
                return f"string rejected in {steps} steps. \ntree: {tree}. \ndegree of nondeterminism: {avg_nondeterminism:.2f}"

            # skip if reject state
            if state == ntm["reject_state"]:
                continue

            # get current symbol under the head
            current_symbol = right_of_head[0] if right_of_head else "_"

            # check transitions
            transitions = ntm["transitions"].get((state, current_symbol), [])
            if not transitions:
                continue

            for next_state, _, direction in transitions:
                # update the tape and move the head
                new_left = left_of_head
                new_right = right_of_head

                if direction == "L":
                    if new_left:
                        new_right = new_left[-1] + new_right
                        new_left = new_left[:-1]
                        if not new_left:
                            new_left = "_"
                    else:
                        new_right = "_" + new_right  # add blank when moving left
                elif direction == "R":
                    if new_right:
                        new_left += new_right[0]
                        new_right = new_right[1:]
                        if not new_right:
                            new_right = "_"
                    else:
                        new_left += "_"  # add blank when moving right

                # create new configuration
                new_config = [new_left, next_state, new_right]

                # avoid revisiting configurations
                if tuple(new_config) not in visited:
                    visited.add(tuple(new_config))
                    next_level.append(new_config)

        # add next level to the tree
        tree.append(next_level)

    # compute avg nondeterminism
    avg_nondeterminism = calc_nondeterminism(tree)
    return f"execution stopped after {max_depth} steps. \ndegree of nondeterminism: {avg_nondeterminism:.2f}"

# calculate average nondeterminism
def calc_nondeterminism(tree):
    total = 0
    for config in tree:
        total += len(config)
    return total / len(tree)

# main function to handle arguments
def main():
    if len(sys.argv) < 6:
        print("usage: python3 script.py <ntm_file> <input_string1> <input_string2> <input_string3> <max_depth>")
        print("note: to input an empty string, use '_'.")
        sys.exit(1)

    file_path = sys.argv[1]
    input_string1 = sys.argv[2]
    input_string2 = sys.argv[3]
    input_string3 = sys.argv[4]
    try:
        max_depth = int(sys.argv[5])
    except ValueError:
        print("error: max_depth must be an integer.")
        sys.exit(1)

    output_file = f"trace_{file_path.split('/')[-1].split('.')[0]}.txt"
    with open(output_file, "w") as f:
        # redirect all prints to the file
        sys.stdout = f

        # print inputs
        print(f"program: {sys.argv[0]}")
        print(f"ntm file: {file_path}")
        print(f"input string 1: {input_string1}")
        print(f"input string 2: {input_string2}")
        print(f"input string 3: {input_string3}")
        print(f"max depth: {max_depth}")

        try:
            ntm = parse_csv(file_path)
            for input_string in [input_string1, input_string2, input_string3]:
                print(f"\nprocessing input string: '{input_string}'")
                result = simulate_ntm(ntm, input_string, max_depth)
                print(result)
        except FileNotFoundError:
            print("error: csv file not found. please check the file path.")

if __name__ == "__main__":
    main()

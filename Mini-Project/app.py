# Import Libraries
import random
try:
    from tabulate import tabulate
    tabulate_installed = True
except ImportError:
    print("Please install tabulate using 'pip install tabulate' or type 'skip' to skip this step.")
    if input("Type 'skip' to skip this step: ").lower() == "skip":
        tabulate_installed = False
        print()
    else:
        print("Please install tabulate using 'pip install tabulate' or type 'skip' to skip this step.")
        exit()

# Probability Table
sample_sizes = [10, 100, 10000]
table_info = {"10": {}, "100": {}, "10000": {}}
roll_results = {
    "10": {
        "1": 0,
        "2": 0,
        "3": 0,
        "4": 0,
        "5": 0,
        "6": 0
    },
    "100": {
        "1": 0,
        "2": 0,
        "3": 0,
        "4": 0,
        "5": 0,
        "6": 0
    },
    "10000": {
        "1": 0,
        "2": 0,
        "3": 0,
        "4": 0,
        "5": 0,
        "6": 0
    },
}


# Functions
def roll_dice(sample_size, target_faces):
    """Rolls a dice and returns the result"""
    for rolls in range(sample_size):
        index = 0
        while index < sample_size:
            roll = random.randint(1, 6)
            roll_results[str(sample_size)][str(roll)] += 1
            index += 1

        return roll_results


def calculate_probability(roll_results, target_faces):
    """Calculates the probability of each face"""
    for face in target_faces:
        for sample_size in sample_sizes:
            probability = roll_results[str(sample_size)][str(face)] / sample_size
            print(f"The probability of rolling a {face} in {sample_size} amount of dice rolls is {probability}")

            table_info[str(sample_size)][str(face)] = probability
        print("_"*79)
        print("")

    return table_info 


def create_table(table_info, target_faces):
    table_headers = ["Rolls", ""]
    for face in target_faces:
        table_headers.append(str(face))

    table_data = []
    for header, data in table_info.items():
        table_data.append([header] + [data[str(face)] for face in target_faces])

    # Create the table
    try:
        table = tabulate(table_data, headers=table_headers, tablefmt="grid")
        print(table)
    except Exception as e:
            print("_"*79)

            # Print headers
            for header in table_headers:
                print(f"{header:10}", end="")
        
            print()
            print("-"*40)

            # Print data rows
            for row in table_data:
                for item in row:
                    print(f"{item:10.4f}" if isinstance(item, float) else f"{item:10}", end="")
                print()

    # Print the table    # print(table)



def main(target_faces):
    """Main function"""
    for sample_size in sample_sizes:
        # Roll the dice and get the results
        roll_results = roll_dice(sample_size, target_faces)

    # Calculate the probability of each face
    table_data = calculate_probability(roll_results, target_faces)

    # Create the probability table
    create_table(table_data, target_faces)
    
    # print(roll_results)
    return table_info


if __name__ == "__main__":
    # Vaariables
    target_faces = [1, 3, 6]

    main(target_faces)
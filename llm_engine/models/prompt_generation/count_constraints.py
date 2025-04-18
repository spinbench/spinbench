import os

# Path to the folder containing domains and problem instances
data_path = "/fastdownward/data/LLm-pddl-benchmark/data/pddl"

def count_constraints_in_file(file_path):
    """
    Count the number of constraints (preconditions) in a given PDDL domain file.
    """
    count = 0
    inside_precondition_block = False
    try:
        with open(file_path, 'r') as file:
            for line in file:
                line = line.strip()

                # Check if entering a precondition block
                if ":precondition" in line:
                    inside_precondition_block = True

                # Count predicates inside a precondition block
                if inside_precondition_block:
                    # Count all valid predicates (ignoring "not")
                    count += line.count('(') - line.count('not')

                # Check if leaving the precondition block
                if inside_precondition_block and ")" in line:
                    inside_precondition_block = False
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    return count

def classify_domain(domain_folder_path):
    """
    Classify whether a domain should be a Constraint Satisfaction Problem (CSP)
    and print constraints for each individual domain.
    """
    total_constraints = 0
    num_files = 0

    for root, _, files in os.walk(domain_folder_path):
        for file in files:
            if file.endswith("domain.pddl"):  # Only consider domain files
                file_path = os.path.join(root, file)
                constraints = count_constraints_in_file(file_path)
                total_constraints += constraints
                num_files += 1

                # Print the number of constraints for each domain file
                print(f"File: {file_path} - Constraints: {constraints}")

    # Define criteria for classifying as Constraint Satisfaction
    if num_files == 0:
        print("No PDDL domain files found in the given domain folder.")
        return False

    average_constraints_per_file = total_constraints / num_files

    # Criteria: More than 10 constraints on average per file -> classify as CSP
    if average_constraints_per_file > 10:
        print(f"Domain classified as Constraint Satisfaction Problem: {average_constraints_per_file:.2f} average constraints per file.")
        return True
    else:
        print(f"Domain NOT classified as Constraint Satisfaction Problem: {average_constraints_per_file:.2f} average constraints per file.")
        return False

if __name__ == "__main__":
    # Provide the path to the domain folder (replace with actual path)
    domain_folder_path = data_path

    # Run the classification and print individual file constraints
    classify_domain(domain_folder_path)


import subprocess
import os

def verify_plan(domain_file, problem_file, plan_file, val_executable='./validate'):
    """
    Verify a PDDL plan using VAL.

    Parameters:
    - domain_file (str): Path to the Domain PDDL file.
    - problem_file (str): Path to the Problem PDDL file.
    - plan_file (str): Path to the Plan PDDL file.
    - val_executable (str): Path to the VAL executable. Defaults to 'Validate'.

    Returns:
    - bool: True if the plan is valid, False otherwise.
    """
    # Check if files exist
    for file_path in [domain_file, problem_file, plan_file]:
        if not os.path.isfile(file_path):
            print(f"Error: File '{file_path}' does not exist.")
            return False

    # Construct the VAL command
    cmd = [
        val_executable,
        domain_file,
        problem_file,
        plan_file
    ]
    print(cmd)

    try:
        # Execute VAL as a subprocess
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # Debug: Print VAL's output (optional)
        print("VAL Output:\n", result.stdout)
        print("VAL Errors:\n", result.stderr)

        # Determine validity based on VAL's output
        if "Plan valid" in result.stdout:
            return True
        else:
            return False

    except FileNotFoundError:
        print(f"Error: VAL executable '{val_executable}' not found. Ensure VAL is installed and in your PATH.")
        return False
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False

def main():
    """
    Main function to verify the plan and print the result.
    """
    # Example file paths (replace with your actual file paths)
    domain_file = "/ssd2/kevin/projects/llm-pddl/domains/barman/domain.pddl"
    problem_file = "/ssd2/kevin/projects/llm-pddl/domains/barman/p01.pddl"
    plan_file = "/ssd2/kevin/projects/llm_plan_bench/barman/p01_claude.pddl"
    

    # Verify the plan
    is_valid = verify_plan(domain_file, problem_file, plan_file)

    # Print TRUE or FALSE based on the result
    if is_valid:
        print("TRUE")
    else:
        print("FALSE")

if __name__ == "__main__":
    main()

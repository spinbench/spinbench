import os
import random

# Configuration
output_dir = "scaled_problems"
num_problems = 5  # Number of problems to generate
min_robots = 2
max_robots = 5
min_rooms = 2
max_rooms = 5
min_objects = 1
max_objects = 5

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# Generate PDDL problems
for i in range(1, num_problems + 1):
    robots = random.randint(min_robots, max_robots)
    rooms = random.randint(min_rooms, max_rooms)
    objects = random.randint(min_objects, max_objects)

    # Define problem name and path with zero-padded numbering
    problem_name = f"pd{i:02d}.pddl"  # Zero-padded, e.g., pd01.pddl, pd02.pddl
    problem_file = os.path.join(output_dir, problem_name)

    # Generate PDDL content
    objects_section = (
        " ".join([f"robot{r}" for r in range(1, robots + 1)]) + " - robot\n" +
        " ".join([f"room{r}" for r in range(1, rooms + 1)]) + " - room\n" +
        " ".join([f"ball{b}" for b in range(1, objects + 1)]) + " - object\n" +
        " ".join([f"rgripper{r}" for r in range(1, robots + 1)]) + " " +
        " ".join([f"lgripper{r}" for r in range(1, robots + 1)]) + " - gripper"
    )

    init_section = (
        "\n".join([f"(at-robby robot{r} room{random.randint(1, rooms)})" for r in range(1, robots + 1)]) + "\n" +
        "\n".join([f"(free robot{r} rgripper{r})\n(free robot{r} lgripper{r})" for r in range(1, robots + 1)]) + "\n" +
        "\n".join([f"(at ball{b} room{random.randint(1, rooms)})" for b in range(1, objects + 1)])
    )

    # Assign collaboration requirement for objects
    for b in range(1, objects + 1):
        if random.choice([True, False]):  # 50% chance of requiring collaboration
            init_section += f"\n(needs-collaboration ball{b})"

    # Define a shared goal for all objects
    shared_goal_room = random.randint(1, rooms)
    goal_section = (
        "\n".join([f"(at ball{b} room{shared_goal_room})" for b in range(1, objects + 1)])
    )

    pddl_content = f"""
(define (problem {problem_name})
    (:domain gripper-multiagent)
    (:objects
        {objects_section}
    )
    (:init
        {init_section}
    )
    (:goal
        (and
            {goal_section}
        )
    )
)
    """

    # Write to file
    with open(problem_file, "w") as file:
        file.write(pddl_content.strip())

    print(f"Generated: {problem_file}")

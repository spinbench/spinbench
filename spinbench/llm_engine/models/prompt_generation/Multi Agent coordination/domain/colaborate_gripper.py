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
    problem_name = f"p{i:02d}.pddl"  # Zero-padded, e.g., p01.pddl, p02.pddl
    problem_file = os.path.join(output_dir, problem_name)

    # Generate PDDL content
    objects_section = (
        " ".join([f"robot{r}" for r in range(1, robots + 1)]) + " - robot\n" +
        " ".join([f"room{r}" for r in range(1, rooms + 1)]) + " - room\n" +
        " ".join([f"ball{b}" for b in range(1, objects + 1)]) + " - object\n" +
        " ".join([f"rgripper{r}" for r in range(1, robots + 1)]) + " " +
        " ".join([f"lgripper{r}" for r in range(1, robots + 1)]) + " - gripper"
    )

    # Generate initial robot positions
    robot_positions = {f"robot{r}": random.randint(1, rooms) for r in range(1, robots + 1)}
    init_section = (
        "\n".join([f"(at-robby {robot} room{room})" for robot, room in robot_positions.items()]) + "\n" +
        "\n".join([f"(free robot{r} rgripper{r})\n(free robot{r} lgripper{r})" for r in range(1, robots + 1)])
    )

    # Generate initial object positions and ensure at least one requires collaboration
    object_positions = {f"ball{b}": random.randint(1, rooms) for b in range(1, objects + 1)}
    collaborative_objects = random.sample(list(object_positions.keys()), k=max(1, len(object_positions) // 2))
    init_section += "\n" + "\n".join([f"(at {obj} room{room})" for obj, room in object_positions.items()])
    init_section += "\n" + "\n".join([f"(needs-collaboration {obj})" for obj in collaborative_objects])

    # Ensure the goal state is not trivially satisfied
    all_rooms = set(range(1, rooms + 1))
    occupied_rooms = set(object_positions.values())
    available_rooms = list(all_rooms - occupied_rooms)
    shared_goal_room = random.choice(available_rooms) if available_rooms else random.choice(list(all_rooms))

    goal_section = (
        "\n".join([f"(at {obj} room{shared_goal_room})" for obj in object_positions.keys()])
    )

    # Compile the PDDL content
    pddl_content = f"""
(define (problem {problem_name})
    (:domain domain)
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

print(f"Generated {num_problems} PDDL problems in '{output_dir}' directory.")

import os
import random

# Configuration
output_dir = "instances"
num_problems = 50  # Number of problems to generate
min_robots = 2
max_robots = 20
min_rooms = 2
max_rooms = 20
min_objects = 1
max_objects = 20

os.makedirs(output_dir, exist_ok=True)

for i in range(1, num_problems + 1):
    robots = random.randint(min_robots, max_robots)
    rooms = random.randint(min_rooms, max_rooms)
    objects = random.randint(min_objects, max_objects)

    # Create a "raw" name (p02, p03, etc.) for the problem.
    raw_problem_name = f"p{i:02d}"      # e.g., p01, p02, ...
    # Append .pddl for the filename on disk
    problem_filename = raw_problem_name + ".pddl"
    problem_file = os.path.join(output_dir, problem_filename)

    # Build up the domain objects, init, and goal sections
    objects_section = (
        " ".join([f"robot{r}" for r in range(1, robots + 1)]) + " - robot\n" +
        " ".join([f"room{r}" for r in range(1, rooms + 1)]) + " - room\n" +
        " ".join([f"ball{b}" for b in range(1, objects + 1)]) + " - object\n" +
        " ".join([f"rgripper{r}" for r in range(1, robots + 1)]) + " " +
        " ".join([f"lgripper{r}" for r in range(1, robots + 1)]) + " - gripper"
    )

    robot_positions = {
        f"robot{r}": random.randint(1, rooms) for r in range(1, robots + 1)
    }
    init_section = (
        "\n".join([f"(at-robby {robot} room{room})"
                   for robot, room in robot_positions.items()]) + "\n" +
        "\n".join([f"(free robot{r} rgripper{r})\n(free robot{r} lgripper{r})"
                   for r in range(1, robots + 1)])
    )

    object_positions = {
        f"ball{b}": random.randint(1, rooms) for b in range(1, objects + 1)
    }
    # Mark half (approx.) the objects as collaboration-needed
    collaborative_objects = random.sample(
        list(object_positions.keys()),
        k=max(1, len(object_positions) // 2)
    )
    init_section += "\n" + "\n".join([
        f"(at {obj} room{room})"
        for obj, room in object_positions.items()
    ])
    init_section += "\n" + "\n".join([
        f"(needs-collaboration {obj})"
        for obj in collaborative_objects
    ])

    # Construct a non-trivial goal
    all_rooms = set(range(1, rooms + 1))
    occupied_rooms = set(object_positions.values())
    available_rooms = list(all_rooms - occupied_rooms)
    if available_rooms:
        shared_goal_room = random.choice(available_rooms)
    else:
        shared_goal_room = random.choice(list(all_rooms))

    goal_section = "\n".join([
        f"(at {obj} room{shared_goal_room})"
        for obj in object_positions.keys()
    ])

    # Note: We reference raw_problem_name inside (define (problem ...))
    pddl_content = f"""
(define (problem {raw_problem_name})
    (:domain Multi_Agent_coordination)
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
""".strip()

    with open(problem_file, "w") as f:
        f.write(pddl_content)

print(f"Generated {num_problems} PDDL problems in '{output_dir}' directory.")

import os
import random

output_dir = "instances"
num_problems = 50

# We want fewer robots than rooms so single occupancy has some free space
ROOM_RANGE = (3, 30)
ROBOT_RANGE = (1, 20)
OBJECT_RANGE = (2, 20)

os.makedirs(output_dir, exist_ok=True)

configs = set()
while len(configs) < num_problems:
    num_rooms = random.randint(*ROOM_RANGE)
    num_robots = min(random.randint(*ROBOT_RANGE), num_rooms - 1)
    num_objects = random.randint(*OBJECT_RANGE)
    configs.add((num_rooms, num_robots, num_objects))

selected = list(configs)[:num_problems]

for i, (num_rooms, num_robots, num_objects) in enumerate(selected, start=1):
    # 1) Build a "raw" name like "p02"
    raw_problem_name = f"p{i:02d}"       # e.g. "p01", "p02", ...
    # 2) The filename on disk still appends ".pddl"
    problem_filename = raw_problem_name + ".pddl"
    problem_file = os.path.join(output_dir, problem_filename)

    # Create lists
    room_names = [f"room{r}" for r in range(1, num_rooms + 1)]
    robot_names = [f"robot{r}" for r in range(1, num_robots + 1)]
    object_names = [f"object{o}" for o in range(1, num_objects + 1)]

    # Shuffle rooms, assign each robot to a unique room
    random.shuffle(room_names)
    assigned_pairs = list(zip(robot_names, room_names))
    used_rooms = set(rm for (_, rm) in assigned_pairs)

    init_lines = []
    for (rbt, rm) in assigned_pairs:
        init_lines.append(f"(at-robby {rbt} {rm})")
        init_lines.append(f"(room-occupied {rm})")

    # Mark leftover rooms as free
    for rm in room_names:
        if rm not in used_rooms:
            init_lines.append(f"(not (room-occupied {rm}))")

    # Place objects randomly
    for obj in object_names:
        start_room = random.choice(room_names)
        init_lines.append(f"(at {obj} {start_room})")

    # Assign can-activate, can-handle
    for obj in object_names:
        chosen_robot = random.choice(robot_names)
        init_lines.append(f"(can-activate {chosen_robot} {obj})")
        init_lines.append(f"(can-handle {chosen_robot} {obj})")

    # Mark each robot's gripper as free
    for rbt in robot_names:
        init_lines.append(f"(free {rbt})")

    # Build the :objects section
    objects_section = []
    if robot_names:
        # The domain expects "gripper" for the robot type
        objects_section.append(" ".join(robot_names) + " - gripper")
    objects_section.append(" ".join(room_names) + " - room")
    objects_section.append(" ".join(object_names) + " - object")
    objects_str = "\n        ".join(objects_section)

    # Goals: for each object, a random final room
    goal_lines = []
    for obj in object_names:
        goal_room = random.choice(room_names)
        goal_lines.append(f"(at {obj} {goal_room})")

    # Also require one robot to be in a different room, if possible
    chosen_robot = random.choice(robot_names)
    init_room = next((rm for (r, rm) in assigned_pairs if r == chosen_robot), None)
    possible_rooms = [r for r in room_names if r != init_room]
    if possible_rooms:
        new_robot_room = random.choice(possible_rooms)
        goal_lines.append(f"(at-robby {chosen_robot} {new_robot_room})")

    goal_str = "\n      ".join(goal_lines)
    init_str = "\n        " + "\n        ".join(init_lines)

    # IMPORTANT: use "raw_problem_name" inside the define line
    pddl_content = f"""
(define (problem {raw_problem_name})
  (:domain cooperate_sequential_gripper)

  (:objects
        {objects_str}
  )

  (:init
        {init_str}
  )

  (:goal
    (and
      {goal_str}
    )
  )
)
""".strip()

    with open(problem_file, "w") as f:
        f.write(pddl_content)

print(f"Generated {len(selected)} PDDL problems in '{output_dir}' directory.")

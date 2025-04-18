(define (problem p03.pddl)
    (:domain domain)
    (:objects
        robot1 robot2 robot3 - robot
room1 room2 room3 room4 - room
ball1 ball2 - object
rgripper1 rgripper2 rgripper3 lgripper1 lgripper2 lgripper3 - gripper
    )
    (:init
        (at-robby robot1 room3)
(at-robby robot2 room2)
(at-robby robot3 room3)
(free robot1 rgripper1)
(free robot1 lgripper1)
(free robot2 rgripper2)
(free robot2 lgripper2)
(free robot3 rgripper3)
(free robot3 lgripper3)
(at ball1 room3)
(at ball2 room1)
(needs-collaboration ball1)
    )
    (:goal
        (and
            (at ball1 room4)
(at ball2 room4)
        )
    )
)

(define (problem p04.pddl)
    (:domain domain)
    (:objects
        robot1 robot2 robot3 robot4 robot5 - robot
room1 room2 - room
ball1 - object
rgripper1 rgripper2 rgripper3 rgripper4 rgripper5 lgripper1 lgripper2 lgripper3 lgripper4 lgripper5 - gripper
    )
    (:init
        (at-robby robot1 room1)
(at-robby robot2 room2)
(at-robby robot3 room1)
(at-robby robot4 room1)
(at-robby robot5 room2)
(free robot1 rgripper1)
(free robot1 lgripper1)
(free robot2 rgripper2)
(free robot2 lgripper2)
(free robot3 rgripper3)
(free robot3 lgripper3)
(free robot4 rgripper4)
(free robot4 lgripper4)
(free robot5 rgripper5)
(free robot5 lgripper5)
(at ball1 room2)
(needs-collaboration ball1)
    )
    (:goal
        (and
            (at ball1 room1)
        )
    )
)

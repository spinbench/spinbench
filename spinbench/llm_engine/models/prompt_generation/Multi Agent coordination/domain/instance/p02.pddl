(define (problem p02.pddl)
    (:domain domain)
    (:objects
        robot1 robot2 robot3 robot4 robot5 - robot
room1 room2 - room
ball1 ball2 ball3 ball4 ball5 - object
rgripper1 rgripper2 rgripper3 rgripper4 rgripper5 lgripper1 lgripper2 lgripper3 lgripper4 lgripper5 - gripper
    )
    (:init
        (at-robby robot1 room1)
(at-robby robot2 room1)
(at-robby robot3 room2)
(at-robby robot4 room2)
(at-robby robot5 room1)
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
(at ball1 room1)
(at ball2 room1)
(at ball3 room1)
(at ball4 room1)
(at ball5 room1)
(needs-collaboration ball4)
(needs-collaboration ball2)
    )
    (:goal
        (and
            (at ball1 room2)
(at ball2 room2)
(at ball3 room2)
(at ball4 room2)
(at ball5 room2)
        )
    )
)

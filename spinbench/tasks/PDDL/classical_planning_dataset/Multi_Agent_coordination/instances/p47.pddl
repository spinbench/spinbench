(define (problem p47)
    (:domain Multi_Agent_coordination)
    (:objects
        robot1 robot2 robot3 robot4 - robot
room1 room2 room3 room4 room5 room6 room7 room8 - room
ball1 ball2 ball3 ball4 - object
rgripper1 rgripper2 rgripper3 rgripper4 lgripper1 lgripper2 lgripper3 lgripper4 - gripper
    )
    (:init
        (at-robby robot1 room2)
(at-robby robot2 room2)
(at-robby robot3 room3)
(at-robby robot4 room4)
(free robot1 rgripper1)
(free robot1 lgripper1)
(free robot2 rgripper2)
(free robot2 lgripper2)
(free robot3 rgripper3)
(free robot3 lgripper3)
(free robot4 rgripper4)
(free robot4 lgripper4)
(at ball1 room6)
(at ball2 room3)
(at ball3 room1)
(at ball4 room8)
(needs-collaboration ball3)
(needs-collaboration ball2)
    )
    (:goal
        (and
            (at ball1 room2)
(at ball2 room2)
(at ball3 room2)
(at ball4 room2)
        )
    )
)
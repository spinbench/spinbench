(define (problem p11)
    (:domain Multi_Agent_coordination)
    (:objects
        robot1 robot2 robot3 - robot
room1 room2 room3 room4 room5 room6 room7 room8 room9 room10 - room
ball1 ball2 ball3 ball4 ball5 ball6 - object
rgripper1 rgripper2 rgripper3 lgripper1 lgripper2 lgripper3 - gripper
    )
    (:init
        (at-robby robot1 room8)
(at-robby robot2 room4)
(at-robby robot3 room2)
(free robot1 rgripper1)
(free robot1 lgripper1)
(free robot2 rgripper2)
(free robot2 lgripper2)
(free robot3 rgripper3)
(free robot3 lgripper3)
(at ball1 room10)
(at ball2 room2)
(at ball3 room10)
(at ball4 room4)
(at ball5 room4)
(at ball6 room2)
(needs-collaboration ball1)
(needs-collaboration ball3)
(needs-collaboration ball5)
    )
    (:goal
        (and
            (at ball1 room3)
(at ball2 room3)
(at ball3 room3)
(at ball4 room3)
(at ball5 room3)
(at ball6 room3)
        )
    )
)
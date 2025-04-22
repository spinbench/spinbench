(define (problem p19)
    (:domain Multi_Agent_coordination)
    (:objects
        robot1 robot2 robot3 robot4 - robot
room1 room2 room3 room4 room5 room6 room7 room8 room9 room10 room11 room12 room13 room14 room15 room16 room17 - room
ball1 - object
rgripper1 rgripper2 rgripper3 rgripper4 lgripper1 lgripper2 lgripper3 lgripper4 - gripper
    )
    (:init
        (at-robby robot1 room12)
(at-robby robot2 room11)
(at-robby robot3 room2)
(at-robby robot4 room15)
(free robot1 rgripper1)
(free robot1 lgripper1)
(free robot2 rgripper2)
(free robot2 lgripper2)
(free robot3 rgripper3)
(free robot3 lgripper3)
(free robot4 rgripper4)
(free robot4 lgripper4)
(at ball1 room14)
(needs-collaboration ball1)
    )
    (:goal
        (and
            (at ball1 room6)
        )
    )
)
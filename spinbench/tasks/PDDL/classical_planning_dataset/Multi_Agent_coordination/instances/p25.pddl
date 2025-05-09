(define (problem p25)
    (:domain Multi_Agent_coordination)
    (:objects
        robot1 robot2 robot3 robot4 - robot
room1 room2 room3 room4 room5 room6 - room
ball1 ball2 ball3 ball4 ball5 ball6 ball7 ball8 ball9 ball10 ball11 ball12 ball13 ball14 ball15 - object
rgripper1 rgripper2 rgripper3 rgripper4 lgripper1 lgripper2 lgripper3 lgripper4 - gripper
    )
    (:init
        (at-robby robot1 room5)
(at-robby robot2 room4)
(at-robby robot3 room5)
(at-robby robot4 room2)
(free robot1 rgripper1)
(free robot1 lgripper1)
(free robot2 rgripper2)
(free robot2 lgripper2)
(free robot3 rgripper3)
(free robot3 lgripper3)
(free robot4 rgripper4)
(free robot4 lgripper4)
(at ball1 room3)
(at ball2 room2)
(at ball3 room2)
(at ball4 room6)
(at ball5 room2)
(at ball6 room6)
(at ball7 room6)
(at ball8 room4)
(at ball9 room3)
(at ball10 room3)
(at ball11 room4)
(at ball12 room5)
(at ball13 room5)
(at ball14 room6)
(at ball15 room4)
(needs-collaboration ball1)
(needs-collaboration ball14)
(needs-collaboration ball13)
(needs-collaboration ball5)
(needs-collaboration ball8)
(needs-collaboration ball3)
(needs-collaboration ball10)
    )
    (:goal
        (and
            (at ball1 room1)
(at ball2 room1)
(at ball3 room1)
(at ball4 room1)
(at ball5 room1)
(at ball6 room1)
(at ball7 room1)
(at ball8 room1)
(at ball9 room1)
(at ball10 room1)
(at ball11 room1)
(at ball12 room1)
(at ball13 room1)
(at ball14 room1)
(at ball15 room1)
        )
    )
)
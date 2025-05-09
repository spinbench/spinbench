(define (problem p28)
    (:domain Multi_Agent_coordination)
    (:objects
        robot1 robot2 robot3 robot4 robot5 robot6 robot7 robot8 robot9 robot10 robot11 robot12 robot13 - robot
room1 room2 room3 room4 - room
ball1 ball2 - object
rgripper1 rgripper2 rgripper3 rgripper4 rgripper5 rgripper6 rgripper7 rgripper8 rgripper9 rgripper10 rgripper11 rgripper12 rgripper13 lgripper1 lgripper2 lgripper3 lgripper4 lgripper5 lgripper6 lgripper7 lgripper8 lgripper9 lgripper10 lgripper11 lgripper12 lgripper13 - gripper
    )
    (:init
        (at-robby robot1 room3)
(at-robby robot2 room3)
(at-robby robot3 room1)
(at-robby robot4 room3)
(at-robby robot5 room4)
(at-robby robot6 room2)
(at-robby robot7 room1)
(at-robby robot8 room3)
(at-robby robot9 room2)
(at-robby robot10 room4)
(at-robby robot11 room2)
(at-robby robot12 room2)
(at-robby robot13 room3)
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
(free robot6 rgripper6)
(free robot6 lgripper6)
(free robot7 rgripper7)
(free robot7 lgripper7)
(free robot8 rgripper8)
(free robot8 lgripper8)
(free robot9 rgripper9)
(free robot9 lgripper9)
(free robot10 rgripper10)
(free robot10 lgripper10)
(free robot11 rgripper11)
(free robot11 lgripper11)
(free robot12 rgripper12)
(free robot12 lgripper12)
(free robot13 rgripper13)
(free robot13 lgripper13)
(at ball1 room4)
(at ball2 room4)
(needs-collaboration ball1)
    )
    (:goal
        (and
            (at ball1 room1)
(at ball2 room1)
        )
    )
)
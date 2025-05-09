(define (problem p08)
  (:domain cooperate_sequential_gripper)

  (:objects
        robot1 robot2 - gripper
        room23 room3 room6 room22 room14 room2 room24 room19 room17 room15 room7 room21 room5 room20 room11 room12 room16 room4 room13 room18 room8 room10 room1 room9 - room
        object1 object2 object3 object4 object5 object6 object7 object8 object9 object10 object11 object12 object13 object14 - object
  )

  (:init
        
        (at-robby robot1 room23)
        (room-occupied room23)
        (at-robby robot2 room3)
        (room-occupied room3)
        (not (room-occupied room6))
        (not (room-occupied room22))
        (not (room-occupied room14))
        (not (room-occupied room2))
        (not (room-occupied room24))
        (not (room-occupied room19))
        (not (room-occupied room17))
        (not (room-occupied room15))
        (not (room-occupied room7))
        (not (room-occupied room21))
        (not (room-occupied room5))
        (not (room-occupied room20))
        (not (room-occupied room11))
        (not (room-occupied room12))
        (not (room-occupied room16))
        (not (room-occupied room4))
        (not (room-occupied room13))
        (not (room-occupied room18))
        (not (room-occupied room8))
        (not (room-occupied room10))
        (not (room-occupied room1))
        (not (room-occupied room9))
        (at object1 room11)
        (at object2 room1)
        (at object3 room11)
        (at object4 room3)
        (at object5 room13)
        (at object6 room14)
        (at object7 room21)
        (at object8 room10)
        (at object9 room20)
        (at object10 room4)
        (at object11 room3)
        (at object12 room17)
        (at object13 room12)
        (at object14 room3)
        (can-activate robot1 object1)
        (can-handle robot1 object1)
        (can-activate robot1 object2)
        (can-handle robot1 object2)
        (can-activate robot1 object3)
        (can-handle robot1 object3)
        (can-activate robot2 object4)
        (can-handle robot2 object4)
        (can-activate robot2 object5)
        (can-handle robot2 object5)
        (can-activate robot1 object6)
        (can-handle robot1 object6)
        (can-activate robot1 object7)
        (can-handle robot1 object7)
        (can-activate robot2 object8)
        (can-handle robot2 object8)
        (can-activate robot2 object9)
        (can-handle robot2 object9)
        (can-activate robot1 object10)
        (can-handle robot1 object10)
        (can-activate robot1 object11)
        (can-handle robot1 object11)
        (can-activate robot2 object12)
        (can-handle robot2 object12)
        (can-activate robot1 object13)
        (can-handle robot1 object13)
        (can-activate robot2 object14)
        (can-handle robot2 object14)
        (free robot1)
        (free robot2)
  )

  (:goal
    (and
      (at object1 room22)
      (at object2 room18)
      (at object3 room23)
      (at object4 room8)
      (at object5 room4)
      (at object6 room18)
      (at object7 room1)
      (at object8 room1)
      (at object9 room15)
      (at object10 room3)
      (at object11 room13)
      (at object12 room17)
      (at object13 room18)
      (at object14 room7)
      (at-robby robot2 room14)
    )
  )
)
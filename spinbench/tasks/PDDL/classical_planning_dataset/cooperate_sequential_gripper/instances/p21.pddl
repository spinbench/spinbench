(define (problem p21)
  (:domain cooperate_sequential_gripper)

  (:objects
        robot1 robot2 robot3 robot4 - gripper
        room3 room1 room8 room5 room7 room6 room2 room4 - room
        object1 object2 object3 object4 object5 object6 object7 object8 object9 object10 object11 object12 object13 object14 object15 object16 object17 object18 object19 object20 - object
  )

  (:init
        
        (at-robby robot1 room3)
        (room-occupied room3)
        (at-robby robot2 room1)
        (room-occupied room1)
        (at-robby robot3 room8)
        (room-occupied room8)
        (at-robby robot4 room5)
        (room-occupied room5)
        (not (room-occupied room7))
        (not (room-occupied room6))
        (not (room-occupied room2))
        (not (room-occupied room4))
        (at object1 room5)
        (at object2 room2)
        (at object3 room1)
        (at object4 room4)
        (at object5 room6)
        (at object6 room5)
        (at object7 room8)
        (at object8 room8)
        (at object9 room4)
        (at object10 room7)
        (at object11 room8)
        (at object12 room1)
        (at object13 room3)
        (at object14 room3)
        (at object15 room8)
        (at object16 room1)
        (at object17 room4)
        (at object18 room5)
        (at object19 room3)
        (at object20 room4)
        (can-activate robot4 object1)
        (can-handle robot4 object1)
        (can-activate robot2 object2)
        (can-handle robot2 object2)
        (can-activate robot2 object3)
        (can-handle robot2 object3)
        (can-activate robot4 object4)
        (can-handle robot4 object4)
        (can-activate robot2 object5)
        (can-handle robot2 object5)
        (can-activate robot4 object6)
        (can-handle robot4 object6)
        (can-activate robot1 object7)
        (can-handle robot1 object7)
        (can-activate robot1 object8)
        (can-handle robot1 object8)
        (can-activate robot4 object9)
        (can-handle robot4 object9)
        (can-activate robot3 object10)
        (can-handle robot3 object10)
        (can-activate robot3 object11)
        (can-handle robot3 object11)
        (can-activate robot1 object12)
        (can-handle robot1 object12)
        (can-activate robot1 object13)
        (can-handle robot1 object13)
        (can-activate robot1 object14)
        (can-handle robot1 object14)
        (can-activate robot4 object15)
        (can-handle robot4 object15)
        (can-activate robot2 object16)
        (can-handle robot2 object16)
        (can-activate robot4 object17)
        (can-handle robot4 object17)
        (can-activate robot3 object18)
        (can-handle robot3 object18)
        (can-activate robot3 object19)
        (can-handle robot3 object19)
        (can-activate robot1 object20)
        (can-handle robot1 object20)
        (free robot1)
        (free robot2)
        (free robot3)
        (free robot4)
  )

  (:goal
    (and
      (at object1 room3)
      (at object2 room3)
      (at object3 room8)
      (at object4 room8)
      (at object5 room4)
      (at object6 room5)
      (at object7 room1)
      (at object8 room5)
      (at object9 room5)
      (at object10 room4)
      (at object11 room1)
      (at object12 room1)
      (at object13 room2)
      (at object14 room6)
      (at object15 room5)
      (at object16 room4)
      (at object17 room1)
      (at object18 room1)
      (at object19 room4)
      (at object20 room2)
      (at-robby robot2 room6)
    )
  )
)
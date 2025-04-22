(define (problem p48)
  (:domain cooperate_sequential_gripper)

  (:objects
        robot1 robot2 robot3 - gripper
        room9 room4 room6 room1 room7 room5 room11 room3 room8 room10 room2 - room
        object1 object2 object3 object4 object5 - object
  )

  (:init
        
        (at-robby robot1 room9)
        (room-occupied room9)
        (at-robby robot2 room4)
        (room-occupied room4)
        (at-robby robot3 room6)
        (room-occupied room6)
        (not (room-occupied room1))
        (not (room-occupied room7))
        (not (room-occupied room5))
        (not (room-occupied room11))
        (not (room-occupied room3))
        (not (room-occupied room8))
        (not (room-occupied room10))
        (not (room-occupied room2))
        (at object1 room10)
        (at object2 room3)
        (at object3 room6)
        (at object4 room11)
        (at object5 room2)
        (can-activate robot2 object1)
        (can-handle robot2 object1)
        (can-activate robot2 object2)
        (can-handle robot2 object2)
        (can-activate robot1 object3)
        (can-handle robot1 object3)
        (can-activate robot1 object4)
        (can-handle robot1 object4)
        (can-activate robot2 object5)
        (can-handle robot2 object5)
        (free robot1)
        (free robot2)
        (free robot3)
  )

  (:goal
    (and
      (at object1 room10)
      (at object2 room7)
      (at object3 room2)
      (at object4 room11)
      (at object5 room3)
      (at-robby robot1 room1)
    )
  )
)
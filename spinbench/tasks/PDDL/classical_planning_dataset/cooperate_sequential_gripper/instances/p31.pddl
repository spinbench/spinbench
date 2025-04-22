(define (problem p31)
  (:domain cooperate_sequential_gripper)

  (:objects
        robot1 robot2 - gripper
        room2 room1 room3 - room
        object1 object2 object3 object4 object5 object6 - object
  )

  (:init
        
        (at-robby robot1 room2)
        (room-occupied room2)
        (at-robby robot2 room1)
        (room-occupied room1)
        (not (room-occupied room3))
        (at object1 room2)
        (at object2 room2)
        (at object3 room2)
        (at object4 room2)
        (at object5 room2)
        (at object6 room1)
        (can-activate robot1 object1)
        (can-handle robot1 object1)
        (can-activate robot2 object2)
        (can-handle robot2 object2)
        (can-activate robot2 object3)
        (can-handle robot2 object3)
        (can-activate robot1 object4)
        (can-handle robot1 object4)
        (can-activate robot2 object5)
        (can-handle robot2 object5)
        (can-activate robot1 object6)
        (can-handle robot1 object6)
        (free robot1)
        (free robot2)
  )

  (:goal
    (and
      (at object1 room1)
      (at object2 room1)
      (at object3 room2)
      (at object4 room2)
      (at object5 room2)
      (at object6 room1)
      (at-robby robot1 room1)
    )
  )
)
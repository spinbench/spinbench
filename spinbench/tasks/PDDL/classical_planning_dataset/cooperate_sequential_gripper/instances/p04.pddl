(define (problem p04)
  (:domain cooperate_sequential_gripper)

  (:objects
        robot1 robot2 robot3 robot4 - gripper
        room2 room3 room5 room1 room4 - room
        object1 object2 object3 object4 object5 object6 object7 object8 object9 object10 object11 - object
  )

  (:init
        
        (at-robby robot1 room2)
        (room-occupied room2)
        (at-robby robot2 room3)
        (room-occupied room3)
        (at-robby robot3 room5)
        (room-occupied room5)
        (at-robby robot4 room1)
        (room-occupied room1)
        (not (room-occupied room4))
        (at object1 room1)
        (at object2 room5)
        (at object3 room5)
        (at object4 room3)
        (at object5 room3)
        (at object6 room5)
        (at object7 room5)
        (at object8 room2)
        (at object9 room2)
        (at object10 room5)
        (at object11 room5)
        (can-activate robot1 object1)
        (can-handle robot1 object1)
        (can-activate robot1 object2)
        (can-handle robot1 object2)
        (can-activate robot3 object3)
        (can-handle robot3 object3)
        (can-activate robot1 object4)
        (can-handle robot1 object4)
        (can-activate robot3 object5)
        (can-handle robot3 object5)
        (can-activate robot3 object6)
        (can-handle robot3 object6)
        (can-activate robot1 object7)
        (can-handle robot1 object7)
        (can-activate robot3 object8)
        (can-handle robot3 object8)
        (can-activate robot4 object9)
        (can-handle robot4 object9)
        (can-activate robot2 object10)
        (can-handle robot2 object10)
        (can-activate robot4 object11)
        (can-handle robot4 object11)
        (free robot1)
        (free robot2)
        (free robot3)
        (free robot4)
  )

  (:goal
    (and
      (at object1 room4)
      (at object2 room2)
      (at object3 room2)
      (at object4 room5)
      (at object5 room3)
      (at object6 room2)
      (at object7 room2)
      (at object8 room3)
      (at object9 room3)
      (at object10 room2)
      (at object11 room3)
      (at-robby robot2 room1)
    )
  )
)
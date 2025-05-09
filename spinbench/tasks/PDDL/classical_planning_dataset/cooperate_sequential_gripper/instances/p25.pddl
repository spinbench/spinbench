(define (problem p25)
  (:domain cooperate_sequential_gripper)

  (:objects
        robot1 robot2 robot3 robot4 robot5 robot6 robot7 robot8 robot9 robot10 robot11 - gripper
        room7 room5 room6 room10 room11 room9 room4 room3 room1 room8 room2 room12 - room
        object1 object2 object3 object4 object5 object6 object7 - object
  )

  (:init
        
        (at-robby robot1 room7)
        (room-occupied room7)
        (at-robby robot2 room5)
        (room-occupied room5)
        (at-robby robot3 room6)
        (room-occupied room6)
        (at-robby robot4 room10)
        (room-occupied room10)
        (at-robby robot5 room11)
        (room-occupied room11)
        (at-robby robot6 room9)
        (room-occupied room9)
        (at-robby robot7 room4)
        (room-occupied room4)
        (at-robby robot8 room3)
        (room-occupied room3)
        (at-robby robot9 room1)
        (room-occupied room1)
        (at-robby robot10 room8)
        (room-occupied room8)
        (at-robby robot11 room2)
        (room-occupied room2)
        (not (room-occupied room12))
        (at object1 room9)
        (at object2 room10)
        (at object3 room2)
        (at object4 room3)
        (at object5 room12)
        (at object6 room2)
        (at object7 room2)
        (can-activate robot4 object1)
        (can-handle robot4 object1)
        (can-activate robot6 object2)
        (can-handle robot6 object2)
        (can-activate robot10 object3)
        (can-handle robot10 object3)
        (can-activate robot1 object4)
        (can-handle robot1 object4)
        (can-activate robot2 object5)
        (can-handle robot2 object5)
        (can-activate robot10 object6)
        (can-handle robot10 object6)
        (can-activate robot5 object7)
        (can-handle robot5 object7)
        (free robot1)
        (free robot2)
        (free robot3)
        (free robot4)
        (free robot5)
        (free robot6)
        (free robot7)
        (free robot8)
        (free robot9)
        (free robot10)
        (free robot11)
  )

  (:goal
    (and
      (at object1 room4)
      (at object2 room12)
      (at object3 room10)
      (at object4 room8)
      (at object5 room7)
      (at object6 room8)
      (at object7 room6)
      (at-robby robot1 room12)
    )
  )
)
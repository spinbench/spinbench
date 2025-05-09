(define (problem p18)
  (:domain cooperate_sequential_gripper)

  (:objects
        robot1 robot2 robot3 robot4 robot5 robot6 robot7 robot8 robot9 robot10 robot11 robot12 robot13 robot14 robot15 - gripper
        room10 room11 room3 room12 room2 room6 room7 room9 room8 room1 room13 room16 room14 room4 room5 room15 - room
        object1 object2 object3 object4 object5 object6 object7 object8 object9 object10 - object
  )

  (:init
        
        (at-robby robot1 room10)
        (room-occupied room10)
        (at-robby robot2 room11)
        (room-occupied room11)
        (at-robby robot3 room3)
        (room-occupied room3)
        (at-robby robot4 room12)
        (room-occupied room12)
        (at-robby robot5 room2)
        (room-occupied room2)
        (at-robby robot6 room6)
        (room-occupied room6)
        (at-robby robot7 room7)
        (room-occupied room7)
        (at-robby robot8 room9)
        (room-occupied room9)
        (at-robby robot9 room8)
        (room-occupied room8)
        (at-robby robot10 room1)
        (room-occupied room1)
        (at-robby robot11 room13)
        (room-occupied room13)
        (at-robby robot12 room16)
        (room-occupied room16)
        (at-robby robot13 room14)
        (room-occupied room14)
        (at-robby robot14 room4)
        (room-occupied room4)
        (at-robby robot15 room5)
        (room-occupied room5)
        (not (room-occupied room15))
        (at object1 room1)
        (at object2 room5)
        (at object3 room13)
        (at object4 room4)
        (at object5 room13)
        (at object6 room4)
        (at object7 room1)
        (at object8 room13)
        (at object9 room9)
        (at object10 room9)
        (can-activate robot10 object1)
        (can-handle robot10 object1)
        (can-activate robot11 object2)
        (can-handle robot11 object2)
        (can-activate robot5 object3)
        (can-handle robot5 object3)
        (can-activate robot14 object4)
        (can-handle robot14 object4)
        (can-activate robot3 object5)
        (can-handle robot3 object5)
        (can-activate robot9 object6)
        (can-handle robot9 object6)
        (can-activate robot10 object7)
        (can-handle robot10 object7)
        (can-activate robot2 object8)
        (can-handle robot2 object8)
        (can-activate robot7 object9)
        (can-handle robot7 object9)
        (can-activate robot1 object10)
        (can-handle robot1 object10)
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
        (free robot12)
        (free robot13)
        (free robot14)
        (free robot15)
  )

  (:goal
    (and
      (at object1 room14)
      (at object2 room10)
      (at object3 room4)
      (at object4 room12)
      (at object5 room12)
      (at object6 room13)
      (at object7 room3)
      (at object8 room6)
      (at object9 room7)
      (at object10 room6)
      (at-robby robot15 room7)
    )
  )
)
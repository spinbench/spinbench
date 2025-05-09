(define (problem p15)
  (:domain cooperate_sequential_gripper)

  (:objects
        robot1 robot2 robot3 robot4 robot5 robot6 robot7 robot8 robot9 robot10 robot11 robot12 robot13 robot14 robot15 - gripper
        room5 room6 room3 room9 room12 room16 room2 room19 room17 room4 room20 room13 room18 room14 room7 room1 room8 room10 room15 room11 - room
        object1 object2 object3 object4 object5 object6 object7 object8 - object
  )

  (:init
        
        (at-robby robot1 room5)
        (room-occupied room5)
        (at-robby robot2 room6)
        (room-occupied room6)
        (at-robby robot3 room3)
        (room-occupied room3)
        (at-robby robot4 room9)
        (room-occupied room9)
        (at-robby robot5 room12)
        (room-occupied room12)
        (at-robby robot6 room16)
        (room-occupied room16)
        (at-robby robot7 room2)
        (room-occupied room2)
        (at-robby robot8 room19)
        (room-occupied room19)
        (at-robby robot9 room17)
        (room-occupied room17)
        (at-robby robot10 room4)
        (room-occupied room4)
        (at-robby robot11 room20)
        (room-occupied room20)
        (at-robby robot12 room13)
        (room-occupied room13)
        (at-robby robot13 room18)
        (room-occupied room18)
        (at-robby robot14 room14)
        (room-occupied room14)
        (at-robby robot15 room7)
        (room-occupied room7)
        (not (room-occupied room1))
        (not (room-occupied room8))
        (not (room-occupied room10))
        (not (room-occupied room15))
        (not (room-occupied room11))
        (at object1 room17)
        (at object2 room1)
        (at object3 room15)
        (at object4 room14)
        (at object5 room12)
        (at object6 room16)
        (at object7 room5)
        (at object8 room1)
        (can-activate robot4 object1)
        (can-handle robot4 object1)
        (can-activate robot1 object2)
        (can-handle robot1 object2)
        (can-activate robot15 object3)
        (can-handle robot15 object3)
        (can-activate robot15 object4)
        (can-handle robot15 object4)
        (can-activate robot8 object5)
        (can-handle robot8 object5)
        (can-activate robot6 object6)
        (can-handle robot6 object6)
        (can-activate robot14 object7)
        (can-handle robot14 object7)
        (can-activate robot6 object8)
        (can-handle robot6 object8)
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
      (at object1 room12)
      (at object2 room5)
      (at object3 room9)
      (at object4 room19)
      (at object5 room2)
      (at object6 room3)
      (at object7 room13)
      (at object8 room11)
      (at-robby robot8 room9)
    )
  )
)
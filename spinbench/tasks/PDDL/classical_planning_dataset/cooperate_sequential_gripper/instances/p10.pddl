(define (problem p10)
  (:domain cooperate_sequential_gripper)

  (:objects
        robot1 robot2 robot3 robot4 robot5 robot6 robot7 - gripper
        room8 room12 room13 room9 room7 room2 room3 room1 room5 room10 room4 room11 room6 - room
        object1 object2 object3 object4 object5 object6 object7 object8 object9 object10 object11 object12 object13 object14 object15 object16 object17 object18 - object
  )

  (:init
        
        (at-robby robot1 room8)
        (room-occupied room8)
        (at-robby robot2 room12)
        (room-occupied room12)
        (at-robby robot3 room13)
        (room-occupied room13)
        (at-robby robot4 room9)
        (room-occupied room9)
        (at-robby robot5 room7)
        (room-occupied room7)
        (at-robby robot6 room2)
        (room-occupied room2)
        (at-robby robot7 room3)
        (room-occupied room3)
        (not (room-occupied room1))
        (not (room-occupied room5))
        (not (room-occupied room10))
        (not (room-occupied room4))
        (not (room-occupied room11))
        (not (room-occupied room6))
        (at object1 room13)
        (at object2 room12)
        (at object3 room8)
        (at object4 room12)
        (at object5 room1)
        (at object6 room6)
        (at object7 room13)
        (at object8 room6)
        (at object9 room5)
        (at object10 room4)
        (at object11 room5)
        (at object12 room5)
        (at object13 room11)
        (at object14 room9)
        (at object15 room10)
        (at object16 room7)
        (at object17 room3)
        (at object18 room11)
        (can-activate robot7 object1)
        (can-handle robot7 object1)
        (can-activate robot4 object2)
        (can-handle robot4 object2)
        (can-activate robot6 object3)
        (can-handle robot6 object3)
        (can-activate robot3 object4)
        (can-handle robot3 object4)
        (can-activate robot6 object5)
        (can-handle robot6 object5)
        (can-activate robot5 object6)
        (can-handle robot5 object6)
        (can-activate robot6 object7)
        (can-handle robot6 object7)
        (can-activate robot4 object8)
        (can-handle robot4 object8)
        (can-activate robot5 object9)
        (can-handle robot5 object9)
        (can-activate robot6 object10)
        (can-handle robot6 object10)
        (can-activate robot6 object11)
        (can-handle robot6 object11)
        (can-activate robot5 object12)
        (can-handle robot5 object12)
        (can-activate robot3 object13)
        (can-handle robot3 object13)
        (can-activate robot2 object14)
        (can-handle robot2 object14)
        (can-activate robot7 object15)
        (can-handle robot7 object15)
        (can-activate robot4 object16)
        (can-handle robot4 object16)
        (can-activate robot6 object17)
        (can-handle robot6 object17)
        (can-activate robot6 object18)
        (can-handle robot6 object18)
        (free robot1)
        (free robot2)
        (free robot3)
        (free robot4)
        (free robot5)
        (free robot6)
        (free robot7)
  )

  (:goal
    (and
      (at object1 room1)
      (at object2 room9)
      (at object3 room1)
      (at object4 room6)
      (at object5 room8)
      (at object6 room9)
      (at object7 room10)
      (at object8 room6)
      (at object9 room8)
      (at object10 room8)
      (at object11 room7)
      (at object12 room10)
      (at object13 room11)
      (at object14 room6)
      (at object15 room6)
      (at object16 room8)
      (at object17 room6)
      (at object18 room1)
      (at-robby robot2 room6)
    )
  )
)
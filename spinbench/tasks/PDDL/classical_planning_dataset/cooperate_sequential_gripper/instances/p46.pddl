(define (problem p46)
  (:domain cooperate_sequential_gripper)

  (:objects
        robot1 robot2 robot3 robot4 robot5 robot6 robot7 robot8 robot9 robot10 robot11 robot12 robot13 robot14 - gripper
        room10 room5 room16 room23 room17 room15 room14 room22 room8 room25 room12 room11 room6 room18 room20 room4 room26 room19 room9 room7 room13 room24 room1 room2 room21 room3 - room
        object1 object2 object3 object4 object5 object6 object7 object8 object9 object10 object11 object12 object13 object14 object15 object16 object17 object18 object19 object20 - object
  )

  (:init
        
        (at-robby robot1 room10)
        (room-occupied room10)
        (at-robby robot2 room5)
        (room-occupied room5)
        (at-robby robot3 room16)
        (room-occupied room16)
        (at-robby robot4 room23)
        (room-occupied room23)
        (at-robby robot5 room17)
        (room-occupied room17)
        (at-robby robot6 room15)
        (room-occupied room15)
        (at-robby robot7 room14)
        (room-occupied room14)
        (at-robby robot8 room22)
        (room-occupied room22)
        (at-robby robot9 room8)
        (room-occupied room8)
        (at-robby robot10 room25)
        (room-occupied room25)
        (at-robby robot11 room12)
        (room-occupied room12)
        (at-robby robot12 room11)
        (room-occupied room11)
        (at-robby robot13 room6)
        (room-occupied room6)
        (at-robby robot14 room18)
        (room-occupied room18)
        (not (room-occupied room20))
        (not (room-occupied room4))
        (not (room-occupied room26))
        (not (room-occupied room19))
        (not (room-occupied room9))
        (not (room-occupied room7))
        (not (room-occupied room13))
        (not (room-occupied room24))
        (not (room-occupied room1))
        (not (room-occupied room2))
        (not (room-occupied room21))
        (not (room-occupied room3))
        (at object1 room17)
        (at object2 room8)
        (at object3 room4)
        (at object4 room21)
        (at object5 room7)
        (at object6 room11)
        (at object7 room25)
        (at object8 room1)
        (at object9 room17)
        (at object10 room26)
        (at object11 room23)
        (at object12 room22)
        (at object13 room19)
        (at object14 room3)
        (at object15 room12)
        (at object16 room3)
        (at object17 room10)
        (at object18 room23)
        (at object19 room5)
        (at object20 room18)
        (can-activate robot11 object1)
        (can-handle robot11 object1)
        (can-activate robot5 object2)
        (can-handle robot5 object2)
        (can-activate robot13 object3)
        (can-handle robot13 object3)
        (can-activate robot13 object4)
        (can-handle robot13 object4)
        (can-activate robot3 object5)
        (can-handle robot3 object5)
        (can-activate robot9 object6)
        (can-handle robot9 object6)
        (can-activate robot10 object7)
        (can-handle robot10 object7)
        (can-activate robot4 object8)
        (can-handle robot4 object8)
        (can-activate robot3 object9)
        (can-handle robot3 object9)
        (can-activate robot1 object10)
        (can-handle robot1 object10)
        (can-activate robot6 object11)
        (can-handle robot6 object11)
        (can-activate robot13 object12)
        (can-handle robot13 object12)
        (can-activate robot1 object13)
        (can-handle robot1 object13)
        (can-activate robot1 object14)
        (can-handle robot1 object14)
        (can-activate robot2 object15)
        (can-handle robot2 object15)
        (can-activate robot1 object16)
        (can-handle robot1 object16)
        (can-activate robot5 object17)
        (can-handle robot5 object17)
        (can-activate robot11 object18)
        (can-handle robot11 object18)
        (can-activate robot7 object19)
        (can-handle robot7 object19)
        (can-activate robot13 object20)
        (can-handle robot13 object20)
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
  )

  (:goal
    (and
      (at object1 room1)
      (at object2 room15)
      (at object3 room4)
      (at object4 room2)
      (at object5 room14)
      (at object6 room15)
      (at object7 room17)
      (at object8 room19)
      (at object9 room10)
      (at object10 room1)
      (at object11 room11)
      (at object12 room20)
      (at object13 room10)
      (at object14 room23)
      (at object15 room24)
      (at object16 room23)
      (at object17 room21)
      (at object18 room9)
      (at object19 room14)
      (at object20 room4)
      (at-robby robot12 room12)
    )
  )
)
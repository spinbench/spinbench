; Automatically generated instance: grid-3-4-S2-K3-L3-PG0.5-typedFalse-seed1
; x=3, y=4, shapes=2, keys=3, locks=3, prob_goal=0.5, typed=False, seed=1

(define (problem grid-3-4-S2-K3-L3-PG0.5-typedFalse-seed1)
    (:domain grid)
    (:objects
        pos0-0 pos0-1 pos0-2 pos0-3 pos1-0 pos1-1 pos1-2 pos1-3 pos2-0 pos2-1 pos2-2 pos2-3
        shape0 shape1
        key0 key1 key2
    )

    (:init
        (arm-empty)

       (place pos0-0)
       (place pos0-1)
       (place pos0-2)
       (place pos0-3)
       (place pos1-0)
       (place pos1-1)
       (place pos1-2)
       (place pos1-3)
       (place pos2-0)
       (place pos2-1)
       (place pos2-2)
       (place pos2-3)
       (shape shape0)
       (shape shape1)
       (key key0)
       (key key1)
       (key key2)

       (conn pos0-0 pos1-0)
       (conn pos0-0 pos0-1)
       (conn pos0-1 pos1-1)
       (conn pos0-1 pos0-2)
       (conn pos0-1 pos0-0)
       (conn pos0-2 pos1-2)
       (conn pos0-2 pos0-3)
       (conn pos0-2 pos0-1)
       (conn pos0-3 pos1-3)
       (conn pos0-3 pos0-2)
       (conn pos1-0 pos2-0)
       (conn pos1-0 pos1-1)
       (conn pos1-0 pos0-0)
       (conn pos1-1 pos2-1)
       (conn pos1-1 pos1-2)
       (conn pos1-1 pos0-1)
       (conn pos1-1 pos1-0)
       (conn pos1-2 pos2-2)
       (conn pos1-2 pos1-3)
       (conn pos1-2 pos0-2)
       (conn pos1-2 pos1-1)
       (conn pos1-3 pos2-3)
       (conn pos1-3 pos0-3)
       (conn pos1-3 pos1-2)
       (conn pos2-0 pos2-1)
       (conn pos2-0 pos1-0)
       (conn pos2-1 pos2-2)
       (conn pos2-1 pos1-1)
       (conn pos2-1 pos2-0)
       (conn pos2-2 pos2-3)
       (conn pos2-2 pos1-2)
       (conn pos2-2 pos2-1)
       (conn pos2-3 pos1-3)
       (conn pos2-3 pos2-2)

       (locked pos0-2)
       (locked pos2-1)
       (locked pos0-1)
       (lock-shape pos0-2 shape0)
       (lock-shape pos2-1 shape1)
       (lock-shape pos0-1 shape1)
       (open pos0-0)
       (open pos0-3)
       (open pos1-0)
       (open pos1-1)
       (open pos1-2)
       (open pos1-3)
       (open pos2-0)
       (open pos2-2)
       (open pos2-3)

       (key-shape key0 shape0)
       (key-shape key1 shape1)
       (key-shape key2 shape0)
       (at key0 pos2-2)
       (at key2 pos1-0)
       (at key1 pos2-0)
       (at-robot pos1-2)
    )

    (:goal (and
       (at key0 pos1-2)
       (at key1 pos0-0)
    ))
)

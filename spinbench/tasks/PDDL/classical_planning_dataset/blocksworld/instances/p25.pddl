

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 )
(:init
(arm-empty)
(on b1 b9)
(on-table b2)
(on-table b3)
(on-table b4)
(on-table b5)
(on b6 b4)
(on b7 b3)
(on-table b8)
(on b9 b6)
(clear b1)
(clear b2)
(clear b5)
(clear b7)
(clear b8)
)
(:goal
(and
(on b1 b4)
(on b3 b6)
(on b4 b7)
(on b5 b8)
(on b6 b1)
(on b7 b2)
(on b9 b3))
)
)



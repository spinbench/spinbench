

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 )
(:init
(arm-empty)
(on b1 b3)
(on-table b2)
(on b3 b5)
(on-table b4)
(on b5 b6)
(on-table b6)
(on b7 b9)
(on b8 b2)
(on b9 b4)
(clear b1)
(clear b7)
(clear b8)
)
(:goal
(and
(on b1 b6)
(on b2 b1)
(on b3 b5)
(on b6 b8)
(on b7 b4)
(on b8 b9)
(on b9 b3))
)
)



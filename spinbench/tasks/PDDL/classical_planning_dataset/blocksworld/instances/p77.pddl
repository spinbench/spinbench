

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 )
(:init
(arm-empty)
(on b1 b9)
(on b2 b3)
(on b3 b7)
(on-table b4)
(on b5 b8)
(on b6 b4)
(on-table b7)
(on-table b8)
(on b9 b2)
(clear b1)
(clear b5)
(clear b6)
)
(:goal
(and
(on b1 b8)
(on b2 b1)
(on b3 b7)
(on b6 b5)
(on b8 b9)
(on b9 b3))
)
)



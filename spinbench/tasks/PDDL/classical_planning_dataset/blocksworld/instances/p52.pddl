

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 )
(:init
(arm-empty)
(on-table b1)
(on-table b2)
(on b3 b8)
(on b4 b9)
(on b5 b7)
(on-table b6)
(on b7 b4)
(on-table b8)
(on b9 b1)
(clear b2)
(clear b3)
(clear b5)
(clear b6)
)
(:goal
(and
(on b4 b5)
(on b5 b8)
(on b6 b9)
(on b7 b1)
(on b8 b3)
(on b9 b4))
)
)



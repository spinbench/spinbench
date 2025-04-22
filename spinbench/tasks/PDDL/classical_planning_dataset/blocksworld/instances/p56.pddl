

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 )
(:init
(arm-empty)
(on-table b1)
(on b2 b6)
(on b3 b9)
(on b4 b7)
(on b5 b3)
(on b6 b5)
(on-table b7)
(on b8 b1)
(on b9 b8)
(clear b2)
(clear b4)
)
(:goal
(and
(on b1 b6)
(on b2 b5)
(on b3 b9)
(on b6 b7)
(on b8 b1))
)
)





(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 )
(:init
(arm-empty)
(on b1 b3)
(on b2 b9)
(on-table b3)
(on-table b4)
(on b5 b2)
(on b6 b5)
(on b7 b1)
(on-table b8)
(on-table b9)
(clear b4)
(clear b6)
(clear b7)
(clear b8)
)
(:goal
(and
(on b1 b5)
(on b3 b2)
(on b4 b7)
(on b6 b9)
(on b7 b3)
(on b8 b4)
(on b9 b8))
)
)



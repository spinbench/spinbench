

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 )
(:init
(arm-empty)
(on b1 b4)
(on-table b2)
(on-table b3)
(on-table b4)
(on b5 b1)
(on b6 b8)
(on-table b7)
(on b8 b2)
(on-table b9)
(clear b3)
(clear b5)
(clear b6)
(clear b7)
(clear b9)
)
(:goal
(and
(on b2 b7)
(on b3 b2)
(on b5 b9)
(on b6 b8)
(on b8 b4)
(on b9 b6))
)
)



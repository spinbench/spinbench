

(define (problem BW-rand-10)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 )
(:init
(arm-empty)
(on b1 b3)
(on b2 b4)
(on b3 b8)
(on-table b4)
(on b5 b10)
(on b6 b5)
(on b7 b2)
(on-table b8)
(on b9 b6)
(on b10 b1)
(clear b7)
(clear b9)
)
(:goal
(and
(on b2 b5)
(on b3 b2)
(on b5 b8)
(on b6 b9)
(on b8 b7)
(on b9 b4)
(on b10 b3))
)
)



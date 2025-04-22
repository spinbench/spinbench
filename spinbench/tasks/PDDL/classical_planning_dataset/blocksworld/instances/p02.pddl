

(define (problem BW-rand-10)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 )
(:init
(arm-empty)
(on b1 b2)
(on-table b2)
(on-table b3)
(on b4 b3)
(on b5 b9)
(on b6 b8)
(on b7 b10)
(on b8 b7)
(on-table b9)
(on b10 b4)
(clear b1)
(clear b5)
(clear b6)
)
(:goal
(and
(on b1 b5)
(on b4 b3)
(on b5 b4)
(on b6 b9)
(on b7 b10)
(on b9 b2))
)
)



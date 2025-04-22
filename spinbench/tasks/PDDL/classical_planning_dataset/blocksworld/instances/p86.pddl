

(define (problem BW-rand-10)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 )
(:init
(arm-empty)
(on-table b1)
(on b2 b1)
(on b3 b4)
(on b4 b2)
(on-table b5)
(on-table b6)
(on b7 b9)
(on b8 b3)
(on b9 b10)
(on b10 b8)
(clear b5)
(clear b6)
(clear b7)
)
(:goal
(and
(on b3 b4)
(on b5 b3)
(on b6 b7)
(on b7 b2)
(on b8 b9)
(on b9 b6))
)
)



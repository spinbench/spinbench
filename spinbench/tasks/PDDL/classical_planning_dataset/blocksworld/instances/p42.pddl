

(define (problem BW-rand-11)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 )
(:init
(arm-empty)
(on b1 b5)
(on b2 b8)
(on b3 b7)
(on b4 b9)
(on b5 b3)
(on b6 b4)
(on b7 b11)
(on-table b8)
(on b9 b1)
(on-table b10)
(on b11 b10)
(clear b2)
(clear b6)
)
(:goal
(and
(on b1 b7)
(on b2 b1)
(on b3 b5)
(on b4 b10)
(on b6 b8)
(on b7 b6)
(on b9 b2)
(on b11 b3))
)
)



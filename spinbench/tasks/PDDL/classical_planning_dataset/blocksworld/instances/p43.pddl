

(define (problem BW-rand-13)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 b13 )
(:init
(arm-empty)
(on b1 b9)
(on b2 b11)
(on b3 b1)
(on b4 b7)
(on b5 b13)
(on b6 b5)
(on b7 b8)
(on b8 b2)
(on b9 b4)
(on b10 b6)
(on b11 b12)
(on-table b12)
(on-table b13)
(clear b3)
(clear b10)
)
(:goal
(and
(on b1 b4)
(on b2 b1)
(on b4 b11)
(on b5 b12)
(on b7 b9)
(on b8 b2)
(on b9 b3)
(on b11 b6)
(on b13 b8))
)
)



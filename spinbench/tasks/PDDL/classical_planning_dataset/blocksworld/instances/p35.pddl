

(define (problem BW-rand-13)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 b13 )
(:init
(arm-empty)
(on b1 b11)
(on b2 b12)
(on-table b3)
(on b4 b5)
(on b5 b2)
(on b6 b4)
(on-table b7)
(on b8 b13)
(on b9 b7)
(on b10 b9)
(on b11 b10)
(on-table b12)
(on b13 b6)
(clear b1)
(clear b3)
(clear b8)
)
(:goal
(and
(on b1 b12)
(on b3 b11)
(on b5 b13)
(on b6 b1)
(on b7 b10)
(on b8 b6)
(on b9 b2)
(on b11 b8)
(on b12 b9)
(on b13 b4))
)
)



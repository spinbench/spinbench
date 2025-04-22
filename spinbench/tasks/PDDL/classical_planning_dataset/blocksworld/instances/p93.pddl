

(define (problem BW-rand-13)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 b13 )
(:init
(arm-empty)
(on b1 b10)
(on b2 b4)
(on b3 b11)
(on b4 b5)
(on b5 b13)
(on b6 b12)
(on-table b7)
(on b8 b3)
(on b9 b8)
(on b10 b9)
(on-table b11)
(on-table b12)
(on b13 b6)
(clear b1)
(clear b2)
(clear b7)
)
(:goal
(and
(on b1 b9)
(on b3 b1)
(on b5 b3)
(on b7 b13)
(on b8 b4)
(on b9 b8)
(on b10 b2)
(on b11 b6)
(on b13 b5))
)
)



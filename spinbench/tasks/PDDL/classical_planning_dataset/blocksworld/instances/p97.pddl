

(define (problem BW-rand-13)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 b13 )
(:init
(arm-empty)
(on b1 b11)
(on b2 b8)
(on-table b3)
(on-table b4)
(on-table b5)
(on b6 b4)
(on b7 b3)
(on b8 b9)
(on b9 b13)
(on b10 b12)
(on b11 b5)
(on-table b12)
(on-table b13)
(clear b1)
(clear b2)
(clear b6)
(clear b7)
(clear b10)
)
(:goal
(and
(on b1 b9)
(on b6 b12)
(on b8 b13)
(on b9 b4)
(on b10 b7)
(on b11 b5)
(on b12 b3))
)
)



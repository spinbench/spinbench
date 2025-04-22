

(define (problem BW-rand-12)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 )
(:init
(arm-empty)
(on b1 b4)
(on b2 b5)
(on b3 b9)
(on b4 b3)
(on b5 b1)
(on b6 b11)
(on-table b7)
(on b8 b12)
(on b9 b8)
(on b10 b7)
(on-table b11)
(on b12 b10)
(clear b2)
(clear b6)
)
(:goal
(and
(on b1 b9)
(on b3 b12)
(on b5 b1)
(on b7 b4)
(on b8 b6)
(on b9 b11)
(on b10 b3)
(on b12 b2))
)
)



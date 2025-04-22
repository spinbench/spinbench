

(define (problem BW-rand-12)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 )
(:init
(arm-empty)
(on b1 b7)
(on b2 b12)
(on-table b3)
(on b4 b8)
(on-table b5)
(on b6 b10)
(on b7 b2)
(on-table b8)
(on b9 b1)
(on b10 b11)
(on b11 b9)
(on b12 b3)
(clear b4)
(clear b5)
(clear b6)
)
(:goal
(and
(on b2 b8)
(on b3 b4)
(on b4 b11)
(on b6 b10)
(on b7 b1)
(on b8 b3)
(on b9 b2)
(on b10 b9)
(on b11 b12))
)
)



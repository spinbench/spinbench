

(define (problem BW-rand-12)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 )
(:init
(arm-empty)
(on b1 b9)
(on-table b2)
(on b3 b11)
(on b4 b2)
(on b5 b4)
(on b6 b10)
(on b7 b8)
(on b8 b3)
(on b9 b5)
(on-table b10)
(on-table b11)
(on b12 b6)
(clear b1)
(clear b7)
(clear b12)
)
(:goal
(and
(on b1 b12)
(on b2 b6)
(on b3 b5)
(on b5 b8)
(on b6 b7)
(on b7 b10)
(on b9 b4)
(on b10 b9)
(on b11 b2)
(on b12 b11))
)
)



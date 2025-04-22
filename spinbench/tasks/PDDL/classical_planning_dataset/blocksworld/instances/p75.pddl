

(define (problem BW-rand-12)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 )
(:init
(arm-empty)
(on b1 b4)
(on b2 b10)
(on b3 b2)
(on b4 b11)
(on-table b5)
(on-table b6)
(on b7 b6)
(on b8 b3)
(on b9 b8)
(on b10 b1)
(on b11 b5)
(on b12 b9)
(clear b7)
(clear b12)
)
(:goal
(and
(on b1 b9)
(on b2 b6)
(on b3 b2)
(on b6 b5)
(on b7 b12)
(on b8 b10)
(on b9 b11)
(on b10 b4)
(on b11 b8)
(on b12 b1))
)
)



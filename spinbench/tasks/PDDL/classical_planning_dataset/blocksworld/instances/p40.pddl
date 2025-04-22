

(define (problem BW-rand-12)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 )
(:init
(arm-empty)
(on b1 b6)
(on b2 b1)
(on b3 b10)
(on b4 b9)
(on b5 b11)
(on b6 b8)
(on b7 b5)
(on b8 b12)
(on b9 b2)
(on-table b10)
(on b11 b4)
(on b12 b3)
(clear b7)
)
(:goal
(and
(on b1 b5)
(on b2 b8)
(on b3 b4)
(on b5 b2)
(on b7 b12)
(on b8 b6)
(on b10 b11)
(on b12 b1))
)
)





(define (problem BW-rand-12)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 )
(:init
(arm-empty)
(on b1 b2)
(on b2 b9)
(on b3 b11)
(on b4 b10)
(on b5 b3)
(on b6 b4)
(on-table b7)
(on b8 b12)
(on b9 b6)
(on b10 b7)
(on-table b11)
(on b12 b5)
(clear b1)
(clear b8)
)
(:goal
(and
(on b1 b9)
(on b2 b8)
(on b3 b12)
(on b4 b2)
(on b6 b5)
(on b7 b4)
(on b9 b11)
(on b10 b3)
(on b11 b6)
(on b12 b1))
)
)



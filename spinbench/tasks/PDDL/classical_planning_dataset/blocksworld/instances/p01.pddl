

(define (problem BW-rand-12)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 )
(:init
(arm-empty)
(on b1 b8)
(on b2 b1)
(on-table b3)
(on-table b4)
(on b5 b12)
(on b6 b9)
(on-table b7)
(on b8 b10)
(on b9 b7)
(on b10 b3)
(on b11 b4)
(on b12 b11)
(clear b2)
(clear b5)
(clear b6)
)
(:goal
(and
(on b1 b10)
(on b2 b5)
(on b3 b8)
(on b5 b6)
(on b6 b9)
(on b9 b12)
(on b10 b7)
(on b11 b4)
(on b12 b1))
)
)



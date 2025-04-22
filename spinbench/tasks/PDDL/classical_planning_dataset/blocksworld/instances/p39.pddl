

(define (problem BW-rand-11)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 )
(:init
(arm-empty)
(on b1 b4)
(on b2 b11)
(on b3 b7)
(on b4 b2)
(on b5 b3)
(on-table b6)
(on b7 b9)
(on b8 b1)
(on b9 b8)
(on b10 b6)
(on b11 b10)
(clear b5)
)
(:goal
(and
(on b1 b5)
(on b2 b8)
(on b5 b2)
(on b6 b3)
(on b10 b7)
(on b11 b1))
)
)



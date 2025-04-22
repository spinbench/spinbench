

(define (problem BW-rand-11)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 )
(:init
(arm-empty)
(on b1 b7)
(on b2 b1)
(on b3 b8)
(on b4 b11)
(on b5 b2)
(on-table b6)
(on b7 b4)
(on b8 b9)
(on b9 b10)
(on b10 b5)
(on b11 b6)
(clear b3)
)
(:goal
(and
(on b2 b11)
(on b4 b8)
(on b5 b4)
(on b6 b1)
(on b7 b3)
(on b8 b10)
(on b9 b5))
)
)



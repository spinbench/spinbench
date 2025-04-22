

(define (problem BW-rand-11)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 )
(:init
(arm-empty)
(on b1 b8)
(on b2 b7)
(on-table b3)
(on b4 b2)
(on b5 b1)
(on b6 b5)
(on b7 b11)
(on b8 b3)
(on-table b9)
(on b10 b4)
(on b11 b9)
(clear b6)
(clear b10)
)
(:goal
(and
(on b1 b7)
(on b2 b10)
(on b3 b11)
(on b4 b5)
(on b5 b3)
(on b7 b9)
(on b8 b2)
(on b9 b8)
(on b11 b6))
)
)



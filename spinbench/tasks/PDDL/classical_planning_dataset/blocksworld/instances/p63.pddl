

(define (problem BW-rand-11)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 )
(:init
(arm-empty)
(on-table b1)
(on-table b2)
(on b3 b9)
(on b4 b5)
(on b5 b11)
(on b6 b8)
(on-table b7)
(on b8 b2)
(on b9 b1)
(on b10 b4)
(on b11 b3)
(clear b6)
(clear b7)
(clear b10)
)
(:goal
(and
(on b1 b11)
(on b3 b2)
(on b4 b3)
(on b5 b8)
(on b6 b5)
(on b8 b7)
(on b9 b1)
(on b10 b6))
)
)



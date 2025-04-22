

(define (problem BW-rand-11)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 )
(:init
(arm-empty)
(on b1 b9)
(on-table b2)
(on b3 b5)
(on-table b4)
(on-table b5)
(on b6 b11)
(on b7 b4)
(on-table b8)
(on b9 b10)
(on b10 b6)
(on b11 b2)
(clear b1)
(clear b3)
(clear b7)
(clear b8)
)
(:goal
(and
(on b1 b2)
(on b2 b8)
(on b5 b4)
(on b6 b1)
(on b7 b6)
(on b8 b9)
(on b10 b3)
(on b11 b5))
)
)



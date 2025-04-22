

(define (problem BW-rand-11)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 )
(:init
(arm-empty)
(on b1 b2)
(on-table b2)
(on b3 b5)
(on b4 b9)
(on b5 b7)
(on-table b6)
(on b7 b11)
(on-table b8)
(on-table b9)
(on b10 b8)
(on b11 b4)
(clear b1)
(clear b3)
(clear b6)
(clear b10)
)
(:goal
(and
(on b1 b3)
(on b5 b4)
(on b6 b5)
(on b7 b6)
(on b8 b1)
(on b9 b11)
(on b11 b8))
)
)



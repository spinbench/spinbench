

(define (problem BW-rand-11)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 )
(:init
(arm-empty)
(on-table b1)
(on-table b2)
(on b3 b4)
(on-table b4)
(on b5 b10)
(on-table b6)
(on-table b7)
(on b8 b3)
(on b9 b11)
(on-table b10)
(on b11 b2)
(clear b1)
(clear b5)
(clear b6)
(clear b7)
(clear b8)
(clear b9)
)
(:goal
(and
(on b1 b7)
(on b2 b8)
(on b3 b11)
(on b4 b5)
(on b6 b10)
(on b8 b4)
(on b9 b1)
(on b10 b3))
)
)



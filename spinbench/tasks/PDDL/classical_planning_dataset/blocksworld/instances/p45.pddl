

(define (problem BW-rand-10)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 )
(:init
(arm-empty)
(on b1 b9)
(on b2 b5)
(on b3 b6)
(on-table b4)
(on-table b5)
(on b6 b10)
(on b7 b8)
(on-table b8)
(on b9 b2)
(on b10 b4)
(clear b1)
(clear b3)
(clear b7)
)
(:goal
(and
(on b1 b4)
(on b2 b10)
(on b3 b1)
(on b4 b2)
(on b7 b9)
(on b8 b6)
(on b10 b7))
)
)



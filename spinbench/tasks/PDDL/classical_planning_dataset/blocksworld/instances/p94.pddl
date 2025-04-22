

(define (problem BW-rand-10)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 )
(:init
(arm-empty)
(on-table b1)
(on b2 b8)
(on b3 b6)
(on-table b4)
(on-table b5)
(on-table b6)
(on b7 b4)
(on b8 b7)
(on b9 b3)
(on b10 b2)
(clear b1)
(clear b5)
(clear b9)
(clear b10)
)
(:goal
(and
(on b1 b9)
(on b2 b5)
(on b3 b10)
(on b4 b2)
(on b6 b3)
(on b8 b6)
(on b9 b4)
(on b10 b1))
)
)



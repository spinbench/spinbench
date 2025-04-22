

(define (problem BW-rand-10)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 )
(:init
(arm-empty)
(on-table b1)
(on b2 b5)
(on b3 b9)
(on-table b4)
(on b5 b4)
(on-table b6)
(on-table b7)
(on b8 b1)
(on-table b9)
(on-table b10)
(clear b2)
(clear b3)
(clear b6)
(clear b7)
(clear b8)
(clear b10)
)
(:goal
(and
(on b1 b3)
(on b2 b1)
(on b4 b7)
(on b6 b4)
(on b7 b8)
(on b8 b10)
(on b9 b2)
(on b10 b5))
)
)



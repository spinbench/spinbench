

(define (problem BW-rand-7)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 )
(:init
(arm-empty)
(on b1 b2)
(on b2 b6)
(on b3 b1)
(on b4 b5)
(on b5 b7)
(on b6 b4)
(on-table b7)
(clear b3)
)
(:goal
(and
(on b1 b5)
(on b2 b6)
(on b3 b2)
(on b5 b4)
(on b7 b3))
)
)





(define (problem BW-rand-6)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 )
(:init
(arm-empty)
(on b1 b2)
(on b2 b4)
(on b3 b1)
(on-table b4)
(on b5 b6)
(on b6 b3)
(clear b5)
)
(:goal
(and
(on b2 b3)
(on b3 b4)
(on b5 b1)
(on b6 b2))
)
)



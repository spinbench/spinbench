

(define (problem BW-rand-14)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 b13 b14 )
(:init
(arm-empty)
(on b1 b6)
(on-table b2)
(on-table b3)
(on-table b4)
(on b5 b12)
(on b6 b5)
(on b7 b10)
(on-table b8)
(on b9 b1)
(on b10 b4)
(on b11 b14)
(on b12 b3)
(on b13 b2)
(on b14 b9)
(clear b7)
(clear b8)
(clear b11)
(clear b13)
)
(:goal
(and
(on b1 b9)
(on b2 b5)
(on b3 b7)
(on b4 b11)
(on b5 b10)
(on b6 b3)
(on b8 b13)
(on b9 b8)
(on b10 b4)
(on b12 b2)
(on b13 b14))
)
)



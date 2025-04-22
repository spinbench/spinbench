(define (problem briefcase-o5)
(:domain briefcase)
(:objects l0 l1 l2 l3 l4 l5 - location
          o0 o1 o2 o3 o4 - portable)
(:init
(at o0 l4)
(at o1 l2)
(at o2 l2)
(at o3 l0)
(at o4 l1)
(is-at l5)
)
(:goal
(and
(at o0 l5)
(at o1 l0)
(at o2 l4)
(at o3 l4)
(at o4 l0)
(is-at l3)
)
)
)



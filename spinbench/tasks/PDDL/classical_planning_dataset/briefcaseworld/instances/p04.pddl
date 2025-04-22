(define (problem briefcase-o6)
(:domain briefcase)
(:objects l0 l1 l2 l3 l4 l5 l6 - location
          o0 o1 o2 o3 o4 o5 - portable)
(:init
(at o0 l4)
(at o1 l4)
(at o2 l4)
(at o3 l1)
(at o4 l0)
(at o5 l5)
(is-at l0)
)
(:goal
(and
(at o0 l2)
(at o1 l0)
(at o2 l3)
(at o3 l2)
(at o4 l0)
(at o5 l0)
(is-at l5)
)
)
)



(define (problem briefcase-o8)
(:domain briefcase)
(:objects l0 l1 l2 l3 l4 l5 l6 l7 l8 - location
          o0 o1 o2 o3 o4 o5 o6 o7 - portable)
(:init
(at o0 l2)
(at o1 l7)
(at o2 l6)
(at o3 l6)
(at o4 l0)
(at o5 l6)
(at o6 l2)
(at o7 l0)
(is-at l7)
)
(:goal
(and
(at o0 l1)
(at o1 l5)
(at o2 l0)
(at o3 l2)
(at o4 l3)
(at o5 l2)
(at o6 l0)
(at o7 l3)
(is-at l4)
)
)
)



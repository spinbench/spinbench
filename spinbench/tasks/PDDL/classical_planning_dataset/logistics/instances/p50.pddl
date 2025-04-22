


(define (problem logistics-c1-s4-p2-a1)
(:domain logistics-strips)
(:objects a0 
          c0 
          t0 
          l0-0 l0-1 l0-2 l0-3 
          p0 p1 
)
(:init
    (AIRPLANE a0)
    (CITY c0)
    (TRUCK t0)
    (LOCATION l0-0)
    (in-city  l0-0 c0)
    (LOCATION l0-1)
    (in-city  l0-1 c0)
    (LOCATION l0-2)
    (in-city  l0-2 c0)
    (LOCATION l0-3)
    (in-city  l0-3 c0)
    (AIRPORT l0-0)
    (OBJ p0)
    (OBJ p1)
    (at t0 l0-3)
    (at p0 l0-0)
    (at p1 l0-2)
    (at a0 l0-0)
)
(:goal
    (and
        (at p0 l0-3)
        (at p1 l0-3)
    )
)
)



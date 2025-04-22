


(define (problem logistics-c1-s5-p6-a1)
(:domain logistics-strips)
(:objects a0 
          c0 
          t0 
          l0-0 l0-1 l0-2 l0-3 l0-4 
          p0 p1 p2 p3 p4 p5 
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
    (LOCATION l0-4)
    (in-city  l0-4 c0)
    (AIRPORT l0-0)
    (OBJ p0)
    (OBJ p1)
    (OBJ p2)
    (OBJ p3)
    (OBJ p4)
    (OBJ p5)
    (at t0 l0-3)
    (at p0 l0-0)
    (at p1 l0-4)
    (at p2 l0-3)
    (at p3 l0-1)
    (at p4 l0-2)
    (at p5 l0-2)
    (at a0 l0-0)
)
(:goal
    (and
        (at p0 l0-4)
        (at p1 l0-1)
        (at p2 l0-1)
        (at p3 l0-4)
        (at p4 l0-0)
        (at p5 l0-4)
    )
)
)



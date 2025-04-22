;; he markettrader is a representation of a more general class of
;; real-world trading problems where the aim is to make money through
;; buying, transporting and selling goods.

;; Introduced in
;; Coles, Amanda, M. Fox, and D. Long.
;; "A hybrid LP-RPG heuristic for modelling numeric resource flows in planning."
;; Journal of Artificial Intelligence Research 46 (2013): 343-412.
(define (domain Trader)
(:requirements :typing :fluents) 
(:types market - place 
	camel goods - locatable)

(:predicates (at ?t - camel ?p - place) (can-drive ?from - place ?to - place))

(:functions (on-sale ?g - goods ?m - market)
	    (drive-cost ?p1 ?p2 - place)
	    (price ?g - goods ?m - market)
            (sellprice ?g - goods ?m - market)
	    (bought ?g - goods)
	    (cash)
	    (capacity)
)

(:action travel
 :parameters (?t - camel ?from ?to - market)
 :precondition (and
			(can-drive ?from ?to)
			(>= (cash) (drive-cost ?from ?to))
			(at ?t ?from)
		)
 :effect (and
		(decrease (cash) (drive-cost ?from ?to))
		(at ?t ?to)
		(not (at ?t ?from))
	 )
	  
)


(:action buy
 :parameters (?t - camel ?g - goods ?m - market)
 :precondition (and
                        (at ?t ?m)
		        (<= (+ 7 (price ?g ?m)) (cash))
			(>= (capacity) 1) 
			(> (on-sale ?g ?m) 0)
               )
 :effect (and
              (decrease (capacity) 1)
              (increase (bought ?g) 1)
              (decrease (cash) (price ?g ?m))
        )
)

(:action upgrade
 :parameters (?t - camel)
 :precondition (and
			(>= (cash) 57)
		)
 :effect (and
              (increase (capacity) 20)
	      (decrease (cash) 50))
)




(:action sell
 :parameters (?t - camel ?g - goods ?m - market)
 :precondition (and
			(at ?t ?m)
			(>= (bought ?g) 1) 
		)
 :effect (and
		(increase (capacity) 1)
		(decrease (bought ?g) 1)
	      	(increase (cash) (price ?g ?m))
	)
)

)

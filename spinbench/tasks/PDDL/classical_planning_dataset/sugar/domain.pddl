;; The objective of this domain is to model a problem having to do
;; with producing sugar through industrial processes, refining it from raw cane.
;; 
;; The reference paper is:
;; Coles, Amanda, M. Fox, and D. Long.
;; "A hybrid LP-RPG heuristic for modelling numeric resource flows in planning."
;; Journal of Artificial Intelligence Research 46 (2013): 343-412.
(define (domain supply-chain)
	;(:requirements :typing :fluents :equality)
	(:types 
		 sugar location loader - object
		 brand raw-cane        - sugar
		 mill depot 	       - location
		 truck crane	       - loader
		farm field
	)

	(:predicates
		(available ?m - mill)
		(has-resource ?r - raw-cane ?m - mill)
		(produce ?m - mill ?b - brand)
		(current-process ?m - mill ?b - brand)
		(change-process ?b1 ?b2 - brand)
		(place-order ?r - raw-cane ?m - mill)
		(transport-to ?r - raw-cane  ?m - mill)
		(at-location ?d - loader  ?l - location)
		(connected ?l1 ?l2 - location)
		(busy ?m - mill)
		(ready-crane ?c - crane)
		(service-crane ?c - crane)
	)

	(:functions
		(mill-cost) (cost-process ?m - mill)
		(process-cost ?m - mill)
		(resource-use)
		(unharvest-field)
		(truck-cap ?t - truck)
		(in-truck-sugar ?b - brand ?t - truck)
		(in-storage ?m - location ?b - brand)
		(total-distance)
		(distance ?l1 ?l2 - location)
		(has-resource ?r - raw-cane ?m - mill)
		(max-changing ?m - mill)
		(inventory-cost)
		(changing-product)
		(capacity ?c - crane)
		(max-service-time ?c - crane)
		(service-time ?c - crane)
		(handling-cost)
		(max-produce ?m - mill)
		(labour-cost)
		

	)


	(:action produce_sugar
		:parameters (?r - raw-cane ?m - mill ?b - brand)
		:precondition (and 
				(current-process ?m ?b)
				(available ?m)
				(produce ?m ?b)
				(>(has-resource ?r ?m)0)
				(>(max-changing ?m)0)
		     	     )
		:effect	     (and
				(increase (in-storage ?m ?b)1)
				(decrease (has-resource ?r ?m)1)
				(busy ?m)
				(not(available ?m))
				(increase (mill-cost)(cost-process ?m))
		     	     )
	)


	(:action produce_sugar_max
		:parameters (?r - raw-cane ?m - mill ?b - brand)
		:precondition (and 
				(current-process ?m ?b)
				(available ?m)
				(produce ?m ?b)
			        (>=(has-resource ?r ?m)(max-produce ?m))
				(>(max-changing ?m)0)
		     	     )
		:effect	     (and
				(increase (in-storage ?m ?b)(max-produce ?m))
				(decrease (has-resource ?r ?m)(max-produce ?m))
				(busy ?m)
				(not(available ?m))
				(increase (mill-cost) (* 5 (cost-process ?m)))
		     	     )
	)

	(:action order-sugar-cane
		:parameters (?r - raw-cane ?m - mill )
		:precondition (and
				(>=(has-resource ?r ?m)0)
				(<=(has-resource ?r ?m)0)
			      )
		:effect       (and
				 (place-order ?r ?m)
			      )
	)

	(:action setting-machine
		:parameters (?m - mill)
		:precondition (and
				 (busy ?m)
			      )
		:effect	      (and
				 (not (busy ?m))
				 (available ?m)
			      )
	)
				
	(:action change-product
		:parameters (?m - mill ?b1 - brand ?b2 - brand)
		:precondition (and
				 (current-process ?m ?b1)
				 (change-process ?b1 ?b2)
			      )
		:effect	      (and
				(current-process ?m ?b2)
				(not(current-process ?m ?b1))
				(decrease(max-changing ?m)1)
			      )
	)

	; sugar cane can be obtained from the farm or from other mills

	(:action sugar-cane-farm
		:parameters (?r - raw-cane ?m - mill)
		:precondition (and
				(place-order ?r ?m)
				(>(unharvest-field)0)
			      )
		:effect	      (and
				(decrease (unharvest-field)1)
				(increase (has-resource ?r ?m)5)
				(not (place-order ?r ?m))
				(increase (inventory-cost)10)
			      )
	)

	
	(:action sugar-cane-mills
		:parameters (?r - raw-cane ?m1 ?m2 - mill)
		:precondition (and
				(place-order ?r ?m1)
				(>(has-resource ?r ?m2)0)
			      )
		:effect	      (and
				(increase (has-resource ?r ?m1)1)
				(decrease (has-resource ?r ?m2)1)
				(not (place-order ?r ?m1))
				(decrease(inventory-cost)1)
			      )
	)
		
	(:action load_truck_crane
		:parameters (?b - brand ?t - truck ?l - location ?c - crane)
		:precondition (and 
				 (at-location ?t ?l) 
				 (at-location ?c ?l)
				 (>=(in-storage ?l ?b)(capacity ?c)) 
				 (>=(truck-cap ?t)(capacity ?c)) 
				 (ready-crane ?c)
				
			      )
		:effect      (and
				 (decrease (in-storage ?l ?b)(capacity ?c))
				 (decrease (truck-cap ?t)(capacity ?c))
				 (increase (in-truck-sugar ?b ?t)(capacity ?c)) 
				 (increase (handling-cost)10)
				
			    )
	)

	(:action check-service
		:parameters (?c - crane ?l - location)
		:precondition (and
				 (at-location ?c ?l)
				 (>=(service-time ?c)0)
				 (<=(service-time ?c)0)
			      )
		:effect	      (and 
				 (not(ready-crane ?c))
				     (service-crane ?c)
				     (increase(service-time ?c)(max-service-time ?c))
			      )
	)		
	
	(:action maintainence-crane
		:parameters (?c - crane ?l - location)
		:precondition (and
				 (at-location ?c ?l)
				 (service-crane ?c)
			      )
		:effect	     (and
				(ready-crane ?c)
			     )
	)			
	
	(:action load-truck-manual
		:parameters (?b - brand ?t - truck ?l - location)
		:precondition (and 
				 (at-location ?t ?l) 
				 (>(in-storage ?l ?b)0)
				 (>(truck-cap ?t)0) 
				 
			      )
		:effect      (and
				 (decrease (in-storage ?l ?b)1)
				 (decrease (truck-cap ?t)1)
				 (increase (in-truck-sugar ?b ?t)1)
				 (increase (handling-cost)1)
			    )
	)

	(:action drive_truck
		:parameters (?t - truck ?y1 ?y2 - location)
		:precondition	(and
				     (at-location  ?t ?y1)
				     (connected ?y1 ?y2)
				)
		:effect 	(and (at-location ?t ?y2)
				     (not(at-location ?t ?y1))
				)	
	)

	(:action unload_truck
		:parameters (?b - brand ?t - truck ?l - location)
		:precondition (and 
				(at-location ?t ?l) 
				(>(in-truck-sugar ?b ?t)0)
			      )
		:effect (and 
			      	(increase (in-storage ?l ?b)1)
				(decrease (in-truck-sugar ?b ?t)1)
				(increase (truck-cap ?t)1)
			)
	)

)

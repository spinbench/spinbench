(define (problem prob1)
	(:domain supply-chain)
	
	(:objects
		brand1 brand2 brand3 brand4 	- brand
		sugar-cane		    	- raw-cane
		truck1 truck2  			- truck
		depot1 depot2 depot3 		- depot
		mill1 mill2 mill3 		- mill
		crane1 crane2 crane3		- crane
	)

	(:init
		(=(unharvest-field)3) (=(mill-cost)0) (=(inventory-cost)0) (=(handling-cost)0)(=(labour-cost)0)
		(=(cost-process mill1)1) (=(cost-process mill2)3) (=(cost-process mill3)6)
		(=(has-resource sugar-cane mill1)0) (=(has-resource sugar-cane mill2)10) (=(has-resource sugar-cane mill3)10)
		(=(max-changing mill1)2) (=(max-changing mill2)2) (=(max-changing mill3 )2)
		(=(max-produce mill1)5) (=(max-produce mill2)8) (=(max-produce mill3)10)
		(available mill1)   (available mill2) (available mill3)

		(produce mill1 brand1) (produce mill1 brand3) (produce mill1 brand4) (current-process mill1 brand1)
		(produce mill2 brand2) (produce mill2 brand3) (produce mill2 brand4) (current-process mill2 brand3)
		(produce mill3 brand2) (produce mill3 brand1) (current-process mill3 brand1)
		(=(in-storage mill1 brand1)0) (=(in-storage mill1 brand3)0) (=(in-storage mill1 brand4)0)
		(=(in-storage mill2 brand1)0) (=(in-storage mill2 brand2)0) (=(in-storage mill2 brand3)0)
		(=(in-storage mill3 brand1)0) (=(in-storage mill3 brand2)0) (=(in-storage mill3 brand4)2)

		(change-process brand1 brand2) (change-process brand1 brand3) (change-process brand1 brand4)
		(change-process brand2 brand1) (change-process brand2 brand3) (change-process brand2 brand4)
		(change-process brand3 brand1) (change-process brand3 brand2) (change-process brand3 brand4)
		(change-process brand4 brand1) (change-process brand4 brand2) (change-process brand4 brand3)

		(at-location truck1 depot1 ) (at-location truck2 depot2 ) 
		(=(truck-cap truck1)10) (=(truck-cap truck2)6) 
		(at-location crane1 mill1 )   (at-location  crane2  mill2) (at-location crane3 mill3 ) 
		(ready-crane crane1) (ready-crane crane2) (ready-crane crane3)
		(=(capacity crane1)5) (=(capacity crane2)5) (=(capacity crane3)5)
		(=(service-time crane1)10) (=(service-time crane2)15) (=(service-time crane3)10)
		(=(max-service-time crane1)10) (=(max-service-time crane2)15) (=(max-service-time crane3)10)
		(=(in-truck-sugar brand1 truck1)0) 
		(=(in-truck-sugar brand2 truck1)0) 
		(=(in-truck-sugar brand3 truck1)0) 
		(=(in-truck-sugar brand4 truck1)0) 
		(=(in-truck-sugar brand1 truck2)0) 
		(=(in-truck-sugar brand2 truck2)0) 
		(=(in-truck-sugar brand3 truck2)0) 
		(=(in-truck-sugar brand4 truck2)0)
		
		(=(in-storage depot1 brand1)0) (=(in-storage depot1 brand2)0) (=(in-storage depot1 brand3)0) (=(in-storage depot1 brand4)0)
		(=(in-storage depot2 brand1)0) (=(in-storage depot2 brand2)0) (=(in-storage depot2 brand3)0) (=(in-storage depot2 brand4)0)
		(=(in-storage depot3 brand1)0) (=(in-storage depot3 brand2)0) (=(in-storage depot3 brand3)0) (=(in-storage depot3 brand4)0)

		(connected mill1 mill2) (connected mill2 mill1) 
		(connected mill1 mill3) (connected mill3 mill1) 
		(connected mill2 mill3) (connected mill3 mill2) 

		(connected mill1 depot1) (connected depot1 mill1) 
		(connected mill1 depot2) (connected depot2 mill1) 
		(connected mill1 depot3) (connected depot3 mill1) 

		(connected mill2 depot2) (connected depot2 mill2) 
		(connected mill2 depot3) (connected depot3 mill2) 
		(connected mill2 depot1) (connected depot1 mill2) 

		(connected mill3 depot1) (connected depot1 mill3) 
		(connected mill3 depot2) (connected depot2 mill3) 
		(connected mill3 depot3) (connected depot3 mill3) 

		(connected depot3 depot1) (connected depot1 depot3) 
		(connected depot3 depot2) (connected depot2 depot3) 
		(connected depot1 depot2) (connected depot2 depot1) 
		
	
	)
	(:goal (and
		 (>=(in-storage depot1 brand4)4)
		 (>=(in-storage depot2 brand4)4)
		)
	)

	

)

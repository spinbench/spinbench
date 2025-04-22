(define (problem settlers)
(:domain civ)
(:objects
        location0 - place
        location1 - place
        location2 - place
        location3 - place
        vehicle0 - vehicle
        vehicle1 - vehicle
        vehicle2 - vehicle
        vehicle3 - vehicle
	vehicle4 - vehicle
        vehicle5 - vehicle
        vehicle6 - vehicle
)
(:init
        (= (resource-use) 0)
        (= (labour) 0)
        (= (pollution) 0)
        (woodland location3)
        (mountain location2)
        (by-coast location0)
        (metalliferous location0)
        (= (housing location0) 0)
        (= (available wood location0) 0)
	(= (carts-at location0) 0)
        (= (available timber location0) 0)
        (= (available ore location0) 0)
        (= (available stone location0) 0)
        (= (available iron location0) 0)
        (= (available coal location0) 0)

        (= (housing location2) 0)
        (= (available wood location2)  0)
	(= (carts-at location2) 0)
        (= (available timber location2) 0)
        (= (available ore location2) 0)
        (= (available stone location2) 0)
        (= (available iron location2) 0)
        (= (available coal location2) 0)


        (= (housing location3) 0)
        (= (available wood location3)  0)
	(= (carts-at location3) 0)
        (= (available timber location3) 0)
        (= (available ore location3) 0)
        (= (available stone location3) 0)
        (= (available iron location3) 0)
        (= (available coal location3) 0)

	(by-coast location1)
        (= (housing location1) 0)
        (= (available wood location1)  0)
	(= (carts-at location1) 0)
        (= (available timber location1) 0)
        (= (available ore location1) 0)
        (= (available stone location1) 0)
        (= (available iron location1) 0)
        (= (available coal location1) 0)
	(connected-by-sea location1 location0)
	(connected-by-sea location0 location1)
	(connected-by-land location0 location2)
	(connected-by-land location2 location0)
	(connected-by-land location3 location2)
	(connected-by-land location2 location3)
	(connected-by-land location0 location3)
	(connected-by-land location3 location0)
        (potential vehicle0)
        (potential vehicle1)
	(potential vehicle2)
        (potential vehicle3)
        (potential vehicle4)
	(potential vehicle5)
        (potential vehicle6)
)
(:goal (and
        (>= (available timber location1) 1)
	;(connected-by-rail location0 location3)
	;(has-coal-stack location3)
	;(>= (housing location0) 1)
        )
)

(:metric minimize (+ (+ (* 0 (pollution)) (* 3 (resource-use))) (* 3 (labour))))
)


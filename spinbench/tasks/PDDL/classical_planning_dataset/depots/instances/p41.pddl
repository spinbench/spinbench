(define (problem depot-1-2-2-3-3-4) (:domain depots)
(:objects
	depot0 - Depot
	distributor0 distributor1 - Distributor
	truck0 truck1 - Truck
	pallet0 pallet1 pallet2 - Pallet
	crate0 crate1 crate2 crate3 - Crate
	hoist0 hoist1 hoist2 - Hoist)
(:init
	(at pallet0 depot0)
	(clear crate3)
	(at pallet1 distributor0)
	(clear pallet1)
	(at pallet2 distributor1)
	(clear crate2)
	(at truck0 distributor1)
	(at truck1 distributor0)
	(at hoist0 depot0)
	(available hoist0)
	(at hoist1 distributor0)
	(available hoist1)
	(at hoist2 distributor1)
	(available hoist2)
	(at crate0 depot0)
	(on crate0 pallet0)
	(at crate1 depot0)
	(on crate1 crate0)
	(at crate2 distributor1)
	(on crate2 pallet2)
	(at crate3 depot0)
	(on crate3 crate1)
)

(:goal (and
		(on crate0 crate2)
		(on crate1 pallet1)
		(on crate2 pallet2)
	)
))

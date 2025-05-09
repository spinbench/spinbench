(define (problem depot-1-3-5-7-7-9) (:domain depots)
(:objects
	depot0 - Depot
	distributor0 distributor1 distributor2 - Distributor
	truck0 truck1 truck2 truck3 truck4 - Truck
	pallet0 pallet1 pallet2 pallet3 pallet4 pallet5 pallet6 - Pallet
	crate0 crate1 crate2 crate3 crate4 crate5 crate6 crate7 crate8 - Crate
	hoist0 hoist1 hoist2 hoist3 hoist4 hoist5 hoist6 - Hoist)
(:init
	(at pallet0 depot0)
	(clear crate7)
	(at pallet1 distributor0)
	(clear crate8)
	(at pallet2 distributor1)
	(clear crate3)
	(at pallet3 distributor2)
	(clear pallet3)
	(at pallet4 depot0)
	(clear crate2)
	(at pallet5 depot0)
	(clear crate6)
	(at pallet6 distributor1)
	(clear crate4)
	(at truck0 distributor0)
	(at truck1 depot0)
	(at truck2 distributor2)
	(at truck3 distributor0)
	(at truck4 distributor2)
	(at hoist0 depot0)
	(available hoist0)
	(at hoist1 distributor0)
	(available hoist1)
	(at hoist2 distributor1)
	(available hoist2)
	(at hoist3 distributor2)
	(available hoist3)
	(at hoist4 depot0)
	(available hoist4)
	(at hoist5 depot0)
	(available hoist5)
	(at hoist6 distributor1)
	(available hoist6)
	(at crate0 depot0)
	(on crate0 pallet0)
	(at crate1 depot0)
	(on crate1 pallet4)
	(at crate2 depot0)
	(on crate2 crate1)
	(at crate3 distributor1)
	(on crate3 pallet2)
	(at crate4 distributor1)
	(on crate4 pallet6)
	(at crate5 distributor0)
	(on crate5 pallet1)
	(at crate6 depot0)
	(on crate6 pallet5)
	(at crate7 depot0)
	(on crate7 crate0)
	(at crate8 distributor0)
	(on crate8 crate5)
)

(:goal (and
		(on crate0 crate4)
		(on crate1 pallet4)
		(on crate2 pallet0)
		(on crate3 crate0)
		(on crate4 crate8)
		(on crate6 pallet6)
		(on crate7 pallet1)
		(on crate8 crate2)
	)
))

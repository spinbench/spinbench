(define (problem depot-3-4-4-7-7-7) (:domain depots)
(:objects
	depot0 depot1 depot2 - Depot
	distributor0 distributor1 distributor2 distributor3 - Distributor
	truck0 truck1 truck2 truck3 - Truck
	pallet0 pallet1 pallet2 pallet3 pallet4 pallet5 pallet6 - Pallet
	crate0 crate1 crate2 crate3 crate4 crate5 crate6 - Crate
	hoist0 hoist1 hoist2 hoist3 hoist4 hoist5 hoist6 - Hoist)
(:init
	(at pallet0 depot0)
	(clear pallet0)
	(at pallet1 depot1)
	(clear pallet1)
	(at pallet2 depot2)
	(clear pallet2)
	(at pallet3 distributor0)
	(clear crate3)
	(at pallet4 distributor1)
	(clear crate5)
	(at pallet5 distributor2)
	(clear crate6)
	(at pallet6 distributor3)
	(clear pallet6)
	(at truck0 distributor0)
	(at truck1 distributor2)
	(at truck2 depot1)
	(at truck3 distributor1)
	(at hoist0 depot0)
	(available hoist0)
	(at hoist1 depot1)
	(available hoist1)
	(at hoist2 depot2)
	(available hoist2)
	(at hoist3 distributor0)
	(available hoist3)
	(at hoist4 distributor1)
	(available hoist4)
	(at hoist5 distributor2)
	(available hoist5)
	(at hoist6 distributor3)
	(available hoist6)
	(at crate0 distributor2)
	(on crate0 pallet5)
	(at crate1 distributor0)
	(on crate1 pallet3)
	(at crate2 distributor2)
	(on crate2 crate0)
	(at crate3 distributor0)
	(on crate3 crate1)
	(at crate4 distributor2)
	(on crate4 crate2)
	(at crate5 distributor1)
	(on crate5 pallet4)
	(at crate6 distributor2)
	(on crate6 crate4)
)

(:goal (and
		(on crate0 pallet6)
		(on crate1 crate2)
		(on crate2 pallet2)
		(on crate3 pallet4)
		(on crate5 crate1)
		(on crate6 pallet0)
	)
))

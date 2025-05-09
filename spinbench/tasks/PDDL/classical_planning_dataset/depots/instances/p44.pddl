(define (problem depot-3-2-4-9-9-11) (:domain depots)
(:objects
	depot0 depot1 depot2 - Depot
	distributor0 distributor1 - Distributor
	truck0 truck1 truck2 truck3 - Truck
	pallet0 pallet1 pallet2 pallet3 pallet4 pallet5 pallet6 pallet7 pallet8 - Pallet
	crate0 crate1 crate2 crate3 crate4 crate5 crate6 crate7 crate8 crate9 crate10 - Crate
	hoist0 hoist1 hoist2 hoist3 hoist4 hoist5 hoist6 hoist7 hoist8 - Hoist)
(:init
	(at pallet0 depot0)
	(clear pallet0)
	(at pallet1 depot1)
	(clear pallet1)
	(at pallet2 depot2)
	(clear crate9)
	(at pallet3 distributor0)
	(clear crate7)
	(at pallet4 distributor1)
	(clear pallet4)
	(at pallet5 distributor1)
	(clear crate10)
	(at pallet6 distributor0)
	(clear crate5)
	(at pallet7 distributor1)
	(clear pallet7)
	(at pallet8 distributor0)
	(clear crate8)
	(at truck0 depot2)
	(at truck1 depot2)
	(at truck2 distributor1)
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
	(at hoist5 depot2)
	(available hoist5)
	(at hoist6 depot0)
	(available hoist6)
	(at hoist7 distributor1)
	(available hoist7)
	(at hoist8 depot0)
	(available hoist8)
	(at crate0 distributor0)
	(on crate0 pallet8)
	(at crate1 distributor0)
	(on crate1 pallet3)
	(at crate2 distributor1)
	(on crate2 pallet5)
	(at crate3 distributor0)
	(on crate3 crate0)
	(at crate4 distributor1)
	(on crate4 crate2)
	(at crate5 distributor0)
	(on crate5 pallet6)
	(at crate6 depot2)
	(on crate6 pallet2)
	(at crate7 distributor0)
	(on crate7 crate1)
	(at crate8 distributor0)
	(on crate8 crate3)
	(at crate9 depot2)
	(on crate9 crate6)
	(at crate10 distributor1)
	(on crate10 crate4)
)

(:goal (and
		(on crate0 crate3)
		(on crate2 pallet6)
		(on crate3 pallet3)
		(on crate4 crate5)
		(on crate5 pallet5)
		(on crate6 pallet7)
		(on crate7 pallet8)
		(on crate9 pallet1)
		(on crate10 pallet0)
	)
))

(define (problem depot-5-6-7-11-11-12) (:domain depots)
(:objects
	depot0 depot1 depot2 depot3 depot4 - Depot
	distributor0 distributor1 distributor2 distributor3 distributor4 distributor5 - Distributor
	truck0 truck1 truck2 truck3 truck4 truck5 truck6 - Truck
	pallet0 pallet1 pallet2 pallet3 pallet4 pallet5 pallet6 pallet7 pallet8 pallet9 pallet10 - Pallet
	crate0 crate1 crate2 crate3 crate4 crate5 crate6 crate7 crate8 crate9 crate10 crate11 - Crate
	hoist0 hoist1 hoist2 hoist3 hoist4 hoist5 hoist6 hoist7 hoist8 hoist9 hoist10 - Hoist)
(:init
	(at pallet0 depot0)
	(clear crate6)
	(at pallet1 depot1)
	(clear crate11)
	(at pallet2 depot2)
	(clear pallet2)
	(at pallet3 depot3)
	(clear pallet3)
	(at pallet4 depot4)
	(clear crate4)
	(at pallet5 distributor0)
	(clear crate7)
	(at pallet6 distributor1)
	(clear crate3)
	(at pallet7 distributor2)
	(clear crate10)
	(at pallet8 distributor3)
	(clear crate9)
	(at pallet9 distributor4)
	(clear crate5)
	(at pallet10 distributor5)
	(clear pallet10)
	(at truck0 depot1)
	(at truck1 depot4)
	(at truck2 distributor4)
	(at truck3 distributor3)
	(at truck4 depot1)
	(at truck5 distributor0)
	(at truck6 depot4)
	(at hoist0 depot0)
	(available hoist0)
	(at hoist1 depot1)
	(available hoist1)
	(at hoist2 depot2)
	(available hoist2)
	(at hoist3 depot3)
	(available hoist3)
	(at hoist4 depot4)
	(available hoist4)
	(at hoist5 distributor0)
	(available hoist5)
	(at hoist6 distributor1)
	(available hoist6)
	(at hoist7 distributor2)
	(available hoist7)
	(at hoist8 distributor3)
	(available hoist8)
	(at hoist9 distributor4)
	(available hoist9)
	(at hoist10 distributor5)
	(available hoist10)
	(at crate0 depot1)
	(on crate0 pallet1)
	(at crate1 distributor2)
	(on crate1 pallet7)
	(at crate2 distributor3)
	(on crate2 pallet8)
	(at crate3 distributor1)
	(on crate3 pallet6)
	(at crate4 depot4)
	(on crate4 pallet4)
	(at crate5 distributor4)
	(on crate5 pallet9)
	(at crate6 depot0)
	(on crate6 pallet0)
	(at crate7 distributor0)
	(on crate7 pallet5)
	(at crate8 distributor2)
	(on crate8 crate1)
	(at crate9 distributor3)
	(on crate9 crate2)
	(at crate10 distributor2)
	(on crate10 crate8)
	(at crate11 depot1)
	(on crate11 crate0)
)

(:goal (and
		(on crate0 crate5)
		(on crate1 pallet2)
		(on crate3 pallet0)
		(on crate4 pallet1)
		(on crate5 pallet7)
		(on crate6 pallet4)
		(on crate7 pallet5)
		(on crate8 crate3)
		(on crate9 crate6)
		(on crate10 pallet3)
		(on crate11 crate9)
	)
))

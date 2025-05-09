(define (problem depot-5-7-8-12-12-11) (:domain depots)
(:objects
	depot0 depot1 depot2 depot3 depot4 - Depot
	distributor0 distributor1 distributor2 distributor3 distributor4 distributor5 distributor6 - Distributor
	truck0 truck1 truck2 truck3 truck4 truck5 truck6 truck7 - Truck
	pallet0 pallet1 pallet2 pallet3 pallet4 pallet5 pallet6 pallet7 pallet8 pallet9 pallet10 pallet11 - Pallet
	crate0 crate1 crate2 crate3 crate4 crate5 crate6 crate7 crate8 crate9 crate10 - Crate
	hoist0 hoist1 hoist2 hoist3 hoist4 hoist5 hoist6 hoist7 hoist8 hoist9 hoist10 hoist11 - Hoist)
(:init
	(at pallet0 depot0)
	(clear pallet0)
	(at pallet1 depot1)
	(clear pallet1)
	(at pallet2 depot2)
	(clear crate3)
	(at pallet3 depot3)
	(clear crate1)
	(at pallet4 depot4)
	(clear crate4)
	(at pallet5 distributor0)
	(clear crate5)
	(at pallet6 distributor1)
	(clear crate10)
	(at pallet7 distributor2)
	(clear pallet7)
	(at pallet8 distributor3)
	(clear crate9)
	(at pallet9 distributor4)
	(clear crate6)
	(at pallet10 distributor5)
	(clear crate7)
	(at pallet11 distributor6)
	(clear crate8)
	(at truck0 distributor6)
	(at truck1 distributor0)
	(at truck2 depot3)
	(at truck3 depot0)
	(at truck4 distributor3)
	(at truck5 distributor6)
	(at truck6 distributor6)
	(at truck7 distributor4)
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
	(at hoist11 distributor6)
	(available hoist11)
	(at crate0 distributor1)
	(on crate0 pallet6)
	(at crate1 depot3)
	(on crate1 pallet3)
	(at crate2 distributor0)
	(on crate2 pallet5)
	(at crate3 depot2)
	(on crate3 pallet2)
	(at crate4 depot4)
	(on crate4 pallet4)
	(at crate5 distributor0)
	(on crate5 crate2)
	(at crate6 distributor4)
	(on crate6 pallet9)
	(at crate7 distributor5)
	(on crate7 pallet10)
	(at crate8 distributor6)
	(on crate8 pallet11)
	(at crate9 distributor3)
	(on crate9 pallet8)
	(at crate10 distributor1)
	(on crate10 crate0)
)

(:goal (and
		(on crate0 pallet5)
		(on crate1 pallet2)
		(on crate2 crate4)
		(on crate4 pallet6)
		(on crate5 pallet4)
		(on crate6 crate5)
		(on crate7 crate9)
		(on crate8 pallet8)
		(on crate9 pallet9)
		(on crate10 pallet3)
	)
))

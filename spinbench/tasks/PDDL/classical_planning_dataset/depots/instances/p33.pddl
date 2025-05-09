(define (problem depot-5-6-7-11-11-20) (:domain depots)
(:objects
	depot0 depot1 depot2 depot3 depot4 - Depot
	distributor0 distributor1 distributor2 distributor3 distributor4 distributor5 - Distributor
	truck0 truck1 truck2 truck3 truck4 truck5 truck6 - Truck
	pallet0 pallet1 pallet2 pallet3 pallet4 pallet5 pallet6 pallet7 pallet8 pallet9 pallet10 - Pallet
	crate0 crate1 crate2 crate3 crate4 crate5 crate6 crate7 crate8 crate9 crate10 crate11 crate12 crate13 crate14 crate15 crate16 crate17 crate18 crate19 - Crate
	hoist0 hoist1 hoist2 hoist3 hoist4 hoist5 hoist6 hoist7 hoist8 hoist9 hoist10 - Hoist)
(:init
	(at pallet0 depot0)
	(clear crate6)
	(at pallet1 depot1)
	(clear crate13)
	(at pallet2 depot2)
	(clear crate18)
	(at pallet3 depot3)
	(clear crate8)
	(at pallet4 depot4)
	(clear crate12)
	(at pallet5 distributor0)
	(clear crate1)
	(at pallet6 distributor1)
	(clear pallet6)
	(at pallet7 distributor2)
	(clear pallet7)
	(at pallet8 distributor3)
	(clear crate19)
	(at pallet9 distributor4)
	(clear crate17)
	(at pallet10 distributor5)
	(clear crate10)
	(at truck0 depot3)
	(at truck1 distributor5)
	(at truck2 distributor2)
	(at truck3 depot1)
	(at truck4 distributor3)
	(at truck5 distributor4)
	(at truck6 distributor5)
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
	(at crate0 distributor0)
	(on crate0 pallet5)
	(at crate1 distributor0)
	(on crate1 crate0)
	(at crate2 distributor3)
	(on crate2 pallet8)
	(at crate3 depot4)
	(on crate3 pallet4)
	(at crate4 depot0)
	(on crate4 pallet0)
	(at crate5 depot4)
	(on crate5 crate3)
	(at crate6 depot0)
	(on crate6 crate4)
	(at crate7 depot3)
	(on crate7 pallet3)
	(at crate8 depot3)
	(on crate8 crate7)
	(at crate9 depot2)
	(on crate9 pallet2)
	(at crate10 distributor5)
	(on crate10 pallet10)
	(at crate11 distributor4)
	(on crate11 pallet9)
	(at crate12 depot4)
	(on crate12 crate5)
	(at crate13 depot1)
	(on crate13 pallet1)
	(at crate14 distributor4)
	(on crate14 crate11)
	(at crate15 distributor3)
	(on crate15 crate2)
	(at crate16 distributor4)
	(on crate16 crate14)
	(at crate17 distributor4)
	(on crate17 crate16)
	(at crate18 depot2)
	(on crate18 crate9)
	(at crate19 distributor3)
	(on crate19 crate15)
)

(:goal (and
		(on crate0 crate3)
		(on crate1 crate16)
		(on crate2 pallet1)
		(on crate3 pallet6)
		(on crate4 pallet2)
		(on crate5 pallet5)
		(on crate7 crate19)
		(on crate9 crate11)
		(on crate10 crate12)
		(on crate11 crate5)
		(on crate12 crate2)
		(on crate13 crate14)
		(on crate14 pallet9)
		(on crate15 crate7)
		(on crate16 pallet8)
		(on crate17 pallet0)
		(on crate19 pallet7)
	)
))

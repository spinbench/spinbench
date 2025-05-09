(define (problem depot-1-4-8-15-15-17) (:domain depots)
(:objects
	depot0 - Depot
	distributor0 distributor1 distributor2 distributor3 - Distributor
	truck0 truck1 truck2 truck3 truck4 truck5 truck6 truck7 - Truck
	pallet0 pallet1 pallet2 pallet3 pallet4 pallet5 pallet6 pallet7 pallet8 pallet9 pallet10 pallet11 pallet12 pallet13 pallet14 - Pallet
	crate0 crate1 crate2 crate3 crate4 crate5 crate6 crate7 crate8 crate9 crate10 crate11 crate12 crate13 crate14 crate15 crate16 - Crate
	hoist0 hoist1 hoist2 hoist3 hoist4 hoist5 hoist6 hoist7 hoist8 hoist9 hoist10 hoist11 hoist12 hoist13 hoist14 - Hoist)
(:init
	(at pallet0 depot0)
	(clear crate9)
	(at pallet1 distributor0)
	(clear pallet1)
	(at pallet2 distributor1)
	(clear crate11)
	(at pallet3 distributor2)
	(clear crate0)
	(at pallet4 distributor3)
	(clear crate5)
	(at pallet5 distributor1)
	(clear crate12)
	(at pallet6 distributor1)
	(clear crate14)
	(at pallet7 distributor1)
	(clear pallet7)
	(at pallet8 distributor2)
	(clear crate8)
	(at pallet9 distributor3)
	(clear crate16)
	(at pallet10 distributor0)
	(clear pallet10)
	(at pallet11 distributor1)
	(clear crate15)
	(at pallet12 distributor2)
	(clear crate10)
	(at pallet13 depot0)
	(clear crate7)
	(at pallet14 distributor3)
	(clear crate13)
	(at truck0 distributor0)
	(at truck1 distributor1)
	(at truck2 distributor1)
	(at truck3 distributor1)
	(at truck4 distributor2)
	(at truck5 distributor0)
	(at truck6 distributor1)
	(at truck7 distributor0)
	(at hoist0 depot0)
	(available hoist0)
	(at hoist1 distributor0)
	(available hoist1)
	(at hoist2 distributor1)
	(available hoist2)
	(at hoist3 distributor2)
	(available hoist3)
	(at hoist4 distributor3)
	(available hoist4)
	(at hoist5 distributor2)
	(available hoist5)
	(at hoist6 distributor3)
	(available hoist6)
	(at hoist7 depot0)
	(available hoist7)
	(at hoist8 distributor3)
	(available hoist8)
	(at hoist9 distributor1)
	(available hoist9)
	(at hoist10 depot0)
	(available hoist10)
	(at hoist11 depot0)
	(available hoist11)
	(at hoist12 distributor0)
	(available hoist12)
	(at hoist13 distributor3)
	(available hoist13)
	(at hoist14 distributor3)
	(available hoist14)
	(at crate0 distributor2)
	(on crate0 pallet3)
	(at crate1 depot0)
	(on crate1 pallet0)
	(at crate2 distributor2)
	(on crate2 pallet8)
	(at crate3 distributor1)
	(on crate3 pallet2)
	(at crate4 distributor2)
	(on crate4 pallet12)
	(at crate5 distributor3)
	(on crate5 pallet4)
	(at crate6 distributor3)
	(on crate6 pallet9)
	(at crate7 depot0)
	(on crate7 pallet13)
	(at crate8 distributor2)
	(on crate8 crate2)
	(at crate9 depot0)
	(on crate9 crate1)
	(at crate10 distributor2)
	(on crate10 crate4)
	(at crate11 distributor1)
	(on crate11 crate3)
	(at crate12 distributor1)
	(on crate12 pallet5)
	(at crate13 distributor3)
	(on crate13 pallet14)
	(at crate14 distributor1)
	(on crate14 pallet6)
	(at crate15 distributor1)
	(on crate15 pallet11)
	(at crate16 distributor3)
	(on crate16 crate6)
)

(:goal (and
		(on crate0 crate3)
		(on crate1 crate2)
		(on crate2 pallet8)
		(on crate3 pallet13)
		(on crate4 crate8)
		(on crate5 crate7)
		(on crate6 crate10)
		(on crate7 pallet12)
		(on crate8 pallet10)
		(on crate9 crate1)
		(on crate10 pallet7)
		(on crate11 pallet2)
		(on crate12 pallet0)
		(on crate13 pallet3)
		(on crate15 pallet4)
		(on crate16 pallet11)
	)
))

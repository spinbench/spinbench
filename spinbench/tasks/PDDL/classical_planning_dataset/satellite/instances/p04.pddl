(define (problem strips-sat-x-1)
(:domain satellite)
(:objects
	satellite0 - satellite
	instrument0 - instrument
	instrument1 - instrument
	image3 - mode
	infrared1 - mode
	thermograph0 - mode
	infrared2 - mode
	GroundStation1 - direction
	Star0 - direction
	Phenomenon2 - direction
	Phenomenon3 - direction
	Star4 - direction
	Star5 - direction
	Star6 - direction
	Phenomenon7 - direction
	Star8 - direction
	Phenomenon9 - direction
	Star10 - direction
)
(:init
	(supports instrument0 image3)
	(calibration_target instrument0 GroundStation1)
	(supports instrument1 thermograph0)
	(supports instrument1 infrared2)
	(supports instrument1 infrared1)
	(calibration_target instrument1 Star0)
	(on_board instrument0 satellite0)
	(on_board instrument1 satellite0)
	(power_avail satellite0)
	(pointing satellite0 Star10)
)
(:goal (and
	(pointing satellite0 Star10)
	(have_image Phenomenon2 image3)
	(have_image Phenomenon3 infrared2)
	(have_image Star4 image3)
	(have_image Star5 image3)
	(have_image Star6 infrared2)
	(have_image Phenomenon7 infrared2)
	(have_image Star8 infrared1)
	(have_image Phenomenon9 image3)
	(have_image Star10 image3)
))

)

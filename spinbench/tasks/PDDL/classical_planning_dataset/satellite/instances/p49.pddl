(define (problem strips-sat-x-1)
(:domain satellite)
(:objects
	satellite0 - satellite
	instrument0 - instrument
	instrument1 - instrument
	instrument2 - instrument
	infrared1 - mode
	infrared0 - mode
	image2 - mode
	Star0 - direction
	GroundStation2 - direction
	Star3 - direction
	Star4 - direction
	GroundStation5 - direction
	GroundStation6 - direction
	GroundStation9 - direction
	Star7 - direction
	GroundStation8 - direction
	GroundStation1 - direction
	Planet10 - direction
	Planet11 - direction
	Phenomenon12 - direction
)
(:init
	(supports instrument0 infrared1)
	(calibration_target instrument0 GroundStation6)
	(supports instrument1 infrared0)
	(supports instrument1 image2)
	(calibration_target instrument1 Star7)
	(calibration_target instrument1 GroundStation9)
	(supports instrument2 infrared1)
	(supports instrument2 infrared0)
	(supports instrument2 image2)
	(calibration_target instrument2 GroundStation1)
	(calibration_target instrument2 GroundStation8)
	(on_board instrument0 satellite0)
	(on_board instrument1 satellite0)
	(on_board instrument2 satellite0)
	(power_avail satellite0)
	(pointing satellite0 Phenomenon12)
)
(:goal (and
	(pointing satellite0 GroundStation1)
	(have_image Planet10 infrared1)
	(have_image Planet11 infrared1)
	(have_image Phenomenon12 infrared0)
))

)

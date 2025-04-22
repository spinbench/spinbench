(define (problem strips-sat-x-1)
(:domain satellite)
(:objects
	satellite0 - satellite
	instrument0 - instrument
	instrument1 - instrument
	satellite1 - satellite
	instrument2 - instrument
	instrument3 - instrument
	instrument4 - instrument
	infrared4 - mode
	thermograph0 - mode
	infrared2 - mode
	image3 - mode
	image1 - mode
	Star2 - direction
	GroundStation0 - direction
	GroundStation1 - direction
	Planet3 - direction
	Star4 - direction
	Phenomenon5 - direction
)
(:init
	(supports instrument0 image3)
	(supports instrument0 thermograph0)
	(supports instrument0 infrared4)
	(calibration_target instrument0 GroundStation1)
	(supports instrument1 infrared4)
	(supports instrument1 infrared2)
	(supports instrument1 image1)
	(calibration_target instrument1 GroundStation1)
	(on_board instrument0 satellite0)
	(on_board instrument1 satellite0)
	(power_avail satellite0)
	(pointing satellite0 GroundStation0)
	(supports instrument2 infrared4)
	(supports instrument2 image3)
	(supports instrument2 infrared2)
	(calibration_target instrument2 Star2)
	(supports instrument3 thermograph0)
	(calibration_target instrument3 GroundStation0)
	(supports instrument4 infrared4)
	(supports instrument4 image1)
	(calibration_target instrument4 GroundStation1)
	(on_board instrument2 satellite1)
	(on_board instrument3 satellite1)
	(on_board instrument4 satellite1)
	(power_avail satellite1)
	(pointing satellite1 GroundStation1)
)
(:goal (and
	(pointing satellite0 GroundStation0)
	(have_image Planet3 image1)
	(have_image Star4 infrared4)
	(have_image Phenomenon5 image1)
))

)

(define (problem strips-sat-x-1)
(:domain satellite)
(:objects
	satellite0 - satellite
	instrument0 - instrument
	instrument1 - instrument
	instrument2 - instrument
	satellite1 - satellite
	instrument3 - instrument
	instrument4 - instrument
	image2 - mode
	thermograph1 - mode
	infrared0 - mode
	GroundStation2 - direction
	Star4 - direction
	Star3 - direction
	Star1 - direction
	Star0 - direction
	Star5 - direction
)
(:init
	(supports instrument0 image2)
	(calibration_target instrument0 Star0)
	(supports instrument1 thermograph1)
	(calibration_target instrument1 Star3)
	(supports instrument2 thermograph1)
	(calibration_target instrument2 Star3)
	(on_board instrument0 satellite0)
	(on_board instrument1 satellite0)
	(on_board instrument2 satellite0)
	(power_avail satellite0)
	(pointing satellite0 Star0)
	(supports instrument3 infrared0)
	(supports instrument3 image2)
	(calibration_target instrument3 Star1)
	(supports instrument4 thermograph1)
	(supports instrument4 infrared0)
	(supports instrument4 image2)
	(calibration_target instrument4 Star0)
	(on_board instrument3 satellite1)
	(on_board instrument4 satellite1)
	(power_avail satellite1)
	(pointing satellite1 Star3)
)
(:goal (and
	(pointing satellite0 GroundStation2)
	(pointing satellite1 Star5)
	(have_image Star5 thermograph1)
))

)

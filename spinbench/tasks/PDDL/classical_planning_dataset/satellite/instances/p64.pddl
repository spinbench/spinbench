(define (problem strips-sat-x-1)
(:domain satellite)
(:objects
	satellite0 - satellite
	instrument0 - instrument
	instrument1 - instrument
	satellite1 - satellite
	instrument2 - instrument
	thermograph2 - mode
	image0 - mode
	thermograph1 - mode
	Star2 - direction
	GroundStation6 - direction
	Star8 - direction
	Star3 - direction
	GroundStation1 - direction
	GroundStation0 - direction
	Star4 - direction
	GroundStation5 - direction
	GroundStation7 - direction
	Star9 - direction
	Star10 - direction
	Phenomenon11 - direction
	Star12 - direction
	Planet13 - direction
	Star14 - direction
)
(:init
	(supports instrument0 image0)
	(calibration_target instrument0 GroundStation1)
	(calibration_target instrument0 GroundStation7)
	(calibration_target instrument0 Star3)
	(supports instrument1 thermograph1)
	(supports instrument1 thermograph2)
	(calibration_target instrument1 Star4)
	(calibration_target instrument1 GroundStation0)
	(calibration_target instrument1 GroundStation5)
	(on_board instrument0 satellite0)
	(on_board instrument1 satellite0)
	(power_avail satellite0)
	(pointing satellite0 Star10)
	(supports instrument2 image0)
	(calibration_target instrument2 GroundStation7)
	(calibration_target instrument2 GroundStation5)
	(on_board instrument2 satellite1)
	(power_avail satellite1)
	(pointing satellite1 Phenomenon11)
)
(:goal (and
	(pointing satellite0 Star4)
	(have_image Star9 thermograph2)
	(have_image Star10 image0)
	(have_image Phenomenon11 image0)
	(have_image Star12 thermograph2)
	(have_image Planet13 image0)
	(have_image Star14 thermograph1)
))

)

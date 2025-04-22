(define (problem strips-sat-x-1)
(:domain satellite)
(:objects
	satellite0 - satellite
	instrument0 - instrument
	satellite1 - satellite
	instrument1 - instrument
	satellite2 - satellite
	instrument2 - instrument
	satellite3 - satellite
	instrument3 - instrument
	instrument4 - instrument
	instrument5 - instrument
	thermograph0 - mode
	image3 - mode
	thermograph2 - mode
	image1 - mode
	GroundStation0 - direction
	GroundStation3 - direction
	GroundStation2 - direction
	GroundStation1 - direction
	Planet4 - direction
	Phenomenon5 - direction
	Phenomenon6 - direction
	Phenomenon7 - direction
)
(:init
	(supports instrument0 image1)
	(calibration_target instrument0 GroundStation0)
	(on_board instrument0 satellite0)
	(power_avail satellite0)
	(pointing satellite0 Planet4)
	(supports instrument1 thermograph0)
	(supports instrument1 thermograph2)
	(supports instrument1 image1)
	(calibration_target instrument1 GroundStation3)
	(on_board instrument1 satellite1)
	(power_avail satellite1)
	(pointing satellite1 Phenomenon6)
	(supports instrument2 image1)
	(supports instrument2 thermograph0)
	(supports instrument2 thermograph2)
	(calibration_target instrument2 GroundStation3)
	(on_board instrument2 satellite2)
	(power_avail satellite2)
	(pointing satellite2 GroundStation3)
	(supports instrument3 thermograph0)
	(calibration_target instrument3 GroundStation2)
	(supports instrument4 image3)
	(calibration_target instrument4 GroundStation2)
	(supports instrument5 image3)
	(calibration_target instrument5 GroundStation1)
	(on_board instrument3 satellite3)
	(on_board instrument4 satellite3)
	(on_board instrument5 satellite3)
	(power_avail satellite3)
	(pointing satellite3 GroundStation3)
)
(:goal (and
	(pointing satellite2 GroundStation3)
	(have_image Planet4 thermograph2)
	(have_image Phenomenon5 thermograph0)
	(have_image Phenomenon6 image3)
	(have_image Phenomenon7 image1)
))

)

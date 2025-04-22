(define (problem strips-sat-x-1)
(:domain satellite)
(:objects
	satellite0 - satellite
	instrument0 - instrument
	satellite1 - satellite
	instrument1 - instrument
	spectrograph3 - mode
	thermograph0 - mode
	image1 - mode
	thermograph2 - mode
	infrared4 - mode
	Star1 - direction
	Star0 - direction
	GroundStation2 - direction
	Phenomenon3 - direction
	Star4 - direction
	Star5 - direction
	Phenomenon6 - direction
)
(:init
	(supports instrument0 infrared4)
	(supports instrument0 thermograph2)
	(supports instrument0 image1)
	(supports instrument0 spectrograph3)
	(calibration_target instrument0 Star0)
	(on_board instrument0 satellite0)
	(power_avail satellite0)
	(pointing satellite0 GroundStation2)
	(supports instrument1 thermograph0)
	(supports instrument1 thermograph2)
	(calibration_target instrument1 GroundStation2)
	(on_board instrument1 satellite1)
	(power_avail satellite1)
	(pointing satellite1 Star1)
)
(:goal (and
	(have_image Phenomenon3 thermograph0)
	(have_image Star4 infrared4)
	(have_image Star5 infrared4)
	(have_image Phenomenon6 thermograph2)
))

)

(define (problem strips-sat-x-1)
(:domain satellite)
(:objects
	satellite0 - satellite
	instrument0 - instrument
	instrument1 - instrument
	image3 - mode
	thermograph1 - mode
	spectrograph0 - mode
	thermograph2 - mode
	image4 - mode
	Star1 - direction
	Star0 - direction
	Star2 - direction
	Phenomenon3 - direction
	Phenomenon4 - direction
	Phenomenon5 - direction
	Star6 - direction
	Phenomenon7 - direction
)
(:init
	(supports instrument0 image4)
	(calibration_target instrument0 Star1)
	(supports instrument1 image3)
	(supports instrument1 image4)
	(supports instrument1 thermograph1)
	(supports instrument1 thermograph2)
	(supports instrument1 spectrograph0)
	(calibration_target instrument1 Star0)
	(on_board instrument0 satellite0)
	(on_board instrument1 satellite0)
	(power_avail satellite0)
	(pointing satellite0 Star2)
)
(:goal (and
	(have_image Star2 thermograph1)
	(have_image Phenomenon3 spectrograph0)
	(have_image Phenomenon4 spectrograph0)
	(have_image Phenomenon5 thermograph2)
	(have_image Star6 thermograph2)
	(have_image Phenomenon7 image4)
))

)

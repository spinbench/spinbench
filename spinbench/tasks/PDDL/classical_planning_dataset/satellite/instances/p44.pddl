(define (problem strips-sat-x-1)
(:domain satellite)
(:objects
	satellite0 - satellite
	instrument0 - instrument
	thermograph2 - mode
	infrared3 - mode
	spectrograph0 - mode
	spectrograph1 - mode
	Star0 - direction
	GroundStation1 - direction
	Star2 - direction
	Star3 - direction
	Star5 - direction
	GroundStation6 - direction
	Star7 - direction
	GroundStation8 - direction
	GroundStation4 - direction
	Phenomenon9 - direction
	Star10 - direction
	Star11 - direction
	Planet12 - direction
	Phenomenon13 - direction
	Planet14 - direction
	Phenomenon15 - direction
)
(:init
	(supports instrument0 thermograph2)
	(supports instrument0 spectrograph1)
	(supports instrument0 spectrograph0)
	(supports instrument0 infrared3)
	(calibration_target instrument0 GroundStation4)
	(on_board instrument0 satellite0)
	(power_avail satellite0)
	(pointing satellite0 GroundStation4)
)
(:goal (and
	(have_image Phenomenon9 infrared3)
	(have_image Star10 thermograph2)
	(have_image Star11 infrared3)
	(have_image Planet12 thermograph2)
	(have_image Phenomenon13 infrared3)
	(have_image Planet14 spectrograph0)
	(have_image Phenomenon15 spectrograph0)
))

)

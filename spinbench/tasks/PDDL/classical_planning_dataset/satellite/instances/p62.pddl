(define (problem strips-sat-x-1)
(:domain satellite)
(:objects
	satellite0 - satellite
	instrument0 - instrument
	instrument1 - instrument
	spectrograph0 - mode
	spectrograph1 - mode
	thermograph3 - mode
	spectrograph2 - mode
	Star0 - direction
	GroundStation1 - direction
	GroundStation4 - direction
	GroundStation5 - direction
	Star7 - direction
	Star6 - direction
	Star3 - direction
	GroundStation2 - direction
	Star8 - direction
	Planet9 - direction
	Phenomenon10 - direction
	Phenomenon11 - direction
	Star12 - direction
	Star13 - direction
	Phenomenon14 - direction
	Phenomenon15 - direction
)
(:init
	(supports instrument0 spectrograph1)
	(supports instrument0 spectrograph2)
	(calibration_target instrument0 Star3)
	(calibration_target instrument0 Star6)
	(supports instrument1 thermograph3)
	(supports instrument1 spectrograph0)
	(calibration_target instrument1 Star8)
	(calibration_target instrument1 GroundStation2)
	(calibration_target instrument1 Star3)
	(on_board instrument0 satellite0)
	(on_board instrument1 satellite0)
	(power_avail satellite0)
	(pointing satellite0 Star6)
)
(:goal (and
	(have_image Planet9 spectrograph2)
	(have_image Phenomenon10 thermograph3)
	(have_image Phenomenon11 thermograph3)
	(have_image Star12 spectrograph2)
	(have_image Star13 spectrograph0)
	(have_image Phenomenon14 spectrograph1)
	(have_image Phenomenon15 spectrograph0)
))

)

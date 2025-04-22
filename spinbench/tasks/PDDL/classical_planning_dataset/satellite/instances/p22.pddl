(define (problem strips-sat-x-1)
(:domain satellite)
(:objects
	satellite0 - satellite
	instrument0 - instrument
	satellite1 - satellite
	instrument1 - instrument
	satellite2 - satellite
	instrument2 - instrument
	spectrograph1 - mode
	spectrograph2 - mode
	thermograph0 - mode
	GroundStation2 - direction
	Star1 - direction
	Star0 - direction
	Star3 - direction
	Phenomenon4 - direction
	Star5 - direction
	Planet6 - direction
	Star7 - direction
)
(:init
	(supports instrument0 spectrograph1)
	(supports instrument0 spectrograph2)
	(supports instrument0 thermograph0)
	(calibration_target instrument0 GroundStation2)
	(on_board instrument0 satellite0)
	(power_avail satellite0)
	(pointing satellite0 Planet6)
	(supports instrument1 spectrograph2)
	(supports instrument1 spectrograph1)
	(calibration_target instrument1 Star1)
	(on_board instrument1 satellite1)
	(power_avail satellite1)
	(pointing satellite1 Star1)
	(supports instrument2 thermograph0)
	(supports instrument2 spectrograph1)
	(supports instrument2 spectrograph2)
	(calibration_target instrument2 Star0)
	(on_board instrument2 satellite2)
	(power_avail satellite2)
	(pointing satellite2 Star0)
)
(:goal (and
	(pointing satellite2 Phenomenon4)
	(have_image Star3 thermograph0)
	(have_image Phenomenon4 thermograph0)
	(have_image Star5 spectrograph1)
	(have_image Planet6 spectrograph2)
	(have_image Star7 spectrograph1)
))

)

(define (problem strips-sat-x-1)
(:domain satellite)
(:objects
	satellite0 - satellite
	instrument0 - instrument
	instrument1 - instrument
	satellite1 - satellite
	instrument2 - instrument
	satellite2 - satellite
	instrument3 - instrument
	image0 - mode
	thermograph3 - mode
	spectrograph1 - mode
	spectrograph2 - mode
	GroundStation0 - direction
	Star2 - direction
	GroundStation1 - direction
	Phenomenon3 - direction
	Planet4 - direction
	Phenomenon5 - direction
	Phenomenon6 - direction
	Planet7 - direction
	Planet8 - direction
	Phenomenon9 - direction
	Planet10 - direction
	Star11 - direction
	Planet12 - direction
)
(:init
	(supports instrument0 spectrograph2)
	(calibration_target instrument0 GroundStation1)
	(supports instrument1 spectrograph2)
	(supports instrument1 spectrograph1)
	(supports instrument1 image0)
	(calibration_target instrument1 GroundStation1)
	(on_board instrument0 satellite0)
	(on_board instrument1 satellite0)
	(power_avail satellite0)
	(pointing satellite0 GroundStation0)
	(supports instrument2 thermograph3)
	(supports instrument2 image0)
	(calibration_target instrument2 GroundStation1)
	(on_board instrument2 satellite1)
	(power_avail satellite1)
	(pointing satellite1 Planet12)
	(supports instrument3 thermograph3)
	(supports instrument3 spectrograph2)
	(calibration_target instrument3 GroundStation1)
	(on_board instrument3 satellite2)
	(power_avail satellite2)
	(pointing satellite2 Phenomenon5)
)
(:goal (and
	(pointing satellite0 Phenomenon3)
	(pointing satellite1 Phenomenon5)
	(have_image Phenomenon3 image0)
	(have_image Planet4 thermograph3)
	(have_image Phenomenon5 spectrograph2)
	(have_image Phenomenon6 spectrograph2)
	(have_image Planet7 spectrograph1)
	(have_image Planet8 thermograph3)
	(have_image Phenomenon9 spectrograph2)
	(have_image Planet10 thermograph3)
	(have_image Star11 thermograph3)
	(have_image Planet12 spectrograph1)
))

)

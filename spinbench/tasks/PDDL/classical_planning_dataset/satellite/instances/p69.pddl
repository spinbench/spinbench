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
	instrument4 - instrument
	thermograph1 - mode
	spectrograph0 - mode
	spectrograph3 - mode
	thermograph2 - mode
	thermograph4 - mode
	Star2 - direction
	Star4 - direction
	GroundStation0 - direction
	Star3 - direction
	Star7 - direction
	Star5 - direction
	GroundStation8 - direction
	GroundStation6 - direction
	Star1 - direction
	Phenomenon9 - direction
	Star10 - direction
	Phenomenon11 - direction
	Phenomenon12 - direction
	Planet13 - direction
	Planet14 - direction
	Planet15 - direction
	Planet16 - direction
	Phenomenon17 - direction
)
(:init
	(supports instrument0 spectrograph0)
	(supports instrument0 thermograph1)
	(calibration_target instrument0 Star3)
	(calibration_target instrument0 GroundStation0)
	(supports instrument1 thermograph2)
	(supports instrument1 thermograph4)
	(supports instrument1 thermograph1)
	(calibration_target instrument1 GroundStation8)
	(calibration_target instrument1 Star7)
	(on_board instrument0 satellite0)
	(on_board instrument1 satellite0)
	(power_avail satellite0)
	(pointing satellite0 Phenomenon11)
	(supports instrument2 spectrograph0)
	(supports instrument2 thermograph4)
	(supports instrument2 spectrograph3)
	(calibration_target instrument2 Star7)
	(on_board instrument2 satellite1)
	(power_avail satellite1)
	(pointing satellite1 Phenomenon11)
	(supports instrument3 thermograph4)
	(supports instrument3 spectrograph3)
	(calibration_target instrument3 Star1)
	(calibration_target instrument3 Star5)
	(supports instrument4 spectrograph0)
	(supports instrument4 spectrograph3)
	(calibration_target instrument4 Star1)
	(calibration_target instrument4 GroundStation6)
	(calibration_target instrument4 GroundStation8)
	(on_board instrument3 satellite2)
	(on_board instrument4 satellite2)
	(power_avail satellite2)
	(pointing satellite2 Planet15)
)
(:goal (and
	(pointing satellite2 Phenomenon9)
	(have_image Phenomenon9 thermograph4)
	(have_image Star10 thermograph4)
	(have_image Phenomenon11 spectrograph3)
	(have_image Phenomenon12 thermograph2)
	(have_image Planet13 thermograph2)
	(have_image Planet14 thermograph2)
	(have_image Planet15 thermograph2)
	(have_image Planet16 spectrograph3)
	(have_image Phenomenon17 spectrograph0)
))

)

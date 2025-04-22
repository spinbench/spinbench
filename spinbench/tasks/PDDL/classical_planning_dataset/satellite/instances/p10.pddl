(define (problem strips-sat-x-1)
(:domain satellite)
(:objects
	satellite0 - satellite
	instrument0 - instrument
	instrument1 - instrument
	spectrograph0 - mode
	spectrograph2 - mode
	spectrograph1 - mode
	Star0 - direction
	GroundStation1 - direction
	GroundStation4 - direction
	Star5 - direction
	Star2 - direction
	GroundStation3 - direction
	GroundStation7 - direction
	GroundStation6 - direction
	Star8 - direction
	Star9 - direction
	Star10 - direction
	Planet11 - direction
	Phenomenon12 - direction
)
(:init
	(supports instrument0 spectrograph2)
	(supports instrument0 spectrograph0)
	(supports instrument0 spectrograph1)
	(calibration_target instrument0 GroundStation3)
	(calibration_target instrument0 Star2)
	(supports instrument1 spectrograph0)
	(supports instrument1 spectrograph2)
	(supports instrument1 spectrograph1)
	(calibration_target instrument1 GroundStation6)
	(calibration_target instrument1 GroundStation7)
	(on_board instrument0 satellite0)
	(on_board instrument1 satellite0)
	(power_avail satellite0)
	(pointing satellite0 Planet11)
)
(:goal (and
	(have_image Star8 spectrograph0)
	(have_image Star9 spectrograph1)
	(have_image Star10 spectrograph1)
	(have_image Planet11 spectrograph1)
	(have_image Phenomenon12 spectrograph1)
))

)

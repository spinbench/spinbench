(define (problem strips-sat-x-1)
(:domain satellite)
(:objects
	satellite0 - satellite
	instrument0 - instrument
	instrument1 - instrument
	satellite1 - satellite
	instrument2 - instrument
	spectrograph0 - mode
	spectrograph1 - mode
	infrared2 - mode
	GroundStation0 - direction
	GroundStation1 - direction
	Star2 - direction
	Phenomenon3 - direction
	Planet4 - direction
)
(:init
	(supports instrument0 spectrograph1)
	(supports instrument0 spectrograph0)
	(calibration_target instrument0 GroundStation1)
	(supports instrument1 spectrograph1)
	(supports instrument1 infrared2)
	(supports instrument1 spectrograph0)
	(calibration_target instrument1 GroundStation0)
	(on_board instrument0 satellite0)
	(on_board instrument1 satellite0)
	(power_avail satellite0)
	(pointing satellite0 Planet4)
	(supports instrument2 infrared2)
	(calibration_target instrument2 GroundStation1)
	(on_board instrument2 satellite1)
	(power_avail satellite1)
	(pointing satellite1 Planet4)
)
(:goal (and
	(pointing satellite0 Planet4)
	(pointing satellite1 Star2)
	(have_image Star2 spectrograph0)
	(have_image Phenomenon3 infrared2)
	(have_image Planet4 infrared2)
))

)

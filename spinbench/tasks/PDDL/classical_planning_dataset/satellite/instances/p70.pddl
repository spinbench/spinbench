(define (problem strips-sat-x-1)
(:domain satellite)
(:objects
	satellite0 - satellite
	instrument0 - instrument
	instrument1 - instrument
	instrument2 - instrument
	infrared2 - mode
	thermograph1 - mode
	spectrograph0 - mode
	GroundStation2 - direction
	Star1 - direction
	Star3 - direction
	GroundStation0 - direction
	Star4 - direction
)
(:init
	(supports instrument0 infrared2)
	(supports instrument0 thermograph1)
	(calibration_target instrument0 Star1)
	(supports instrument1 spectrograph0)
	(calibration_target instrument1 Star3)
	(supports instrument2 infrared2)
	(calibration_target instrument2 GroundStation0)
	(on_board instrument0 satellite0)
	(on_board instrument1 satellite0)
	(on_board instrument2 satellite0)
	(power_avail satellite0)
	(pointing satellite0 Star1)
)
(:goal (and
	(have_image Star4 infrared2)
))

)

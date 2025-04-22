(define (problem strips-sat-x-1)
(:domain satellite)
(:objects
	satellite0 - satellite
	instrument0 - instrument
	instrument1 - instrument
	image2 - mode
	infrared1 - mode
	infrared0 - mode
	Star1 - direction
	GroundStation2 - direction
	GroundStation4 - direction
	GroundStation3 - direction
	GroundStation0 - direction
	GroundStation5 - direction
	Planet6 - direction
	Star7 - direction
)
(:init
	(supports instrument0 infrared0)
	(calibration_target instrument0 GroundStation3)
	(supports instrument1 image2)
	(supports instrument1 infrared1)
	(supports instrument1 infrared0)
	(calibration_target instrument1 GroundStation5)
	(calibration_target instrument1 GroundStation0)
	(on_board instrument0 satellite0)
	(on_board instrument1 satellite0)
	(power_avail satellite0)
	(pointing satellite0 GroundStation3)
)
(:goal (and
	(pointing satellite0 GroundStation0)
	(have_image Planet6 image2)
	(have_image Star7 image2)
))

)

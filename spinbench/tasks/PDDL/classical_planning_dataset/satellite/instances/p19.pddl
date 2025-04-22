(define (problem strips-sat-x-1)
(:domain satellite)
(:objects
	satellite0 - satellite
	instrument0 - instrument
	instrument1 - instrument
	image0 - mode
	infrared3 - mode
	infrared2 - mode
	infrared4 - mode
	image1 - mode
	Star1 - direction
	GroundStation0 - direction
	Planet2 - direction
	Phenomenon3 - direction
	Phenomenon4 - direction
	Star5 - direction
	Planet6 - direction
)
(:init
	(supports instrument0 infrared3)
	(supports instrument0 infrared4)
	(supports instrument0 image0)
	(calibration_target instrument0 GroundStation0)
	(supports instrument1 infrared2)
	(supports instrument1 infrared3)
	(supports instrument1 image1)
	(calibration_target instrument1 GroundStation0)
	(on_board instrument0 satellite0)
	(on_board instrument1 satellite0)
	(power_avail satellite0)
	(pointing satellite0 Phenomenon3)
)
(:goal (and
	(pointing satellite0 Planet2)
	(have_image Planet2 infrared3)
	(have_image Phenomenon3 infrared3)
	(have_image Phenomenon4 image0)
	(have_image Star5 infrared3)
	(have_image Planet6 image0)
))

)

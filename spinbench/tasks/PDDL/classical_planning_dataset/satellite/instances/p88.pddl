(define (problem strips-sat-x-1)
(:domain satellite)
(:objects
	satellite0 - satellite
	instrument0 - instrument
	instrument1 - instrument
	infrared2 - mode
	infrared0 - mode
	infrared3 - mode
	spectrograph4 - mode
	image1 - mode
	GroundStation2 - direction
	GroundStation3 - direction
	Star4 - direction
	GroundStation5 - direction
	Star0 - direction
	GroundStation1 - direction
	Phenomenon6 - direction
	Star7 - direction
	Phenomenon8 - direction
	Planet9 - direction
)
(:init
	(supports instrument0 infrared2)
	(supports instrument0 spectrograph4)
	(calibration_target instrument0 GroundStation5)
	(supports instrument1 image1)
	(supports instrument1 infrared3)
	(supports instrument1 infrared0)
	(calibration_target instrument1 GroundStation1)
	(calibration_target instrument1 Star0)
	(on_board instrument0 satellite0)
	(on_board instrument1 satellite0)
	(power_avail satellite0)
	(pointing satellite0 Star7)
)
(:goal (and
	(have_image Phenomenon6 image1)
	(have_image Star7 infrared0)
	(have_image Phenomenon8 infrared0)
	(have_image Planet9 image1)
))

)

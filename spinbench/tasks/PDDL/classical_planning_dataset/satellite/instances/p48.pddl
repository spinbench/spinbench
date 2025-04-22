(define (problem strips-sat-x-1)
(:domain satellite)
(:objects
	satellite0 - satellite
	instrument0 - instrument
	satellite1 - satellite
	instrument1 - instrument
	image3 - mode
	spectrograph0 - mode
	image1 - mode
	infrared2 - mode
	Star1 - direction
	Star4 - direction
	GroundStation5 - direction
	Star6 - direction
	GroundStation3 - direction
	GroundStation0 - direction
	Star2 - direction
	Planet7 - direction
	Phenomenon8 - direction
	Star9 - direction
	Planet10 - direction
	Star11 - direction
)
(:init
	(supports instrument0 image1)
	(supports instrument0 infrared2)
	(supports instrument0 spectrograph0)
	(supports instrument0 image3)
	(calibration_target instrument0 GroundStation3)
	(on_board instrument0 satellite0)
	(power_avail satellite0)
	(pointing satellite0 Star4)
	(supports instrument1 image1)
	(calibration_target instrument1 Star2)
	(calibration_target instrument1 GroundStation0)
	(on_board instrument1 satellite1)
	(power_avail satellite1)
	(pointing satellite1 Star9)
)
(:goal (and
	(pointing satellite1 Star11)
	(have_image Planet7 image1)
	(have_image Phenomenon8 image3)
	(have_image Star9 spectrograph0)
	(have_image Planet10 image1)
	(have_image Star11 infrared2)
))

)

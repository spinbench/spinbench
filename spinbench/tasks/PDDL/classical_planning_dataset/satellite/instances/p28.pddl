(define (problem strips-sat-x-1)
(:domain satellite)
(:objects
	satellite0 - satellite
	instrument0 - instrument
	instrument1 - instrument
	spectrograph0 - mode
	image2 - mode
	image3 - mode
	infrared1 - mode
	GroundStation1 - direction
	Star3 - direction
	Star5 - direction
	GroundStation6 - direction
	GroundStation4 - direction
	Star0 - direction
	GroundStation2 - direction
	Planet7 - direction
	Planet8 - direction
	Star9 - direction
	Star10 - direction
	Star11 - direction
	Phenomenon12 - direction
	Planet13 - direction
	Phenomenon14 - direction
	Planet15 - direction
)
(:init
	(supports instrument0 image3)
	(supports instrument0 spectrograph0)
	(calibration_target instrument0 Star0)
	(calibration_target instrument0 GroundStation4)
	(supports instrument1 image2)
	(supports instrument1 image3)
	(supports instrument1 infrared1)
	(calibration_target instrument1 GroundStation2)
	(calibration_target instrument1 Star0)
	(on_board instrument0 satellite0)
	(on_board instrument1 satellite0)
	(power_avail satellite0)
	(pointing satellite0 GroundStation6)
)
(:goal (and
	(pointing satellite0 GroundStation4)
	(have_image Planet7 spectrograph0)
	(have_image Planet8 image2)
	(have_image Star9 spectrograph0)
	(have_image Star10 image2)
	(have_image Star11 image3)
	(have_image Phenomenon12 image2)
	(have_image Planet13 image2)
	(have_image Phenomenon14 image3)
	(have_image Planet15 image2)
))

)

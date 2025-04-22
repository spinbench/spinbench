(define (problem strips-sat-x-1)
(:domain satellite)
(:objects
	satellite0 - satellite
	instrument0 - instrument
	instrument1 - instrument
	satellite1 - satellite
	instrument2 - instrument
	instrument3 - instrument
	image0 - mode
	infrared4 - mode
	image2 - mode
	spectrograph3 - mode
	infrared1 - mode
	Star2 - direction
	GroundStation0 - direction
	Star1 - direction
	Phenomenon3 - direction
	Phenomenon4 - direction
	Star5 - direction
	Planet6 - direction
	Planet7 - direction
	Phenomenon8 - direction
)
(:init
	(supports instrument0 image2)
	(supports instrument0 image0)
	(calibration_target instrument0 Star1)
	(supports instrument1 spectrograph3)
	(calibration_target instrument1 Star2)
	(on_board instrument0 satellite0)
	(on_board instrument1 satellite0)
	(power_avail satellite0)
	(pointing satellite0 GroundStation0)
	(supports instrument2 image0)
	(supports instrument2 infrared1)
	(supports instrument2 spectrograph3)
	(calibration_target instrument2 GroundStation0)
	(supports instrument3 image0)
	(supports instrument3 infrared4)
	(calibration_target instrument3 Star1)
	(on_board instrument2 satellite1)
	(on_board instrument3 satellite1)
	(power_avail satellite1)
	(pointing satellite1 Star1)
)
(:goal (and
	(have_image Phenomenon3 image2)
	(have_image Phenomenon4 image0)
	(have_image Star5 infrared4)
	(have_image Planet6 image0)
	(have_image Planet7 spectrograph3)
	(have_image Phenomenon8 infrared1)
))

)

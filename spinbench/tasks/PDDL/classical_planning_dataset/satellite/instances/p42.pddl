(define (problem strips-sat-x-1)
(:domain satellite)
(:objects
	satellite0 - satellite
	instrument0 - instrument
	instrument1 - instrument
	satellite1 - satellite
	instrument2 - instrument
	image3 - mode
	image1 - mode
	infrared4 - mode
	infrared0 - mode
	spectrograph2 - mode
	Star0 - direction
	Star1 - direction
	Star2 - direction
	Phenomenon3 - direction
)
(:init
	(supports instrument0 image1)
	(supports instrument0 infrared0)
	(calibration_target instrument0 Star0)
	(supports instrument1 image1)
	(supports instrument1 image3)
	(calibration_target instrument1 Star0)
	(on_board instrument0 satellite0)
	(on_board instrument1 satellite0)
	(power_avail satellite0)
	(pointing satellite0 Star0)
	(supports instrument2 infrared4)
	(supports instrument2 image1)
	(supports instrument2 spectrograph2)
	(calibration_target instrument2 Star1)
	(on_board instrument2 satellite1)
	(power_avail satellite1)
	(pointing satellite1 Star2)
)
(:goal (and
	(pointing satellite1 Star1)
	(have_image Star2 image3)
	(have_image Phenomenon3 spectrograph2)
))

)

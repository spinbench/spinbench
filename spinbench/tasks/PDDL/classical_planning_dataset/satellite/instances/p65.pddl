(define (problem strips-sat-x-1)
(:domain satellite)
(:objects
	satellite0 - satellite
	instrument0 - instrument
	instrument1 - instrument
	image1 - mode
	image0 - mode
	spectrograph2 - mode
	Star1 - direction
	Star4 - direction
	GroundStation5 - direction
	Star6 - direction
	GroundStation7 - direction
	Star8 - direction
	Star3 - direction
	GroundStation2 - direction
	GroundStation0 - direction
	Phenomenon9 - direction
	Star10 - direction
	Phenomenon11 - direction
)
(:init
	(supports instrument0 spectrograph2)
	(supports instrument0 image1)
	(supports instrument0 image0)
	(calibration_target instrument0 Star3)
	(calibration_target instrument0 GroundStation0)
	(supports instrument1 image0)
	(supports instrument1 spectrograph2)
	(calibration_target instrument1 GroundStation0)
	(calibration_target instrument1 GroundStation2)
	(on_board instrument0 satellite0)
	(on_board instrument1 satellite0)
	(power_avail satellite0)
	(pointing satellite0 Star10)
)
(:goal (and
	(have_image Phenomenon9 spectrograph2)
	(have_image Star10 spectrograph2)
	(have_image Phenomenon11 spectrograph2)
))

)

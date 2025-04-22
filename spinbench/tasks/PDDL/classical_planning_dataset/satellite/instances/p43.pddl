(define (problem strips-sat-x-1)
(:domain satellite)
(:objects
	satellite0 - satellite
	instrument0 - instrument
	instrument1 - instrument
	spectrograph3 - mode
	infrared1 - mode
	image2 - mode
	image0 - mode
	GroundStation2 - direction
	GroundStation3 - direction
	GroundStation4 - direction
	Star7 - direction
	GroundStation8 - direction
	Star0 - direction
	Star6 - direction
	Star1 - direction
	GroundStation5 - direction
	Phenomenon9 - direction
)
(:init
	(supports instrument0 spectrograph3)
	(supports instrument0 image2)
	(supports instrument0 infrared1)
	(calibration_target instrument0 Star6)
	(calibration_target instrument0 Star0)
	(calibration_target instrument0 GroundStation8)
	(supports instrument1 image0)
	(supports instrument1 spectrograph3)
	(supports instrument1 image2)
	(calibration_target instrument1 GroundStation5)
	(calibration_target instrument1 Star1)
	(on_board instrument0 satellite0)
	(on_board instrument1 satellite0)
	(power_avail satellite0)
	(pointing satellite0 Star6)
)
(:goal (and
	(have_image Phenomenon9 image2)
))

)

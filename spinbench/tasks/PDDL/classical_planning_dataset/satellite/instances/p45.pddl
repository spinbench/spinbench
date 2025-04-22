(define (problem strips-sat-x-1)
(:domain satellite)
(:objects
	satellite0 - satellite
	instrument0 - instrument
	instrument1 - instrument
	instrument2 - instrument
	infrared1 - mode
	spectrograph2 - mode
	spectrograph0 - mode
	thermograph3 - mode
	GroundStation4 - direction
	Star7 - direction
	Star8 - direction
	GroundStation3 - direction
	Star0 - direction
	Star6 - direction
	GroundStation2 - direction
	Star5 - direction
	GroundStation1 - direction
	Planet9 - direction
	Phenomenon10 - direction
)
(:init
	(supports instrument0 infrared1)
	(calibration_target instrument0 Star6)
	(calibration_target instrument0 Star0)
	(calibration_target instrument0 GroundStation3)
	(supports instrument1 infrared1)
	(calibration_target instrument1 GroundStation2)
	(calibration_target instrument1 Star5)
	(supports instrument2 spectrograph2)
	(supports instrument2 thermograph3)
	(supports instrument2 spectrograph0)
	(calibration_target instrument2 GroundStation1)
	(calibration_target instrument2 Star5)
	(on_board instrument0 satellite0)
	(on_board instrument1 satellite0)
	(on_board instrument2 satellite0)
	(power_avail satellite0)
	(pointing satellite0 Star7)
)
(:goal (and
	(pointing satellite0 Star5)
	(have_image Planet9 spectrograph0)
	(have_image Phenomenon10 spectrograph0)
))

)

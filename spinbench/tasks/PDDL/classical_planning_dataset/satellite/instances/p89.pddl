(define (problem strips-sat-x-1)
(:domain satellite)
(:objects
	satellite0 - satellite
	instrument0 - instrument
	instrument1 - instrument
	thermograph0 - mode
	spectrograph1 - mode
	image3 - mode
	infrared4 - mode
	thermograph2 - mode
	GroundStation0 - direction
	GroundStation2 - direction
	GroundStation3 - direction
	GroundStation5 - direction
	Star6 - direction
	Star7 - direction
	Star1 - direction
	Star8 - direction
	Star4 - direction
	Star9 - direction
)
(:init
	(supports instrument0 spectrograph1)
	(supports instrument0 thermograph2)
	(calibration_target instrument0 Star8)
	(calibration_target instrument0 Star1)
	(calibration_target instrument0 Star7)
	(supports instrument1 image3)
	(supports instrument1 infrared4)
	(supports instrument1 thermograph0)
	(calibration_target instrument1 Star4)
	(calibration_target instrument1 Star8)
	(on_board instrument0 satellite0)
	(on_board instrument1 satellite0)
	(power_avail satellite0)
	(pointing satellite0 Star8)
)
(:goal (and
	(have_image Star9 thermograph0)
))

)

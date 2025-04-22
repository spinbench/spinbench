(define (problem strips-sat-x-1)
(:domain satellite)
(:objects
	satellite0 - satellite
	instrument0 - instrument
	instrument1 - instrument
	satellite1 - satellite
	instrument2 - instrument
	infrared1 - mode
	thermograph0 - mode
	infrared3 - mode
	spectrograph2 - mode
	GroundStation0 - direction
	GroundStation1 - direction
	GroundStation5 - direction
	Star2 - direction
	GroundStation3 - direction
	GroundStation4 - direction
	Star6 - direction
	Star7 - direction
	Phenomenon8 - direction
	Star9 - direction
)
(:init
	(supports instrument0 infrared1)
	(supports instrument0 spectrograph2)
	(supports instrument0 thermograph0)
	(calibration_target instrument0 GroundStation4)
	(supports instrument1 infrared1)
	(calibration_target instrument1 GroundStation3)
	(calibration_target instrument1 Star2)
	(on_board instrument0 satellite0)
	(on_board instrument1 satellite0)
	(power_avail satellite0)
	(pointing satellite0 GroundStation5)
	(supports instrument2 spectrograph2)
	(supports instrument2 infrared3)
	(calibration_target instrument2 GroundStation4)
	(on_board instrument2 satellite1)
	(power_avail satellite1)
	(pointing satellite1 GroundStation3)
)
(:goal (and
	(pointing satellite1 Star7)
	(have_image Star6 infrared1)
	(have_image Star7 spectrograph2)
	(have_image Phenomenon8 thermograph0)
	(have_image Star9 thermograph0)
))

)

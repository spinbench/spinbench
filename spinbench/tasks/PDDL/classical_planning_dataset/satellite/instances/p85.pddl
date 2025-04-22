(define (problem strips-sat-x-1)
(:domain satellite)
(:objects
	satellite0 - satellite
	instrument0 - instrument
	satellite1 - satellite
	instrument1 - instrument
	instrument2 - instrument
	instrument3 - instrument
	satellite2 - satellite
	instrument4 - instrument
	thermograph0 - mode
	spectrograph1 - mode
	spectrograph2 - mode
	GroundStation0 - direction
	Star5 - direction
	GroundStation6 - direction
	Star1 - direction
	GroundStation2 - direction
	GroundStation4 - direction
	Star3 - direction
	Star7 - direction
	Phenomenon8 - direction
	Star9 - direction
)
(:init
	(supports instrument0 spectrograph1)
	(calibration_target instrument0 Star1)
	(on_board instrument0 satellite0)
	(power_avail satellite0)
	(pointing satellite0 Star3)
	(supports instrument1 spectrograph2)
	(calibration_target instrument1 GroundStation4)
	(calibration_target instrument1 Star1)
	(supports instrument2 spectrograph1)
	(calibration_target instrument2 GroundStation4)
	(calibration_target instrument2 GroundStation2)
	(supports instrument3 spectrograph1)
	(supports instrument3 thermograph0)
	(calibration_target instrument3 GroundStation4)
	(on_board instrument1 satellite1)
	(on_board instrument2 satellite1)
	(on_board instrument3 satellite1)
	(power_avail satellite1)
	(pointing satellite1 GroundStation4)
	(supports instrument4 spectrograph2)
	(calibration_target instrument4 Star3)
	(on_board instrument4 satellite2)
	(power_avail satellite2)
	(pointing satellite2 GroundStation0)
)
(:goal (and
	(pointing satellite1 GroundStation4)
	(have_image Star7 spectrograph1)
	(have_image Phenomenon8 spectrograph2)
	(have_image Star9 spectrograph1)
))

)

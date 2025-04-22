(define (problem strips-sat-x-1)
(:domain satellite)
(:objects
	satellite0 - satellite
	instrument0 - instrument
	satellite1 - satellite
	instrument1 - instrument
	instrument2 - instrument
	satellite2 - satellite
	instrument3 - instrument
	instrument4 - instrument
	spectrograph1 - mode
	infrared2 - mode
	thermograph0 - mode
	Star1 - direction
	GroundStation0 - direction
	Star5 - direction
	GroundStation2 - direction
	Star3 - direction
	GroundStation4 - direction
	Star6 - direction
	Planet7 - direction
)
(:init
	(supports instrument0 spectrograph1)
	(supports instrument0 infrared2)
	(calibration_target instrument0 GroundStation0)
	(on_board instrument0 satellite0)
	(power_avail satellite0)
	(pointing satellite0 Star6)
	(supports instrument1 infrared2)
	(supports instrument1 spectrograph1)
	(supports instrument1 thermograph0)
	(calibration_target instrument1 Star3)
	(supports instrument2 infrared2)
	(supports instrument2 thermograph0)
	(calibration_target instrument2 Star5)
	(calibration_target instrument2 GroundStation0)
	(on_board instrument1 satellite1)
	(on_board instrument2 satellite1)
	(power_avail satellite1)
	(pointing satellite1 GroundStation2)
	(supports instrument3 infrared2)
	(calibration_target instrument3 GroundStation2)
	(calibration_target instrument3 Star3)
	(supports instrument4 infrared2)
	(supports instrument4 thermograph0)
	(calibration_target instrument4 GroundStation4)
	(calibration_target instrument4 Star3)
	(on_board instrument3 satellite2)
	(on_board instrument4 satellite2)
	(power_avail satellite2)
	(pointing satellite2 Star3)
)
(:goal (and
	(pointing satellite0 Planet7)
	(pointing satellite2 GroundStation4)
	(have_image Star6 spectrograph1)
	(have_image Planet7 thermograph0)
))

)

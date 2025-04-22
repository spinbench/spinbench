(define (problem strips-sat-x-1)
(:domain satellite)
(:objects
	satellite0 - satellite
	instrument0 - instrument
	instrument1 - instrument
	instrument2 - instrument
	satellite1 - satellite
	instrument3 - instrument
	instrument4 - instrument
	satellite2 - satellite
	instrument5 - instrument
	instrument6 - instrument
	satellite3 - satellite
	instrument7 - instrument
	instrument8 - instrument
	spectrograph2 - mode
	thermograph4 - mode
	image3 - mode
	image0 - mode
	spectrograph1 - mode
	GroundStation3 - direction
	GroundStation2 - direction
	GroundStation4 - direction
	GroundStation0 - direction
	Star1 - direction
	Star5 - direction
	Star6 - direction
	Star7 - direction
	Planet8 - direction
)
(:init
	(supports instrument0 thermograph4)
	(supports instrument0 spectrograph2)
	(calibration_target instrument0 GroundStation4)
	(supports instrument1 spectrograph2)
	(supports instrument1 image3)
	(supports instrument1 image0)
	(calibration_target instrument1 GroundStation0)
	(supports instrument2 image0)
	(calibration_target instrument2 Star1)
	(on_board instrument0 satellite0)
	(on_board instrument1 satellite0)
	(on_board instrument2 satellite0)
	(power_avail satellite0)
	(pointing satellite0 GroundStation4)
	(supports instrument3 image0)
	(calibration_target instrument3 Star1)
	(supports instrument4 spectrograph1)
	(calibration_target instrument4 GroundStation2)
	(on_board instrument3 satellite1)
	(on_board instrument4 satellite1)
	(power_avail satellite1)
	(pointing satellite1 GroundStation0)
	(supports instrument5 spectrograph1)
	(calibration_target instrument5 Star1)
	(supports instrument6 image3)
	(supports instrument6 image0)
	(supports instrument6 spectrograph2)
	(calibration_target instrument6 GroundStation4)
	(on_board instrument5 satellite2)
	(on_board instrument6 satellite2)
	(power_avail satellite2)
	(pointing satellite2 Star6)
	(supports instrument7 image0)
	(calibration_target instrument7 GroundStation0)
	(supports instrument8 image0)
	(calibration_target instrument8 Star1)
	(on_board instrument7 satellite3)
	(on_board instrument8 satellite3)
	(power_avail satellite3)
	(pointing satellite3 Planet8)
)
(:goal (and
	(pointing satellite1 GroundStation0)
	(pointing satellite3 Star7)
	(have_image Star5 spectrograph1)
	(have_image Star6 spectrograph1)
	(have_image Star7 thermograph4)
	(have_image Planet8 spectrograph2)
))

)

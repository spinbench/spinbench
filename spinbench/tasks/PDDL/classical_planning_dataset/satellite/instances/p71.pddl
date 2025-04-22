(define (problem strips-sat-x-1)
(:domain satellite)
(:objects
	satellite0 - satellite
	instrument0 - instrument
	satellite1 - satellite
	instrument1 - instrument
	satellite2 - satellite
	instrument2 - instrument
	instrument3 - instrument
	satellite3 - satellite
	instrument4 - instrument
	satellite4 - satellite
	instrument5 - instrument
	instrument6 - instrument
	spectrograph3 - mode
	thermograph2 - mode
	image1 - mode
	image0 - mode
	GroundStation3 - direction
	Star2 - direction
	GroundStation6 - direction
	GroundStation7 - direction
	GroundStation5 - direction
	GroundStation1 - direction
	GroundStation0 - direction
	GroundStation4 - direction
	Star8 - direction
	Planet9 - direction
	Phenomenon10 - direction
	Planet11 - direction
	Star12 - direction
)
(:init
	(supports instrument0 thermograph2)
	(supports instrument0 image0)
	(supports instrument0 image1)
	(calibration_target instrument0 GroundStation7)
	(on_board instrument0 satellite0)
	(power_avail satellite0)
	(pointing satellite0 Star12)
	(supports instrument1 image1)
	(calibration_target instrument1 Star2)
	(on_board instrument1 satellite1)
	(power_avail satellite1)
	(pointing satellite1 GroundStation5)
	(supports instrument2 thermograph2)
	(calibration_target instrument2 GroundStation7)
	(calibration_target instrument2 GroundStation6)
	(supports instrument3 image0)
	(supports instrument3 spectrograph3)
	(supports instrument3 thermograph2)
	(calibration_target instrument3 GroundStation0)
	(calibration_target instrument3 GroundStation5)
	(on_board instrument2 satellite2)
	(on_board instrument3 satellite2)
	(power_avail satellite2)
	(pointing satellite2 GroundStation1)
	(supports instrument4 image1)
	(supports instrument4 thermograph2)
	(supports instrument4 spectrograph3)
	(calibration_target instrument4 GroundStation1)
	(calibration_target instrument4 GroundStation4)
	(on_board instrument4 satellite3)
	(power_avail satellite3)
	(pointing satellite3 GroundStation6)
	(supports instrument5 thermograph2)
	(supports instrument5 spectrograph3)
	(calibration_target instrument5 GroundStation0)
	(supports instrument6 image1)
	(calibration_target instrument6 GroundStation4)
	(on_board instrument5 satellite4)
	(on_board instrument6 satellite4)
	(power_avail satellite4)
	(pointing satellite4 Star12)
)
(:goal (and
	(pointing satellite0 GroundStation4)
	(pointing satellite3 GroundStation5)
	(pointing satellite4 Planet11)
	(have_image Star8 thermograph2)
	(have_image Planet9 spectrograph3)
	(have_image Phenomenon10 thermograph2)
	(have_image Planet11 thermograph2)
	(have_image Star12 thermograph2)
))

)

(define (problem strips-sat-x-1)
(:domain satellite)
(:objects
	satellite0 - satellite
	instrument0 - instrument
	instrument1 - instrument
	satellite1 - satellite
	instrument2 - instrument
	instrument3 - instrument
	satellite2 - satellite
	instrument4 - instrument
	instrument5 - instrument
	satellite3 - satellite
	instrument6 - instrument
	instrument7 - instrument
	satellite4 - satellite
	instrument8 - instrument
	instrument9 - instrument
	thermograph2 - mode
	thermograph0 - mode
	image1 - mode
	GroundStation3 - direction
	Star0 - direction
	Star1 - direction
	GroundStation4 - direction
	Star2 - direction
	Star5 - direction
	Planet6 - direction
	Phenomenon7 - direction
	Star8 - direction
)
(:init
	(supports instrument0 thermograph2)
	(supports instrument0 thermograph0)
	(supports instrument0 image1)
	(calibration_target instrument0 GroundStation4)
	(supports instrument1 thermograph2)
	(calibration_target instrument1 GroundStation4)
	(on_board instrument0 satellite0)
	(on_board instrument1 satellite0)
	(power_avail satellite0)
	(pointing satellite0 GroundStation4)
	(supports instrument2 thermograph0)
	(calibration_target instrument2 GroundStation4)
	(supports instrument3 thermograph0)
	(supports instrument3 thermograph2)
	(calibration_target instrument3 GroundStation3)
	(on_board instrument2 satellite1)
	(on_board instrument3 satellite1)
	(power_avail satellite1)
	(pointing satellite1 Star1)
	(supports instrument4 thermograph2)
	(supports instrument4 image1)
	(supports instrument4 thermograph0)
	(calibration_target instrument4 Star1)
	(supports instrument5 thermograph0)
	(supports instrument5 image1)
	(calibration_target instrument5 Star0)
	(on_board instrument4 satellite2)
	(on_board instrument5 satellite2)
	(power_avail satellite2)
	(pointing satellite2 Planet6)
	(supports instrument6 image1)
	(supports instrument6 thermograph2)
	(supports instrument6 thermograph0)
	(calibration_target instrument6 Star1)
	(supports instrument7 image1)
	(supports instrument7 thermograph2)
	(supports instrument7 thermograph0)
	(calibration_target instrument7 GroundStation4)
	(on_board instrument6 satellite3)
	(on_board instrument7 satellite3)
	(power_avail satellite3)
	(pointing satellite3 Phenomenon7)
	(supports instrument8 thermograph0)
	(supports instrument8 thermograph2)
	(supports instrument8 image1)
	(calibration_target instrument8 Star2)
	(supports instrument9 image1)
	(supports instrument9 thermograph0)
	(supports instrument9 thermograph2)
	(calibration_target instrument9 Star2)
	(on_board instrument8 satellite4)
	(on_board instrument9 satellite4)
	(power_avail satellite4)
	(pointing satellite4 Phenomenon7)
)
(:goal (and
	(pointing satellite0 GroundStation4)
	(pointing satellite1 Star5)
	(pointing satellite2 Phenomenon7)
	(pointing satellite3 Phenomenon7)
	(pointing satellite4 Star8)
	(have_image Star5 thermograph0)
	(have_image Planet6 thermograph2)
	(have_image Phenomenon7 thermograph2)
	(have_image Star8 thermograph2)
))

)

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
	instrument5 - instrument
	satellite2 - satellite
	instrument6 - instrument
	satellite3 - satellite
	instrument7 - instrument
	instrument8 - instrument
	satellite4 - satellite
	instrument9 - instrument
	instrument10 - instrument
	thermograph3 - mode
	thermograph1 - mode
	image2 - mode
	infrared0 - mode
	Star0 - direction
	Star1 - direction
	Planet2 - direction
	Star3 - direction
	Star4 - direction
	Phenomenon5 - direction
	Star6 - direction
)
(:init
	(supports instrument0 infrared0)
	(supports instrument0 image2)
	(supports instrument0 thermograph1)
	(calibration_target instrument0 Star0)
	(supports instrument1 image2)
	(supports instrument1 thermograph3)
	(supports instrument1 infrared0)
	(calibration_target instrument1 Star0)
	(supports instrument2 infrared0)
	(supports instrument2 thermograph1)
	(calibration_target instrument2 Star1)
	(on_board instrument0 satellite0)
	(on_board instrument1 satellite0)
	(on_board instrument2 satellite0)
	(power_avail satellite0)
	(pointing satellite0 Star0)
	(supports instrument3 thermograph1)
	(supports instrument3 infrared0)
	(calibration_target instrument3 Star1)
	(supports instrument4 infrared0)
	(calibration_target instrument4 Star0)
	(supports instrument5 infrared0)
	(supports instrument5 thermograph1)
	(supports instrument5 thermograph3)
	(calibration_target instrument5 Star1)
	(on_board instrument3 satellite1)
	(on_board instrument4 satellite1)
	(on_board instrument5 satellite1)
	(power_avail satellite1)
	(pointing satellite1 Star4)
	(supports instrument6 infrared0)
	(supports instrument6 thermograph1)
	(supports instrument6 image2)
	(calibration_target instrument6 Star1)
	(on_board instrument6 satellite2)
	(power_avail satellite2)
	(pointing satellite2 Star1)
	(supports instrument7 infrared0)
	(supports instrument7 thermograph3)
	(supports instrument7 image2)
	(calibration_target instrument7 Star1)
	(supports instrument8 thermograph1)
	(supports instrument8 thermograph3)
	(calibration_target instrument8 Star0)
	(on_board instrument7 satellite3)
	(on_board instrument8 satellite3)
	(power_avail satellite3)
	(pointing satellite3 Star1)
	(supports instrument9 thermograph3)
	(supports instrument9 infrared0)
	(calibration_target instrument9 Star0)
	(supports instrument10 infrared0)
	(supports instrument10 thermograph3)
	(calibration_target instrument10 Star1)
	(on_board instrument9 satellite4)
	(on_board instrument10 satellite4)
	(power_avail satellite4)
	(pointing satellite4 Star1)
)
(:goal (and
	(pointing satellite0 Star6)
	(pointing satellite2 Star1)
	(pointing satellite4 Star0)
	(have_image Planet2 image2)
	(have_image Star3 thermograph1)
	(have_image Star4 image2)
	(have_image Phenomenon5 image2)
	(have_image Star6 thermograph1)
))

)

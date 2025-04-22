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
	instrument5 - instrument
	instrument6 - instrument
	thermograph1 - mode
	image0 - mode
	thermograph2 - mode
	Star0 - direction
	Star3 - direction
	GroundStation1 - direction
	GroundStation4 - direction
	Star2 - direction
	Phenomenon5 - direction
	Planet6 - direction
	Phenomenon7 - direction
	Phenomenon8 - direction
	Star9 - direction
	Planet10 - direction
	Star11 - direction
	Phenomenon12 - direction
	Planet13 - direction
	Star14 - direction
)
(:init
	(supports instrument0 image0)
	(supports instrument0 thermograph2)
	(supports instrument0 thermograph1)
	(calibration_target instrument0 Star2)
	(on_board instrument0 satellite0)
	(power_avail satellite0)
	(pointing satellite0 Planet13)
	(supports instrument1 thermograph1)
	(calibration_target instrument1 GroundStation4)
	(supports instrument2 thermograph1)
	(supports instrument2 image0)
	(supports instrument2 thermograph2)
	(calibration_target instrument2 GroundStation1)
	(supports instrument3 thermograph2)
	(supports instrument3 thermograph1)
	(supports instrument3 image0)
	(calibration_target instrument3 GroundStation4)
	(on_board instrument1 satellite1)
	(on_board instrument2 satellite1)
	(on_board instrument3 satellite1)
	(power_avail satellite1)
	(pointing satellite1 Phenomenon12)
	(supports instrument4 thermograph2)
	(calibration_target instrument4 GroundStation4)
	(supports instrument5 image0)
	(supports instrument5 thermograph1)
	(supports instrument5 thermograph2)
	(calibration_target instrument5 GroundStation4)
	(supports instrument6 thermograph2)
	(calibration_target instrument6 Star2)
	(on_board instrument4 satellite2)
	(on_board instrument5 satellite2)
	(on_board instrument6 satellite2)
	(power_avail satellite2)
	(pointing satellite2 Star9)
)
(:goal (and
	(pointing satellite2 Planet13)
	(have_image Phenomenon5 image0)
	(have_image Planet6 thermograph2)
	(have_image Phenomenon7 image0)
	(have_image Phenomenon8 image0)
	(have_image Star9 image0)
	(have_image Planet10 thermograph1)
	(have_image Star11 image0)
	(have_image Phenomenon12 image0)
	(have_image Planet13 thermograph2)
	(have_image Star14 thermograph2)
))

)

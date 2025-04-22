(define (problem strips-sat-x-1)
(:domain satellite)
(:objects
	satellite0 - satellite
	instrument0 - instrument
	instrument1 - instrument
	satellite1 - satellite
	instrument2 - instrument
	instrument3 - instrument
	instrument4 - instrument
	satellite2 - satellite
	instrument5 - instrument
	instrument6 - instrument
	satellite3 - satellite
	instrument7 - instrument
	instrument8 - instrument
	instrument9 - instrument
	infrared1 - mode
	image2 - mode
	thermograph0 - mode
	image3 - mode
	Star0 - direction
	GroundStation1 - direction
	Star4 - direction
	Star3 - direction
	GroundStation2 - direction
	Phenomenon5 - direction
	Planet6 - direction
	Phenomenon7 - direction
	Phenomenon8 - direction
	Phenomenon9 - direction
	Phenomenon10 - direction
	Star11 - direction
	Star12 - direction
	Planet13 - direction
	Star14 - direction
)
(:init
	(supports instrument0 thermograph0)
	(supports instrument0 image3)
	(calibration_target instrument0 GroundStation1)
	(supports instrument1 image3)
	(supports instrument1 image2)
	(calibration_target instrument1 GroundStation1)
	(on_board instrument0 satellite0)
	(on_board instrument1 satellite0)
	(power_avail satellite0)
	(pointing satellite0 Planet13)
	(supports instrument2 infrared1)
	(supports instrument2 image3)
	(calibration_target instrument2 Star4)
	(supports instrument3 infrared1)
	(supports instrument3 thermograph0)
	(supports instrument3 image3)
	(calibration_target instrument3 Star4)
	(supports instrument4 thermograph0)
	(calibration_target instrument4 GroundStation2)
	(on_board instrument2 satellite1)
	(on_board instrument3 satellite1)
	(on_board instrument4 satellite1)
	(power_avail satellite1)
	(pointing satellite1 Phenomenon7)
	(supports instrument5 image3)
	(calibration_target instrument5 GroundStation2)
	(supports instrument6 image2)
	(calibration_target instrument6 GroundStation2)
	(on_board instrument5 satellite2)
	(on_board instrument6 satellite2)
	(power_avail satellite2)
	(pointing satellite2 Star14)
	(supports instrument7 thermograph0)
	(supports instrument7 image2)
	(calibration_target instrument7 Star4)
	(supports instrument8 image2)
	(calibration_target instrument8 Star3)
	(supports instrument9 infrared1)
	(calibration_target instrument9 GroundStation2)
	(on_board instrument7 satellite3)
	(on_board instrument8 satellite3)
	(on_board instrument9 satellite3)
	(power_avail satellite3)
	(pointing satellite3 Phenomenon9)
)
(:goal (and
	(pointing satellite0 Star3)
	(have_image Phenomenon5 image3)
	(have_image Planet6 image3)
	(have_image Phenomenon7 infrared1)
	(have_image Phenomenon8 infrared1)
	(have_image Phenomenon9 thermograph0)
	(have_image Phenomenon10 image3)
	(have_image Star11 thermograph0)
	(have_image Star12 thermograph0)
	(have_image Planet13 thermograph0)
	(have_image Star14 thermograph0)
))

)

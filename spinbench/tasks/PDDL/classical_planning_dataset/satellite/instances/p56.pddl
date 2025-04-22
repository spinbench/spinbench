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
	satellite4 - satellite
	instrument9 - instrument
	infrared1 - mode
	image2 - mode
	image3 - mode
	infrared0 - mode
	GroundStation2 - direction
	Star6 - direction
	GroundStation4 - direction
	GroundStation5 - direction
	Star0 - direction
	Star1 - direction
	GroundStation3 - direction
	GroundStation7 - direction
	Star8 - direction
	Planet9 - direction
	Planet10 - direction
	Phenomenon11 - direction
	Planet12 - direction
	Phenomenon13 - direction
	Star14 - direction
	Phenomenon15 - direction
	Planet16 - direction
)
(:init
	(supports instrument0 image3)
	(calibration_target instrument0 Star1)
	(calibration_target instrument0 Star0)
	(supports instrument1 infrared0)
	(supports instrument1 image2)
	(supports instrument1 image3)
	(calibration_target instrument1 Star6)
	(on_board instrument0 satellite0)
	(on_board instrument1 satellite0)
	(power_avail satellite0)
	(pointing satellite0 Planet10)
	(supports instrument2 image2)
	(supports instrument2 image3)
	(supports instrument2 infrared0)
	(calibration_target instrument2 GroundStation7)
	(calibration_target instrument2 GroundStation3)
	(supports instrument3 image3)
	(supports instrument3 infrared1)
	(supports instrument3 image2)
	(calibration_target instrument3 GroundStation5)
	(calibration_target instrument3 GroundStation3)
	(supports instrument4 image3)
	(supports instrument4 infrared0)
	(calibration_target instrument4 Star0)
	(calibration_target instrument4 Star1)
	(on_board instrument2 satellite1)
	(on_board instrument3 satellite1)
	(on_board instrument4 satellite1)
	(power_avail satellite1)
	(pointing satellite1 Star6)
	(supports instrument5 infrared0)
	(supports instrument5 infrared1)
	(calibration_target instrument5 Star0)
	(supports instrument6 infrared1)
	(supports instrument6 image3)
	(supports instrument6 image2)
	(calibration_target instrument6 GroundStation4)
	(on_board instrument5 satellite2)
	(on_board instrument6 satellite2)
	(power_avail satellite2)
	(pointing satellite2 Star6)
	(supports instrument7 infrared0)
	(calibration_target instrument7 GroundStation7)
	(calibration_target instrument7 GroundStation5)
	(supports instrument8 infrared0)
	(supports instrument8 infrared1)
	(calibration_target instrument8 Star1)
	(calibration_target instrument8 Star0)
	(on_board instrument7 satellite3)
	(on_board instrument8 satellite3)
	(power_avail satellite3)
	(pointing satellite3 Phenomenon15)
	(supports instrument9 image2)
	(supports instrument9 image3)
	(supports instrument9 infrared0)
	(calibration_target instrument9 GroundStation7)
	(calibration_target instrument9 GroundStation3)
	(on_board instrument9 satellite4)
	(power_avail satellite4)
	(pointing satellite4 GroundStation3)
)
(:goal (and
	(pointing satellite1 Planet9)
	(pointing satellite2 Star0)
	(have_image Star8 infrared1)
	(have_image Planet9 image2)
	(have_image Planet10 infrared1)
	(have_image Phenomenon11 infrared1)
	(have_image Planet12 image2)
	(have_image Phenomenon13 image3)
	(have_image Star14 infrared1)
	(have_image Phenomenon15 infrared0)
	(have_image Planet16 infrared0)
))

)

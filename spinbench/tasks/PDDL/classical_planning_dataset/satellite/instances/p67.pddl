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
	instrument10 - instrument
	image0 - mode
	image3 - mode
	infrared1 - mode
	image2 - mode
	GroundStation0 - direction
	Star3 - direction
	GroundStation5 - direction
	Star6 - direction
	Star1 - direction
	GroundStation4 - direction
	Star2 - direction
	Star7 - direction
	Star8 - direction
	Planet9 - direction
	Planet10 - direction
	Phenomenon11 - direction
	Star12 - direction
	Planet13 - direction
	Star14 - direction
	Planet15 - direction
)
(:init
	(supports instrument0 image2)
	(calibration_target instrument0 Star7)
	(calibration_target instrument0 Star2)
	(supports instrument1 image0)
	(supports instrument1 infrared1)
	(supports instrument1 image2)
	(calibration_target instrument1 Star1)
	(calibration_target instrument1 Star6)
	(on_board instrument0 satellite0)
	(on_board instrument1 satellite0)
	(power_avail satellite0)
	(pointing satellite0 Planet10)
	(supports instrument2 image0)
	(supports instrument2 infrared1)
	(calibration_target instrument2 GroundStation5)
	(supports instrument3 image0)
	(supports instrument3 image2)
	(supports instrument3 image3)
	(calibration_target instrument3 GroundStation4)
	(calibration_target instrument3 Star7)
	(on_board instrument2 satellite1)
	(on_board instrument3 satellite1)
	(power_avail satellite1)
	(pointing satellite1 Star12)
	(supports instrument4 infrared1)
	(calibration_target instrument4 GroundStation5)
	(supports instrument5 infrared1)
	(calibration_target instrument5 Star1)
	(on_board instrument4 satellite2)
	(on_board instrument5 satellite2)
	(power_avail satellite2)
	(pointing satellite2 Star1)
	(supports instrument6 image2)
	(calibration_target instrument6 Star6)
	(supports instrument7 image2)
	(calibration_target instrument7 Star1)
	(on_board instrument6 satellite3)
	(on_board instrument7 satellite3)
	(power_avail satellite3)
	(pointing satellite3 Phenomenon11)
	(supports instrument8 image0)
	(supports instrument8 image3)
	(supports instrument8 image2)
	(calibration_target instrument8 GroundStation4)
	(calibration_target instrument8 Star1)
	(supports instrument9 image0)
	(supports instrument9 image3)
	(calibration_target instrument9 Star2)
	(calibration_target instrument9 GroundStation4)
	(supports instrument10 image3)
	(calibration_target instrument10 Star7)
	(on_board instrument8 satellite4)
	(on_board instrument9 satellite4)
	(on_board instrument10 satellite4)
	(power_avail satellite4)
	(pointing satellite4 Star3)
)
(:goal (and
	(pointing satellite1 Star6)
	(pointing satellite2 Planet15)
	(pointing satellite4 GroundStation5)
	(have_image Star8 image2)
	(have_image Planet9 image3)
	(have_image Planet10 infrared1)
	(have_image Phenomenon11 image2)
	(have_image Star12 image3)
	(have_image Planet13 image2)
	(have_image Star14 infrared1)
	(have_image Planet15 image0)
))

)

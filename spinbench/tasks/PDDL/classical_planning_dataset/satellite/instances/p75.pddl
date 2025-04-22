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
	instrument7 - instrument
	satellite3 - satellite
	instrument8 - instrument
	instrument9 - instrument
	instrument10 - instrument
	satellite4 - satellite
	instrument11 - instrument
	instrument12 - instrument
	instrument13 - instrument
	image3 - mode
	infrared4 - mode
	image1 - mode
	image0 - mode
	infrared2 - mode
	Star2 - direction
	GroundStation6 - direction
	GroundStation4 - direction
	GroundStation5 - direction
	Star1 - direction
	GroundStation7 - direction
	GroundStation3 - direction
	GroundStation0 - direction
	Planet8 - direction
	Planet9 - direction
	Phenomenon10 - direction
	Phenomenon11 - direction
)
(:init
	(supports instrument0 infrared4)
	(calibration_target instrument0 Star1)
	(supports instrument1 image3)
	(calibration_target instrument1 Star1)
	(supports instrument2 infrared2)
	(supports instrument2 image3)
	(calibration_target instrument2 GroundStation7)
	(calibration_target instrument2 GroundStation0)
	(on_board instrument0 satellite0)
	(on_board instrument1 satellite0)
	(on_board instrument2 satellite0)
	(power_avail satellite0)
	(pointing satellite0 GroundStation6)
	(supports instrument3 image0)
	(supports instrument3 infrared4)
	(calibration_target instrument3 GroundStation4)
	(supports instrument4 image0)
	(supports instrument4 infrared2)
	(calibration_target instrument4 GroundStation3)
	(calibration_target instrument4 GroundStation4)
	(on_board instrument3 satellite1)
	(on_board instrument4 satellite1)
	(power_avail satellite1)
	(pointing satellite1 GroundStation7)
	(supports instrument5 image0)
	(supports instrument5 infrared2)
	(calibration_target instrument5 GroundStation4)
	(calibration_target instrument5 GroundStation0)
	(supports instrument6 infrared2)
	(supports instrument6 image1)
	(calibration_target instrument6 GroundStation4)
	(calibration_target instrument6 GroundStation6)
	(supports instrument7 infrared2)
	(supports instrument7 image0)
	(supports instrument7 image3)
	(calibration_target instrument7 GroundStation7)
	(on_board instrument5 satellite2)
	(on_board instrument6 satellite2)
	(on_board instrument7 satellite2)
	(power_avail satellite2)
	(pointing satellite2 Phenomenon10)
	(supports instrument8 infrared4)
	(calibration_target instrument8 GroundStation5)
	(calibration_target instrument8 GroundStation4)
	(supports instrument9 image1)
	(calibration_target instrument9 GroundStation7)
	(calibration_target instrument9 Star1)
	(supports instrument10 image0)
	(supports instrument10 infrared4)
	(calibration_target instrument10 GroundStation3)
	(on_board instrument8 satellite3)
	(on_board instrument9 satellite3)
	(on_board instrument10 satellite3)
	(power_avail satellite3)
	(pointing satellite3 Star1)
	(supports instrument11 infrared2)
	(calibration_target instrument11 GroundStation3)
	(supports instrument12 image0)
	(supports instrument12 infrared2)
	(calibration_target instrument12 GroundStation0)
	(supports instrument13 image1)
	(calibration_target instrument13 GroundStation0)
	(on_board instrument11 satellite4)
	(on_board instrument12 satellite4)
	(on_board instrument13 satellite4)
	(power_avail satellite4)
	(pointing satellite4 GroundStation6)
)
(:goal (and
	(pointing satellite3 Planet9)
	(have_image Planet8 image3)
	(have_image Planet9 image3)
	(have_image Phenomenon10 image1)
	(have_image Phenomenon11 image1)
))

)

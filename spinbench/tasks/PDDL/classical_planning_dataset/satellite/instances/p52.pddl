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
	satellite3 - satellite
	instrument6 - instrument
	instrument7 - instrument
	instrument8 - instrument
	satellite4 - satellite
	instrument9 - instrument
	instrument10 - instrument
	spectrograph0 - mode
	infrared2 - mode
	infrared4 - mode
	infrared3 - mode
	image1 - mode
	GroundStation2 - direction
	GroundStation0 - direction
	GroundStation3 - direction
	GroundStation1 - direction
	GroundStation5 - direction
	GroundStation4 - direction
	Planet6 - direction
	Phenomenon7 - direction
	Star8 - direction
	Star9 - direction
	Planet10 - direction
	Phenomenon11 - direction
	Planet12 - direction
	Star13 - direction
	Phenomenon14 - direction
	Phenomenon15 - direction
)
(:init
	(supports instrument0 infrared2)
	(calibration_target instrument0 GroundStation4)
	(calibration_target instrument0 GroundStation5)
	(supports instrument1 infrared4)
	(supports instrument1 infrared3)
	(supports instrument1 infrared2)
	(calibration_target instrument1 GroundStation3)
	(on_board instrument0 satellite0)
	(on_board instrument1 satellite0)
	(power_avail satellite0)
	(pointing satellite0 GroundStation1)
	(supports instrument2 spectrograph0)
	(supports instrument2 infrared3)
	(calibration_target instrument2 GroundStation2)
	(calibration_target instrument2 GroundStation4)
	(supports instrument3 image1)
	(supports instrument3 infrared4)
	(supports instrument3 spectrograph0)
	(calibration_target instrument3 GroundStation0)
	(calibration_target instrument3 GroundStation3)
	(supports instrument4 infrared3)
	(calibration_target instrument4 GroundStation1)
	(calibration_target instrument4 GroundStation3)
	(on_board instrument2 satellite1)
	(on_board instrument3 satellite1)
	(on_board instrument4 satellite1)
	(power_avail satellite1)
	(pointing satellite1 Star13)
	(supports instrument5 infrared4)
	(supports instrument5 infrared3)
	(supports instrument5 spectrograph0)
	(calibration_target instrument5 GroundStation0)
	(on_board instrument5 satellite2)
	(power_avail satellite2)
	(pointing satellite2 GroundStation1)
	(supports instrument6 image1)
	(supports instrument6 infrared2)
	(supports instrument6 spectrograph0)
	(calibration_target instrument6 GroundStation1)
	(calibration_target instrument6 GroundStation5)
	(supports instrument7 image1)
	(supports instrument7 infrared2)
	(calibration_target instrument7 GroundStation3)
	(calibration_target instrument7 GroundStation4)
	(supports instrument8 infrared2)
	(calibration_target instrument8 GroundStation1)
	(calibration_target instrument8 GroundStation4)
	(on_board instrument6 satellite3)
	(on_board instrument7 satellite3)
	(on_board instrument8 satellite3)
	(power_avail satellite3)
	(pointing satellite3 GroundStation4)
	(supports instrument9 infrared2)
	(supports instrument9 spectrograph0)
	(calibration_target instrument9 GroundStation4)
	(supports instrument10 infrared3)
	(supports instrument10 image1)
	(calibration_target instrument10 GroundStation4)
	(calibration_target instrument10 GroundStation5)
	(on_board instrument9 satellite4)
	(on_board instrument10 satellite4)
	(power_avail satellite4)
	(pointing satellite4 GroundStation3)
)
(:goal (and
	(pointing satellite1 Star8)
	(pointing satellite2 GroundStation0)
	(pointing satellite3 GroundStation1)
	(have_image Planet6 image1)
	(have_image Phenomenon7 infrared3)
	(have_image Star8 infrared4)
	(have_image Star9 infrared4)
	(have_image Planet10 spectrograph0)
	(have_image Phenomenon11 spectrograph0)
	(have_image Planet12 spectrograph0)
	(have_image Star13 image1)
	(have_image Phenomenon14 spectrograph0)
	(have_image Phenomenon15 infrared4)
))

)

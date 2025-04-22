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
	satellite3 - satellite
	instrument6 - instrument
	instrument7 - instrument
	instrument8 - instrument
	spectrograph1 - mode
	image2 - mode
	infrared0 - mode
	Star0 - direction
	Star1 - direction
	Planet2 - direction
	Phenomenon3 - direction
	Phenomenon4 - direction
)
(:init
	(supports instrument0 infrared0)
	(calibration_target instrument0 Star0)
	(on_board instrument0 satellite0)
	(power_avail satellite0)
	(pointing satellite0 Star0)
	(supports instrument1 spectrograph1)
	(supports instrument1 image2)
	(calibration_target instrument1 Star0)
	(supports instrument2 image2)
	(supports instrument2 spectrograph1)
	(calibration_target instrument2 Star0)
	(supports instrument3 image2)
	(supports instrument3 spectrograph1)
	(supports instrument3 infrared0)
	(calibration_target instrument3 Star0)
	(on_board instrument1 satellite1)
	(on_board instrument2 satellite1)
	(on_board instrument3 satellite1)
	(power_avail satellite1)
	(pointing satellite1 Phenomenon3)
	(supports instrument4 image2)
	(supports instrument4 spectrograph1)
	(supports instrument4 infrared0)
	(calibration_target instrument4 Star0)
	(supports instrument5 image2)
	(calibration_target instrument5 Star0)
	(on_board instrument4 satellite2)
	(on_board instrument5 satellite2)
	(power_avail satellite2)
	(pointing satellite2 Star0)
	(supports instrument6 infrared0)
	(supports instrument6 image2)
	(supports instrument6 spectrograph1)
	(calibration_target instrument6 Star0)
	(supports instrument7 infrared0)
	(calibration_target instrument7 Star0)
	(supports instrument8 infrared0)
	(calibration_target instrument8 Star0)
	(on_board instrument6 satellite3)
	(on_board instrument7 satellite3)
	(on_board instrument8 satellite3)
	(power_avail satellite3)
	(pointing satellite3 Phenomenon3)
)
(:goal (and
	(pointing satellite0 Phenomenon4)
	(pointing satellite3 Star1)
	(have_image Star1 spectrograph1)
	(have_image Planet2 spectrograph1)
	(have_image Phenomenon3 image2)
	(have_image Phenomenon4 image2)
))

)

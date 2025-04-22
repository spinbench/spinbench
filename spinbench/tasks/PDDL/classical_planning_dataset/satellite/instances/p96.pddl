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
	satellite3 - satellite
	instrument5 - instrument
	instrument6 - instrument
	spectrograph1 - mode
	infrared2 - mode
	image0 - mode
	Star2 - direction
	Star0 - direction
	Star1 - direction
	Star3 - direction
	Planet4 - direction
	Star5 - direction
	Phenomenon6 - direction
	Planet7 - direction
	Star8 - direction
	Phenomenon9 - direction
)
(:init
	(supports instrument0 infrared2)
	(supports instrument0 spectrograph1)
	(supports instrument0 image0)
	(calibration_target instrument0 Star2)
	(on_board instrument0 satellite0)
	(power_avail satellite0)
	(pointing satellite0 Star1)
	(supports instrument1 spectrograph1)
	(supports instrument1 infrared2)
	(calibration_target instrument1 Star0)
	(supports instrument2 infrared2)
	(calibration_target instrument2 Star2)
	(supports instrument3 spectrograph1)
	(supports instrument3 image0)
	(supports instrument3 infrared2)
	(calibration_target instrument3 Star0)
	(on_board instrument1 satellite1)
	(on_board instrument2 satellite1)
	(on_board instrument3 satellite1)
	(power_avail satellite1)
	(pointing satellite1 Planet7)
	(supports instrument4 spectrograph1)
	(supports instrument4 image0)
	(calibration_target instrument4 Star2)
	(on_board instrument4 satellite2)
	(power_avail satellite2)
	(pointing satellite2 Star8)
	(supports instrument5 spectrograph1)
	(supports instrument5 image0)
	(supports instrument5 infrared2)
	(calibration_target instrument5 Star0)
	(supports instrument6 infrared2)
	(calibration_target instrument6 Star1)
	(on_board instrument5 satellite3)
	(on_board instrument6 satellite3)
	(power_avail satellite3)
	(pointing satellite3 Star3)
)
(:goal (and
	(pointing satellite0 Planet7)
	(pointing satellite3 Star3)
	(have_image Star3 infrared2)
	(have_image Planet4 spectrograph1)
	(have_image Star5 image0)
	(have_image Phenomenon6 infrared2)
	(have_image Planet7 image0)
	(have_image Star8 infrared2)
	(have_image Phenomenon9 infrared2)
))

)

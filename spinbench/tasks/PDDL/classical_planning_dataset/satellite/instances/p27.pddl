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
	satellite3 - satellite
	instrument7 - instrument
	instrument8 - instrument
	satellite4 - satellite
	instrument9 - instrument
	instrument10 - instrument
	infrared3 - mode
	spectrograph0 - mode
	infrared1 - mode
	spectrograph4 - mode
	infrared2 - mode
	GroundStation5 - direction
	GroundStation6 - direction
	GroundStation1 - direction
	Star2 - direction
	Star4 - direction
	Star3 - direction
	Star0 - direction
	Planet7 - direction
	Phenomenon8 - direction
	Phenomenon9 - direction
	Star10 - direction
	Phenomenon11 - direction
	Star12 - direction
	Star13 - direction
)
(:init
	(supports instrument0 infrared1)
	(supports instrument0 spectrograph4)
	(calibration_target instrument0 Star3)
	(on_board instrument0 satellite0)
	(power_avail satellite0)
	(pointing satellite0 Star4)
	(supports instrument1 infrared2)
	(supports instrument1 spectrograph0)
	(calibration_target instrument1 Star2)
	(supports instrument2 infrared2)
	(supports instrument2 spectrograph4)
	(calibration_target instrument2 Star0)
	(calibration_target instrument2 GroundStation5)
	(supports instrument3 spectrograph4)
	(supports instrument3 infrared3)
	(calibration_target instrument3 GroundStation6)
	(calibration_target instrument3 GroundStation1)
	(on_board instrument1 satellite1)
	(on_board instrument2 satellite1)
	(on_board instrument3 satellite1)
	(power_avail satellite1)
	(pointing satellite1 Star0)
	(supports instrument4 spectrograph0)
	(calibration_target instrument4 Star0)
	(supports instrument5 spectrograph0)
	(supports instrument5 infrared1)
	(calibration_target instrument5 Star0)
	(supports instrument6 infrared2)
	(supports instrument6 infrared3)
	(supports instrument6 spectrograph4)
	(calibration_target instrument6 GroundStation1)
	(calibration_target instrument6 Star0)
	(on_board instrument4 satellite2)
	(on_board instrument5 satellite2)
	(on_board instrument6 satellite2)
	(power_avail satellite2)
	(pointing satellite2 Phenomenon8)
	(supports instrument7 spectrograph0)
	(supports instrument7 infrared1)
	(supports instrument7 infrared3)
	(calibration_target instrument7 Star2)
	(supports instrument8 spectrograph0)
	(calibration_target instrument8 Star4)
	(on_board instrument7 satellite3)
	(on_board instrument8 satellite3)
	(power_avail satellite3)
	(pointing satellite3 Star3)
	(supports instrument9 infrared3)
	(calibration_target instrument9 Star3)
	(supports instrument10 infrared2)
	(supports instrument10 infrared3)
	(calibration_target instrument10 Star0)
	(on_board instrument9 satellite4)
	(on_board instrument10 satellite4)
	(power_avail satellite4)
	(pointing satellite4 Planet7)
)
(:goal (and
	(pointing satellite1 Star12)
	(pointing satellite2 Star12)
	(pointing satellite4 Phenomenon9)
	(have_image Planet7 infrared3)
	(have_image Phenomenon8 infrared1)
	(have_image Phenomenon9 spectrograph0)
	(have_image Star10 infrared1)
	(have_image Phenomenon11 infrared2)
	(have_image Star12 infrared3)
	(have_image Star13 infrared1)
))

)

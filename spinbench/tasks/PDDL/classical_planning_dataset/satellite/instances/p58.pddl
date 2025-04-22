(define (problem strips-sat-x-1)
(:domain satellite)
(:objects
	satellite0 - satellite
	instrument0 - instrument
	satellite1 - satellite
	instrument1 - instrument
	satellite2 - satellite
	instrument2 - instrument
	instrument3 - instrument
	instrument4 - instrument
	satellite3 - satellite
	instrument5 - instrument
	instrument6 - instrument
	instrument7 - instrument
	thermograph0 - mode
	infrared3 - mode
	spectrograph4 - mode
	infrared2 - mode
	thermograph1 - mode
	Star8 - direction
	GroundStation3 - direction
	GroundStation6 - direction
	Star9 - direction
	Star1 - direction
	GroundStation5 - direction
	GroundStation0 - direction
	GroundStation4 - direction
	Star7 - direction
	Star2 - direction
	Star10 - direction
	Planet11 - direction
	Planet12 - direction
	Star13 - direction
	Phenomenon14 - direction
	Planet15 - direction
	Phenomenon16 - direction
	Planet17 - direction
	Star18 - direction
)
(:init
	(supports instrument0 spectrograph4)
	(calibration_target instrument0 GroundStation0)
	(calibration_target instrument0 Star7)
	(on_board instrument0 satellite0)
	(power_avail satellite0)
	(pointing satellite0 Phenomenon14)
	(supports instrument1 spectrograph4)
	(supports instrument1 thermograph0)
	(calibration_target instrument1 GroundStation3)
	(calibration_target instrument1 Star9)
	(calibration_target instrument1 Star1)
	(on_board instrument1 satellite1)
	(power_avail satellite1)
	(pointing satellite1 Star7)
	(supports instrument2 infrared2)
	(calibration_target instrument2 GroundStation6)
	(calibration_target instrument2 Star2)
	(supports instrument3 infrared2)
	(supports instrument3 thermograph0)
	(calibration_target instrument3 Star9)
	(supports instrument4 thermograph1)
	(supports instrument4 thermograph0)
	(calibration_target instrument4 Star9)
	(calibration_target instrument4 Star2)
	(calibration_target instrument4 GroundStation0)
	(on_board instrument2 satellite2)
	(on_board instrument3 satellite2)
	(on_board instrument4 satellite2)
	(power_avail satellite2)
	(pointing satellite2 GroundStation5)
	(supports instrument5 infrared3)
	(supports instrument5 infrared2)
	(supports instrument5 spectrograph4)
	(calibration_target instrument5 Star7)
	(calibration_target instrument5 Star1)
	(supports instrument6 thermograph1)
	(supports instrument6 thermograph0)
	(calibration_target instrument6 GroundStation4)
	(calibration_target instrument6 GroundStation0)
	(calibration_target instrument6 GroundStation5)
	(supports instrument7 spectrograph4)
	(supports instrument7 infrared2)
	(calibration_target instrument7 Star2)
	(calibration_target instrument7 Star7)
	(on_board instrument5 satellite3)
	(on_board instrument6 satellite3)
	(on_board instrument7 satellite3)
	(power_avail satellite3)
	(pointing satellite3 Planet11)
)
(:goal (and
	(pointing satellite2 GroundStation0)
	(have_image Star10 thermograph0)
	(have_image Planet11 infrared2)
	(have_image Planet12 infrared2)
	(have_image Star13 thermograph0)
	(have_image Phenomenon14 spectrograph4)
	(have_image Planet15 spectrograph4)
	(have_image Phenomenon16 spectrograph4)
	(have_image Planet17 infrared2)
	(have_image Star18 infrared3)
))

)

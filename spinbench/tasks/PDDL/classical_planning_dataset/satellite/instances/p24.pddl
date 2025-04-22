(define (problem strips-sat-x-1)
(:domain satellite)
(:objects
	satellite0 - satellite
	instrument0 - instrument
	instrument1 - instrument
	instrument2 - instrument
	satellite1 - satellite
	instrument3 - instrument
	satellite2 - satellite
	instrument4 - instrument
	satellite3 - satellite
	instrument5 - instrument
	instrument6 - instrument
	satellite4 - satellite
	instrument7 - instrument
	instrument8 - instrument
	thermograph1 - mode
	thermograph4 - mode
	infrared2 - mode
	infrared0 - mode
	spectrograph3 - mode
	Star3 - direction
	GroundStation7 - direction
	GroundStation8 - direction
	Star9 - direction
	GroundStation6 - direction
	Star0 - direction
	GroundStation2 - direction
	GroundStation5 - direction
	GroundStation1 - direction
	Star4 - direction
	Star10 - direction
	Planet11 - direction
	Planet12 - direction
	Phenomenon13 - direction
	Star14 - direction
	Star15 - direction
	Phenomenon16 - direction
)
(:init
	(supports instrument0 infrared2)
	(supports instrument0 thermograph1)
	(calibration_target instrument0 GroundStation8)
	(calibration_target instrument0 Star9)
	(calibration_target instrument0 Star4)
	(supports instrument1 infrared0)
	(calibration_target instrument1 GroundStation1)
	(calibration_target instrument1 GroundStation5)
	(calibration_target instrument1 GroundStation8)
	(supports instrument2 infrared0)
	(supports instrument2 thermograph1)
	(supports instrument2 spectrograph3)
	(calibration_target instrument2 GroundStation2)
	(calibration_target instrument2 Star4)
	(on_board instrument0 satellite0)
	(on_board instrument1 satellite0)
	(on_board instrument2 satellite0)
	(power_avail satellite0)
	(pointing satellite0 Star4)
	(supports instrument3 infrared2)
	(calibration_target instrument3 Star9)
	(calibration_target instrument3 GroundStation8)
	(calibration_target instrument3 GroundStation5)
	(on_board instrument3 satellite1)
	(power_avail satellite1)
	(pointing satellite1 Star14)
	(supports instrument4 infrared0)
	(supports instrument4 thermograph4)
	(supports instrument4 thermograph1)
	(calibration_target instrument4 GroundStation5)
	(calibration_target instrument4 GroundStation6)
	(calibration_target instrument4 Star0)
	(on_board instrument4 satellite2)
	(power_avail satellite2)
	(pointing satellite2 Star10)
	(supports instrument5 infrared2)
	(calibration_target instrument5 Star0)
	(supports instrument6 thermograph4)
	(supports instrument6 spectrograph3)
	(calibration_target instrument6 Star0)
	(calibration_target instrument6 GroundStation5)
	(calibration_target instrument6 GroundStation6)
	(on_board instrument5 satellite3)
	(on_board instrument6 satellite3)
	(power_avail satellite3)
	(pointing satellite3 Planet12)
	(supports instrument7 spectrograph3)
	(supports instrument7 thermograph4)
	(calibration_target instrument7 GroundStation1)
	(calibration_target instrument7 GroundStation5)
	(calibration_target instrument7 GroundStation2)
	(supports instrument8 infrared2)
	(calibration_target instrument8 Star4)
	(on_board instrument7 satellite4)
	(on_board instrument8 satellite4)
	(power_avail satellite4)
	(pointing satellite4 Star3)
)
(:goal (and
	(pointing satellite0 Star9)
	(pointing satellite1 Planet11)
	(pointing satellite4 Star10)
	(have_image Star10 spectrograph3)
	(have_image Planet11 thermograph4)
	(have_image Planet12 thermograph4)
	(have_image Phenomenon13 infrared2)
	(have_image Star14 thermograph4)
	(have_image Star15 infrared2)
	(have_image Phenomenon16 thermograph4)
))

)

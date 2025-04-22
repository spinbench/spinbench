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
	thermograph2 - mode
	infrared0 - mode
	image1 - mode
	spectrograph3 - mode
	thermograph4 - mode
	GroundStation2 - direction
	Star0 - direction
	GroundStation1 - direction
	Phenomenon3 - direction
	Star4 - direction
	Planet5 - direction
	Phenomenon6 - direction
	Phenomenon7 - direction
	Star8 - direction
	Phenomenon9 - direction
	Phenomenon10 - direction
	Star11 - direction
)
(:init
	(supports instrument0 infrared0)
	(calibration_target instrument0 GroundStation1)
	(supports instrument1 spectrograph3)
	(supports instrument1 infrared0)
	(supports instrument1 image1)
	(calibration_target instrument1 Star0)
	(supports instrument2 image1)
	(supports instrument2 thermograph4)
	(supports instrument2 thermograph2)
	(calibration_target instrument2 GroundStation2)
	(on_board instrument0 satellite0)
	(on_board instrument1 satellite0)
	(on_board instrument2 satellite0)
	(power_avail satellite0)
	(pointing satellite0 Star0)
	(supports instrument3 image1)
	(calibration_target instrument3 GroundStation1)
	(supports instrument4 image1)
	(supports instrument4 thermograph4)
	(calibration_target instrument4 GroundStation2)
	(on_board instrument3 satellite1)
	(on_board instrument4 satellite1)
	(power_avail satellite1)
	(pointing satellite1 Planet5)
	(supports instrument5 image1)
	(supports instrument5 thermograph4)
	(supports instrument5 spectrograph3)
	(calibration_target instrument5 GroundStation1)
	(supports instrument6 thermograph2)
	(supports instrument6 infrared0)
	(calibration_target instrument6 Star0)
	(supports instrument7 spectrograph3)
	(supports instrument7 thermograph2)
	(calibration_target instrument7 Star0)
	(on_board instrument5 satellite2)
	(on_board instrument6 satellite2)
	(on_board instrument7 satellite2)
	(power_avail satellite2)
	(pointing satellite2 Star4)
	(supports instrument8 thermograph2)
	(supports instrument8 image1)
	(calibration_target instrument8 GroundStation1)
	(on_board instrument8 satellite3)
	(power_avail satellite3)
	(pointing satellite3 Phenomenon10)
)
(:goal (and
	(pointing satellite2 Phenomenon10)
	(have_image Phenomenon3 thermograph2)
	(have_image Star4 spectrograph3)
	(have_image Planet5 spectrograph3)
	(have_image Phenomenon6 infrared0)
	(have_image Phenomenon7 spectrograph3)
	(have_image Star8 spectrograph3)
	(have_image Phenomenon9 thermograph2)
	(have_image Phenomenon10 infrared0)
	(have_image Star11 spectrograph3)
))

)

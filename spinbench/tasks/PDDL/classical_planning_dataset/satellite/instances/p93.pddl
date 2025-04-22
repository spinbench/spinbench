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
	spectrograph3 - mode
	thermograph1 - mode
	spectrograph2 - mode
	thermograph0 - mode
	image4 - mode
	Star2 - direction
	GroundStation4 - direction
	GroundStation1 - direction
	Star3 - direction
	GroundStation0 - direction
	Planet5 - direction
	Star6 - direction
	Planet7 - direction
	Planet8 - direction
	Planet9 - direction
	Phenomenon10 - direction
	Phenomenon11 - direction
	Star12 - direction
	Star13 - direction
	Star14 - direction
)
(:init
	(supports instrument0 thermograph0)
	(supports instrument0 spectrograph3)
	(calibration_target instrument0 GroundStation1)
	(supports instrument1 spectrograph2)
	(supports instrument1 spectrograph3)
	(supports instrument1 image4)
	(calibration_target instrument1 GroundStation1)
	(on_board instrument0 satellite0)
	(on_board instrument1 satellite0)
	(power_avail satellite0)
	(pointing satellite0 Planet9)
	(supports instrument2 spectrograph3)
	(calibration_target instrument2 Star3)
	(supports instrument3 spectrograph3)
	(supports instrument3 image4)
	(supports instrument3 thermograph1)
	(calibration_target instrument3 GroundStation0)
	(supports instrument4 spectrograph3)
	(calibration_target instrument4 GroundStation1)
	(on_board instrument2 satellite1)
	(on_board instrument3 satellite1)
	(on_board instrument4 satellite1)
	(power_avail satellite1)
	(pointing satellite1 Phenomenon10)
	(supports instrument5 spectrograph3)
	(calibration_target instrument5 GroundStation1)
	(on_board instrument5 satellite2)
	(power_avail satellite2)
	(pointing satellite2 Planet5)
	(supports instrument6 image4)
	(supports instrument6 thermograph1)
	(supports instrument6 thermograph0)
	(calibration_target instrument6 GroundStation0)
	(supports instrument7 thermograph1)
	(supports instrument7 spectrograph3)
	(calibration_target instrument7 Star3)
	(supports instrument8 spectrograph2)
	(calibration_target instrument8 GroundStation0)
	(on_board instrument6 satellite3)
	(on_board instrument7 satellite3)
	(on_board instrument8 satellite3)
	(power_avail satellite3)
	(pointing satellite3 Star13)
	(supports instrument9 thermograph1)
	(supports instrument9 spectrograph2)
	(supports instrument9 thermograph0)
	(calibration_target instrument9 GroundStation0)
	(on_board instrument9 satellite4)
	(power_avail satellite4)
	(pointing satellite4 Star2)
)
(:goal (and
	(pointing satellite1 GroundStation4)
	(pointing satellite3 GroundStation0)
	(have_image Planet5 spectrograph3)
	(have_image Star6 spectrograph3)
	(have_image Planet7 image4)
	(have_image Planet8 thermograph1)
	(have_image Planet9 image4)
	(have_image Phenomenon10 image4)
	(have_image Phenomenon11 spectrograph3)
	(have_image Star12 spectrograph2)
	(have_image Star13 thermograph0)
	(have_image Star14 spectrograph3)
))

)

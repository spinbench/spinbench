(define (problem strips-sat-x-1)
(:domain satellite)
(:objects
	satellite0 - satellite
	instrument0 - instrument
	instrument1 - instrument
	satellite1 - satellite
	instrument2 - instrument
	satellite2 - satellite
	instrument3 - instrument
	instrument4 - instrument
	instrument5 - instrument
	satellite3 - satellite
	instrument6 - instrument
	instrument7 - instrument
	thermograph1 - mode
	spectrograph3 - mode
	spectrograph0 - mode
	image2 - mode
	GroundStation2 - direction
	Star3 - direction
	Star0 - direction
	GroundStation1 - direction
	Star4 - direction
	Star5 - direction
	Planet6 - direction
	Planet7 - direction
	Planet8 - direction
	Planet9 - direction
	Phenomenon10 - direction
	Phenomenon11 - direction
	Planet12 - direction
)
(:init
	(supports instrument0 spectrograph0)
	(supports instrument0 spectrograph3)
	(calibration_target instrument0 Star0)
	(supports instrument1 image2)
	(calibration_target instrument1 Star3)
	(on_board instrument0 satellite0)
	(on_board instrument1 satellite0)
	(power_avail satellite0)
	(pointing satellite0 Star0)
	(supports instrument2 thermograph1)
	(supports instrument2 spectrograph3)
	(supports instrument2 spectrograph0)
	(calibration_target instrument2 GroundStation1)
	(on_board instrument2 satellite1)
	(power_avail satellite1)
	(pointing satellite1 Planet8)
	(supports instrument3 thermograph1)
	(supports instrument3 spectrograph0)
	(supports instrument3 image2)
	(calibration_target instrument3 Star0)
	(supports instrument4 thermograph1)
	(supports instrument4 spectrograph3)
	(supports instrument4 image2)
	(calibration_target instrument4 Star3)
	(supports instrument5 spectrograph0)
	(supports instrument5 spectrograph3)
	(supports instrument5 thermograph1)
	(calibration_target instrument5 Star0)
	(on_board instrument3 satellite2)
	(on_board instrument4 satellite2)
	(on_board instrument5 satellite2)
	(power_avail satellite2)
	(pointing satellite2 Planet8)
	(supports instrument6 image2)
	(calibration_target instrument6 Star0)
	(supports instrument7 image2)
	(supports instrument7 thermograph1)
	(calibration_target instrument7 GroundStation1)
	(on_board instrument6 satellite3)
	(on_board instrument7 satellite3)
	(power_avail satellite3)
	(pointing satellite3 Star0)
)
(:goal (and
	(pointing satellite1 GroundStation1)
	(pointing satellite3 Planet12)
	(have_image Star4 spectrograph0)
	(have_image Star5 image2)
	(have_image Planet6 spectrograph3)
	(have_image Planet7 spectrograph3)
	(have_image Planet8 image2)
	(have_image Planet9 spectrograph0)
	(have_image Phenomenon10 thermograph1)
	(have_image Phenomenon11 image2)
	(have_image Planet12 spectrograph3)
))

)

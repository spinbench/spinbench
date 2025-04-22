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
	image1 - mode
	spectrograph3 - mode
	infrared0 - mode
	thermograph2 - mode
	Star1 - direction
	Star3 - direction
	Star2 - direction
	Star0 - direction
	Star4 - direction
	Star5 - direction
	Star6 - direction
	Star7 - direction
	Phenomenon8 - direction
	Planet9 - direction
	Planet10 - direction
	Planet11 - direction
	Phenomenon12 - direction
)
(:init
	(supports instrument0 thermograph2)
	(supports instrument0 spectrograph3)
	(supports instrument0 image1)
	(calibration_target instrument0 Star2)
	(on_board instrument0 satellite0)
	(power_avail satellite0)
	(pointing satellite0 Star7)
	(supports instrument1 thermograph2)
	(supports instrument1 image1)
	(supports instrument1 infrared0)
	(calibration_target instrument1 Star2)
	(supports instrument2 image1)
	(supports instrument2 infrared0)
	(calibration_target instrument2 Star2)
	(supports instrument3 thermograph2)
	(supports instrument3 image1)
	(calibration_target instrument3 Star0)
	(on_board instrument1 satellite1)
	(on_board instrument2 satellite1)
	(on_board instrument3 satellite1)
	(power_avail satellite1)
	(pointing satellite1 Star5)
	(supports instrument4 spectrograph3)
	(calibration_target instrument4 Star0)
	(supports instrument5 spectrograph3)
	(supports instrument5 image1)
	(calibration_target instrument5 Star4)
	(on_board instrument4 satellite2)
	(on_board instrument5 satellite2)
	(power_avail satellite2)
	(pointing satellite2 Star4)
)
(:goal (and
	(pointing satellite1 Star7)
	(have_image Star5 thermograph2)
	(have_image Star6 infrared0)
	(have_image Star7 image1)
	(have_image Phenomenon8 image1)
	(have_image Planet9 image1)
	(have_image Planet10 thermograph2)
	(have_image Planet11 thermograph2)
	(have_image Phenomenon12 infrared0)
))

)

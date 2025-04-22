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
	spectrograph0 - mode
	image1 - mode
	thermograph2 - mode
	Star0 - direction
	GroundStation3 - direction
	GroundStation4 - direction
	Star1 - direction
	Star2 - direction
	GroundStation6 - direction
	GroundStation5 - direction
	Star7 - direction
	Star8 - direction
	Planet9 - direction
	Star10 - direction
)
(:init
	(supports instrument0 spectrograph0)
	(supports instrument0 image1)
	(calibration_target instrument0 Star1)
	(on_board instrument0 satellite0)
	(power_avail satellite0)
	(pointing satellite0 Star2)
	(supports instrument1 thermograph2)
	(calibration_target instrument1 GroundStation6)
	(supports instrument2 image1)
	(supports instrument2 spectrograph0)
	(calibration_target instrument2 Star2)
	(supports instrument3 spectrograph0)
	(supports instrument3 image1)
	(calibration_target instrument3 GroundStation5)
	(calibration_target instrument3 Star2)
	(on_board instrument1 satellite1)
	(on_board instrument2 satellite1)
	(on_board instrument3 satellite1)
	(power_avail satellite1)
	(pointing satellite1 GroundStation4)
	(supports instrument4 spectrograph0)
	(calibration_target instrument4 GroundStation5)
	(calibration_target instrument4 GroundStation6)
	(on_board instrument4 satellite2)
	(power_avail satellite2)
	(pointing satellite2 GroundStation5)
)
(:goal (and
	(pointing satellite1 GroundStation3)
	(have_image Star7 image1)
	(have_image Star8 image1)
	(have_image Planet9 spectrograph0)
	(have_image Star10 spectrograph0)
))

)

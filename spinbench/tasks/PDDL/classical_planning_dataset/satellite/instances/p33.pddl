(define (problem strips-sat-x-1)
(:domain satellite)
(:objects
	satellite0 - satellite
	instrument0 - instrument
	instrument1 - instrument
	instrument2 - instrument
	satellite1 - satellite
	instrument3 - instrument
	image0 - mode
	image2 - mode
	spectrograph3 - mode
	spectrograph1 - mode
	Star2 - direction
	Star3 - direction
	GroundStation1 - direction
	GroundStation7 - direction
	Star9 - direction
	GroundStation5 - direction
	Star4 - direction
	Star0 - direction
	GroundStation6 - direction
	Star8 - direction
	Planet10 - direction
	Planet11 - direction
	Phenomenon12 - direction
	Star13 - direction
	Planet14 - direction
	Star15 - direction
	Phenomenon16 - direction
	Phenomenon17 - direction
)
(:init
	(supports instrument0 spectrograph3)
	(supports instrument0 spectrograph1)
	(calibration_target instrument0 Star9)
	(calibration_target instrument0 GroundStation1)
	(supports instrument1 spectrograph1)
	(supports instrument1 image0)
	(supports instrument1 image2)
	(calibration_target instrument1 Star9)
	(calibration_target instrument1 Star4)
	(calibration_target instrument1 GroundStation7)
	(supports instrument2 image0)
	(supports instrument2 image2)
	(supports instrument2 spectrograph3)
	(calibration_target instrument2 Star0)
	(calibration_target instrument2 Star4)
	(calibration_target instrument2 GroundStation5)
	(on_board instrument0 satellite0)
	(on_board instrument1 satellite0)
	(on_board instrument2 satellite0)
	(power_avail satellite0)
	(pointing satellite0 Star13)
	(supports instrument3 image0)
	(supports instrument3 spectrograph1)
	(supports instrument3 image2)
	(calibration_target instrument3 Star8)
	(calibration_target instrument3 GroundStation6)
	(calibration_target instrument3 Star0)
	(on_board instrument3 satellite1)
	(power_avail satellite1)
	(pointing satellite1 GroundStation1)
)
(:goal (and
	(pointing satellite0 Star2)
	(have_image Planet10 spectrograph1)
	(have_image Planet11 spectrograph3)
	(have_image Phenomenon12 spectrograph3)
	(have_image Star13 spectrograph3)
	(have_image Planet14 spectrograph1)
	(have_image Star15 spectrograph3)
	(have_image Phenomenon16 image2)
	(have_image Phenomenon17 spectrograph1)
))

)

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
	thermograph3 - mode
	spectrograph4 - mode
	thermograph2 - mode
	image0 - mode
	image1 - mode
	Star1 - direction
	GroundStation2 - direction
	Star7 - direction
	Star6 - direction
	GroundStation3 - direction
	GroundStation4 - direction
	GroundStation5 - direction
	GroundStation0 - direction
	Phenomenon8 - direction
	Star9 - direction
	Phenomenon10 - direction
	Planet11 - direction
	Planet12 - direction
	Star13 - direction
	Planet14 - direction
	Planet15 - direction
	Phenomenon16 - direction
)
(:init
	(supports instrument0 image0)
	(supports instrument0 thermograph3)
	(supports instrument0 thermograph2)
	(calibration_target instrument0 GroundStation5)
	(calibration_target instrument0 Star6)
	(supports instrument1 thermograph3)
	(supports instrument1 spectrograph4)
	(supports instrument1 image1)
	(calibration_target instrument1 GroundStation0)
	(on_board instrument0 satellite0)
	(on_board instrument1 satellite0)
	(power_avail satellite0)
	(pointing satellite0 GroundStation0)
	(supports instrument2 image1)
	(supports instrument2 thermograph2)
	(calibration_target instrument2 GroundStation4)
	(calibration_target instrument2 GroundStation3)
	(on_board instrument2 satellite1)
	(power_avail satellite1)
	(pointing satellite1 Phenomenon8)
	(supports instrument3 spectrograph4)
	(calibration_target instrument3 GroundStation0)
	(calibration_target instrument3 GroundStation5)
	(on_board instrument3 satellite2)
	(power_avail satellite2)
	(pointing satellite2 GroundStation3)
)
(:goal (and
	(pointing satellite0 Star6)
	(have_image Phenomenon8 image1)
	(have_image Star9 thermograph3)
	(have_image Phenomenon10 image0)
	(have_image Planet11 image0)
	(have_image Planet12 thermograph3)
	(have_image Star13 thermograph3)
	(have_image Planet14 image1)
	(have_image Planet15 spectrograph4)
	(have_image Phenomenon16 thermograph3)
))

)

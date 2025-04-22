(define (problem strips-sat-x-1)
(:domain satellite)
(:objects
	satellite0 - satellite
	instrument0 - instrument
	satellite1 - satellite
	instrument1 - instrument
	instrument2 - instrument
	instrument3 - instrument
	infrared4 - mode
	thermograph3 - mode
	thermograph1 - mode
	image2 - mode
	spectrograph0 - mode
	GroundStation3 - direction
	GroundStation0 - direction
	GroundStation2 - direction
	GroundStation1 - direction
	Planet4 - direction
	Planet5 - direction
	Star6 - direction
	Phenomenon7 - direction
	Phenomenon8 - direction
	Star9 - direction
	Phenomenon10 - direction
	Phenomenon11 - direction
	Phenomenon12 - direction
	Star13 - direction
)
(:init
	(supports instrument0 spectrograph0)
	(supports instrument0 image2)
	(calibration_target instrument0 GroundStation2)
	(on_board instrument0 satellite0)
	(power_avail satellite0)
	(pointing satellite0 GroundStation3)
	(supports instrument1 infrared4)
	(calibration_target instrument1 GroundStation0)
	(supports instrument2 thermograph3)
	(supports instrument2 thermograph1)
	(calibration_target instrument2 GroundStation2)
	(supports instrument3 thermograph3)
	(calibration_target instrument3 GroundStation1)
	(on_board instrument1 satellite1)
	(on_board instrument2 satellite1)
	(on_board instrument3 satellite1)
	(power_avail satellite1)
	(pointing satellite1 Phenomenon12)
)
(:goal (and
	(have_image Planet4 image2)
	(have_image Planet5 spectrograph0)
	(have_image Star6 thermograph1)
	(have_image Phenomenon7 spectrograph0)
	(have_image Phenomenon8 image2)
	(have_image Star9 image2)
	(have_image Phenomenon10 image2)
	(have_image Phenomenon11 thermograph3)
	(have_image Phenomenon12 image2)
	(have_image Star13 thermograph3)
))

)

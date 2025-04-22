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
	instrument5 - instrument
	satellite2 - satellite
	instrument6 - instrument
	spectrograph1 - mode
	infrared2 - mode
	spectrograph0 - mode
	GroundStation2 - direction
	GroundStation1 - direction
	GroundStation0 - direction
	Star3 - direction
	Star4 - direction
	Phenomenon5 - direction
	Star6 - direction
	Star7 - direction
	Planet8 - direction
	Planet9 - direction
)
(:init
	(supports instrument0 infrared2)
	(supports instrument0 spectrograph1)
	(calibration_target instrument0 GroundStation2)
	(supports instrument1 infrared2)
	(calibration_target instrument1 Star3)
	(supports instrument2 infrared2)
	(calibration_target instrument2 GroundStation1)
	(on_board instrument0 satellite0)
	(on_board instrument1 satellite0)
	(on_board instrument2 satellite0)
	(power_avail satellite0)
	(pointing satellite0 Star4)
	(supports instrument3 spectrograph0)
	(supports instrument3 spectrograph1)
	(supports instrument3 infrared2)
	(calibration_target instrument3 GroundStation1)
	(supports instrument4 spectrograph1)
	(supports instrument4 spectrograph0)
	(supports instrument4 infrared2)
	(calibration_target instrument4 GroundStation0)
	(supports instrument5 spectrograph1)
	(supports instrument5 spectrograph0)
	(calibration_target instrument5 GroundStation0)
	(on_board instrument3 satellite1)
	(on_board instrument4 satellite1)
	(on_board instrument5 satellite1)
	(power_avail satellite1)
	(pointing satellite1 GroundStation2)
	(supports instrument6 spectrograph1)
	(supports instrument6 infrared2)
	(supports instrument6 spectrograph0)
	(calibration_target instrument6 Star3)
	(on_board instrument6 satellite2)
	(power_avail satellite2)
	(pointing satellite2 GroundStation0)
)
(:goal (and
	(pointing satellite1 Star7)
	(pointing satellite2 Star7)
	(have_image Star4 infrared2)
	(have_image Phenomenon5 spectrograph1)
	(have_image Star6 spectrograph0)
	(have_image Star7 infrared2)
	(have_image Planet8 infrared2)
	(have_image Planet9 spectrograph0)
))

)

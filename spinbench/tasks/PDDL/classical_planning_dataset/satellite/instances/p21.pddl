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
	spectrograph0 - mode
	infrared1 - mode
	spectrograph3 - mode
	image2 - mode
	infrared4 - mode
	Star2 - direction
	GroundStation1 - direction
	GroundStation0 - direction
	Planet3 - direction
	Planet4 - direction
	Planet5 - direction
)
(:init
	(supports instrument0 spectrograph3)
	(supports instrument0 infrared1)
	(calibration_target instrument0 GroundStation1)
	(supports instrument1 infrared1)
	(supports instrument1 image2)
	(supports instrument1 infrared4)
	(calibration_target instrument1 Star2)
	(supports instrument2 spectrograph0)
	(calibration_target instrument2 GroundStation0)
	(on_board instrument0 satellite0)
	(on_board instrument1 satellite0)
	(on_board instrument2 satellite0)
	(power_avail satellite0)
	(pointing satellite0 Planet4)
	(supports instrument3 spectrograph3)
	(calibration_target instrument3 GroundStation0)
	(supports instrument4 image2)
	(calibration_target instrument4 GroundStation1)
	(supports instrument5 infrared4)
	(supports instrument5 spectrograph3)
	(calibration_target instrument5 GroundStation1)
	(on_board instrument3 satellite1)
	(on_board instrument4 satellite1)
	(on_board instrument5 satellite1)
	(power_avail satellite1)
	(pointing satellite1 Star2)
	(supports instrument6 spectrograph0)
	(supports instrument6 infrared4)
	(supports instrument6 image2)
	(calibration_target instrument6 GroundStation0)
	(on_board instrument6 satellite2)
	(power_avail satellite2)
	(pointing satellite2 Planet3)
)
(:goal (and
	(pointing satellite2 Planet3)
	(have_image Planet3 spectrograph0)
	(have_image Planet4 spectrograph0)
	(have_image Planet5 image2)
))

)

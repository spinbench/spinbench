(define (problem strips-sat-x-1)
(:domain satellite)
(:objects
	satellite0 - satellite
	instrument0 - instrument
	instrument1 - instrument
	satellite1 - satellite
	instrument2 - instrument
	instrument3 - instrument
	satellite2 - satellite
	instrument4 - instrument
	satellite3 - satellite
	instrument5 - instrument
	instrument6 - instrument
	instrument7 - instrument
	thermograph0 - mode
	infrared3 - mode
	infrared1 - mode
	spectrograph2 - mode
	Star0 - direction
	GroundStation1 - direction
	Star3 - direction
	Star2 - direction
	Phenomenon4 - direction
	Star5 - direction
	Star6 - direction
	Planet7 - direction
)
(:init
	(supports instrument0 infrared1)
	(supports instrument0 infrared3)
	(supports instrument0 thermograph0)
	(calibration_target instrument0 GroundStation1)
	(supports instrument1 thermograph0)
	(supports instrument1 spectrograph2)
	(calibration_target instrument1 Star3)
	(on_board instrument0 satellite0)
	(on_board instrument1 satellite0)
	(power_avail satellite0)
	(pointing satellite0 Star2)
	(supports instrument2 infrared1)
	(supports instrument2 thermograph0)
	(supports instrument2 infrared3)
	(calibration_target instrument2 GroundStation1)
	(supports instrument3 thermograph0)
	(calibration_target instrument3 Star2)
	(on_board instrument2 satellite1)
	(on_board instrument3 satellite1)
	(power_avail satellite1)
	(pointing satellite1 Star6)
	(supports instrument4 infrared3)
	(supports instrument4 spectrograph2)
	(calibration_target instrument4 Star3)
	(on_board instrument4 satellite2)
	(power_avail satellite2)
	(pointing satellite2 Star2)
	(supports instrument5 infrared1)
	(supports instrument5 thermograph0)
	(supports instrument5 spectrograph2)
	(calibration_target instrument5 Star2)
	(supports instrument6 infrared3)
	(supports instrument6 spectrograph2)
	(calibration_target instrument6 Star3)
	(supports instrument7 infrared1)
	(calibration_target instrument7 Star2)
	(on_board instrument5 satellite3)
	(on_board instrument6 satellite3)
	(on_board instrument7 satellite3)
	(power_avail satellite3)
	(pointing satellite3 Star6)
)
(:goal (and
	(pointing satellite1 Star3)
	(pointing satellite2 Star2)
	(pointing satellite3 Phenomenon4)
	(have_image Phenomenon4 infrared3)
	(have_image Star5 infrared1)
	(have_image Star6 thermograph0)
	(have_image Planet7 infrared1)
))

)

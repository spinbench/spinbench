(define (problem strips-sat-x-1)
(:domain satellite)
(:objects
	satellite0 - satellite
	instrument0 - instrument
	satellite1 - satellite
	instrument1 - instrument
	instrument2 - instrument
	satellite2 - satellite
	instrument3 - instrument
	satellite3 - satellite
	instrument4 - instrument
	instrument5 - instrument
	satellite4 - satellite
	instrument6 - instrument
	thermograph2 - mode
	infrared1 - mode
	thermograph0 - mode
	Star3 - direction
	Star0 - direction
	Star2 - direction
	Star4 - direction
	GroundStation1 - direction
	Star5 - direction
	Star6 - direction
	Planet7 - direction
	Phenomenon8 - direction
	Star9 - direction
	Star10 - direction
	Phenomenon11 - direction
)
(:init
	(supports instrument0 infrared1)
	(supports instrument0 thermograph2)
	(calibration_target instrument0 Star0)
	(on_board instrument0 satellite0)
	(power_avail satellite0)
	(pointing satellite0 Star10)
	(supports instrument1 thermograph2)
	(supports instrument1 infrared1)
	(calibration_target instrument1 Star0)
	(supports instrument2 thermograph0)
	(supports instrument2 thermograph2)
	(calibration_target instrument2 Star0)
	(on_board instrument1 satellite1)
	(on_board instrument2 satellite1)
	(power_avail satellite1)
	(pointing satellite1 Star3)
	(supports instrument3 thermograph0)
	(calibration_target instrument3 GroundStation1)
	(on_board instrument3 satellite2)
	(power_avail satellite2)
	(pointing satellite2 Planet7)
	(supports instrument4 infrared1)
	(supports instrument4 thermograph0)
	(calibration_target instrument4 Star2)
	(supports instrument5 thermograph2)
	(supports instrument5 infrared1)
	(calibration_target instrument5 Star4)
	(on_board instrument4 satellite3)
	(on_board instrument5 satellite3)
	(power_avail satellite3)
	(pointing satellite3 Star10)
	(supports instrument6 thermograph0)
	(calibration_target instrument6 GroundStation1)
	(on_board instrument6 satellite4)
	(power_avail satellite4)
	(pointing satellite4 GroundStation1)
)
(:goal (and
	(pointing satellite1 Planet7)
	(pointing satellite3 Phenomenon11)
	(pointing satellite4 Star4)
	(have_image Star5 thermograph0)
	(have_image Star6 thermograph0)
	(have_image Planet7 infrared1)
	(have_image Phenomenon8 thermograph0)
	(have_image Star9 thermograph0)
	(have_image Star10 infrared1)
	(have_image Phenomenon11 thermograph2)
))

)

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
	satellite3 - satellite
	instrument5 - instrument
	instrument6 - instrument
	infrared2 - mode
	thermograph0 - mode
	thermograph1 - mode
	GroundStation4 - direction
	Star6 - direction
	GroundStation1 - direction
	Star7 - direction
	Star5 - direction
	GroundStation2 - direction
	GroundStation3 - direction
	Star0 - direction
	Phenomenon8 - direction
	Star9 - direction
	Phenomenon10 - direction
	Star11 - direction
)
(:init
	(supports instrument0 infrared2)
	(supports instrument0 thermograph1)
	(supports instrument0 thermograph0)
	(calibration_target instrument0 GroundStation1)
	(supports instrument1 thermograph1)
	(supports instrument1 thermograph0)
	(supports instrument1 infrared2)
	(calibration_target instrument1 GroundStation2)
	(on_board instrument0 satellite0)
	(on_board instrument1 satellite0)
	(power_avail satellite0)
	(pointing satellite0 GroundStation2)
	(supports instrument2 thermograph0)
	(calibration_target instrument2 Star7)
	(calibration_target instrument2 GroundStation1)
	(on_board instrument2 satellite1)
	(power_avail satellite1)
	(pointing satellite1 GroundStation4)
	(supports instrument3 infrared2)
	(supports instrument3 thermograph0)
	(supports instrument3 thermograph1)
	(calibration_target instrument3 Star0)
	(supports instrument4 thermograph1)
	(supports instrument4 infrared2)
	(calibration_target instrument4 GroundStation2)
	(calibration_target instrument4 Star5)
	(on_board instrument3 satellite2)
	(on_board instrument4 satellite2)
	(power_avail satellite2)
	(pointing satellite2 GroundStation2)
	(supports instrument5 infrared2)
	(calibration_target instrument5 Star0)
	(supports instrument6 thermograph0)
	(supports instrument6 thermograph1)
	(calibration_target instrument6 Star0)
	(calibration_target instrument6 GroundStation3)
	(on_board instrument5 satellite3)
	(on_board instrument6 satellite3)
	(power_avail satellite3)
	(pointing satellite3 GroundStation1)
)
(:goal (and
	(pointing satellite0 GroundStation4)
	(have_image Phenomenon8 thermograph0)
	(have_image Star9 thermograph1)
	(have_image Phenomenon10 infrared2)
	(have_image Star11 infrared2)
))

)

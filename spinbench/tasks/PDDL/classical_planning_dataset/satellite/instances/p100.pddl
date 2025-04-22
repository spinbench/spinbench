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
	satellite3 - satellite
	instrument6 - instrument
	satellite4 - satellite
	instrument7 - instrument
	image0 - mode
	infrared2 - mode
	image3 - mode
	image1 - mode
	Star6 - direction
	Star5 - direction
	GroundStation1 - direction
	Star0 - direction
	GroundStation2 - direction
	GroundStation9 - direction
	Star8 - direction
	GroundStation4 - direction
	GroundStation7 - direction
	GroundStation3 - direction
	Star10 - direction
	Star11 - direction
	Phenomenon12 - direction
	Star13 - direction
	Phenomenon14 - direction
)
(:init
	(supports instrument0 image0)
	(supports instrument0 infrared2)
	(calibration_target instrument0 GroundStation3)
	(calibration_target instrument0 GroundStation4)
	(calibration_target instrument0 Star5)
	(on_board instrument0 satellite0)
	(power_avail satellite0)
	(pointing satellite0 GroundStation1)
	(supports instrument1 infrared2)
	(supports instrument1 image3)
	(supports instrument1 image0)
	(calibration_target instrument1 GroundStation9)
	(calibration_target instrument1 GroundStation1)
	(calibration_target instrument1 GroundStation7)
	(supports instrument2 image3)
	(supports instrument2 image0)
	(supports instrument2 image1)
	(calibration_target instrument2 GroundStation3)
	(calibration_target instrument2 GroundStation2)
	(supports instrument3 image3)
	(supports instrument3 image1)
	(supports instrument3 image0)
	(calibration_target instrument3 Star0)
	(calibration_target instrument3 GroundStation1)
	(on_board instrument1 satellite1)
	(on_board instrument2 satellite1)
	(on_board instrument3 satellite1)
	(power_avail satellite1)
	(pointing satellite1 Phenomenon12)
	(supports instrument4 image3)
	(supports instrument4 image1)
	(supports instrument4 image0)
	(calibration_target instrument4 Star8)
	(calibration_target instrument4 GroundStation9)
	(calibration_target instrument4 GroundStation2)
	(supports instrument5 infrared2)
	(calibration_target instrument5 GroundStation4)
	(on_board instrument4 satellite2)
	(on_board instrument5 satellite2)
	(power_avail satellite2)
	(pointing satellite2 Star11)
	(supports instrument6 image3)
	(calibration_target instrument6 GroundStation7)
	(on_board instrument6 satellite3)
	(power_avail satellite3)
	(pointing satellite3 Star8)
	(supports instrument7 infrared2)
	(supports instrument7 image3)
	(calibration_target instrument7 GroundStation3)
	(on_board instrument7 satellite4)
	(power_avail satellite4)
	(pointing satellite4 GroundStation4)
)
(:goal (and
	(pointing satellite1 Star8)
	(pointing satellite2 Phenomenon12)
	(have_image Star10 image0)
	(have_image Star11 infrared2)
	(have_image Phenomenon12 image3)
	(have_image Star13 image1)
	(have_image Phenomenon14 image0)
))

)

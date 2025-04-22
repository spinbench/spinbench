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
	satellite4 - satellite
	instrument6 - instrument
	instrument7 - instrument
	image0 - mode
	image3 - mode
	infrared1 - mode
	image2 - mode
	GroundStation0 - direction
	Star1 - direction
	Phenomenon2 - direction
	Planet3 - direction
	Phenomenon4 - direction
	Star5 - direction
	Star6 - direction
	Phenomenon7 - direction
	Star8 - direction
	Phenomenon9 - direction
)
(:init
	(supports instrument0 image3)
	(supports instrument0 infrared1)
	(supports instrument0 image0)
	(calibration_target instrument0 Star1)
	(supports instrument1 infrared1)
	(supports instrument1 image3)
	(calibration_target instrument1 GroundStation0)
	(on_board instrument0 satellite0)
	(on_board instrument1 satellite0)
	(power_avail satellite0)
	(pointing satellite0 Star1)
	(supports instrument2 infrared1)
	(supports instrument2 image2)
	(calibration_target instrument2 GroundStation0)
	(on_board instrument2 satellite1)
	(power_avail satellite1)
	(pointing satellite1 Star5)
	(supports instrument3 image2)
	(supports instrument3 infrared1)
	(supports instrument3 image3)
	(calibration_target instrument3 Star1)
	(supports instrument4 infrared1)
	(supports instrument4 image3)
	(supports instrument4 image0)
	(calibration_target instrument4 Star1)
	(on_board instrument3 satellite2)
	(on_board instrument4 satellite2)
	(power_avail satellite2)
	(pointing satellite2 GroundStation0)
	(supports instrument5 image2)
	(supports instrument5 image0)
	(calibration_target instrument5 Star1)
	(on_board instrument5 satellite3)
	(power_avail satellite3)
	(pointing satellite3 Star1)
	(supports instrument6 image2)
	(supports instrument6 image3)
	(calibration_target instrument6 Star1)
	(supports instrument7 infrared1)
	(calibration_target instrument7 Star1)
	(on_board instrument6 satellite4)
	(on_board instrument7 satellite4)
	(power_avail satellite4)
	(pointing satellite4 Star1)
)
(:goal (and
	(pointing satellite0 Star1)
	(pointing satellite3 Planet3)
	(have_image Phenomenon2 image3)
	(have_image Planet3 image3)
	(have_image Phenomenon4 image0)
	(have_image Star5 image3)
	(have_image Star6 image3)
	(have_image Phenomenon7 image3)
	(have_image Star8 image3)
	(have_image Phenomenon9 image3)
))

)

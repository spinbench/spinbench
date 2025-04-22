(define (problem strips-sat-x-1)
(:domain satellite)
(:objects
	satellite0 - satellite
	instrument0 - instrument
	instrument1 - instrument
	satellite1 - satellite
	instrument2 - instrument
	instrument3 - instrument
	instrument4 - instrument
	satellite2 - satellite
	instrument5 - instrument
	instrument6 - instrument
	infrared3 - mode
	infrared2 - mode
	image1 - mode
	spectrograph0 - mode
	Star5 - direction
	Star0 - direction
	GroundStation4 - direction
	Star7 - direction
	GroundStation1 - direction
	GroundStation3 - direction
	Star2 - direction
	Star6 - direction
	Planet8 - direction
	Phenomenon9 - direction
	Star10 - direction
	Planet11 - direction
)
(:init
	(supports instrument0 infrared3)
	(supports instrument0 image1)
	(calibration_target instrument0 Star7)
	(supports instrument1 infrared3)
	(calibration_target instrument1 Star0)
	(calibration_target instrument1 GroundStation4)
	(on_board instrument0 satellite0)
	(on_board instrument1 satellite0)
	(power_avail satellite0)
	(pointing satellite0 Star7)
	(supports instrument2 infrared2)
	(supports instrument2 image1)
	(calibration_target instrument2 GroundStation3)
	(calibration_target instrument2 Star6)
	(supports instrument3 infrared2)
	(calibration_target instrument3 GroundStation4)
	(supports instrument4 image1)
	(supports instrument4 spectrograph0)
	(supports instrument4 infrared3)
	(calibration_target instrument4 GroundStation1)
	(calibration_target instrument4 Star7)
	(on_board instrument2 satellite1)
	(on_board instrument3 satellite1)
	(on_board instrument4 satellite1)
	(power_avail satellite1)
	(pointing satellite1 Star5)
	(supports instrument5 infrared2)
	(supports instrument5 image1)
	(supports instrument5 infrared3)
	(calibration_target instrument5 GroundStation3)
	(calibration_target instrument5 Star6)
	(supports instrument6 infrared3)
	(supports instrument6 infrared2)
	(calibration_target instrument6 Star6)
	(calibration_target instrument6 Star2)
	(on_board instrument5 satellite2)
	(on_board instrument6 satellite2)
	(power_avail satellite2)
	(pointing satellite2 Star10)
)
(:goal (and
	(pointing satellite1 Star10)
	(pointing satellite2 Phenomenon9)
	(have_image Planet8 image1)
	(have_image Phenomenon9 image1)
	(have_image Star10 image1)
	(have_image Planet11 infrared2)
))

)

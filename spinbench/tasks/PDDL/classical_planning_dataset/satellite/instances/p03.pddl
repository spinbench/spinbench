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
	satellite3 - satellite
	instrument7 - instrument
	instrument8 - instrument
	instrument9 - instrument
	image3 - mode
	image2 - mode
	spectrograph0 - mode
	image4 - mode
	infrared1 - mode
	Star0 - direction
	Star5 - direction
	Star8 - direction
	Star3 - direction
	GroundStation2 - direction
	GroundStation1 - direction
	GroundStation4 - direction
	Star6 - direction
	Star7 - direction
	Phenomenon9 - direction
	Star10 - direction
	Phenomenon11 - direction
	Phenomenon12 - direction
)
(:init
	(supports instrument0 spectrograph0)
	(supports instrument0 image4)
	(calibration_target instrument0 Star6)
	(calibration_target instrument0 GroundStation4)
	(calibration_target instrument0 Star7)
	(supports instrument1 spectrograph0)
	(calibration_target instrument1 GroundStation2)
	(calibration_target instrument1 Star3)
	(calibration_target instrument1 Star6)
	(on_board instrument0 satellite0)
	(on_board instrument1 satellite0)
	(power_avail satellite0)
	(pointing satellite0 GroundStation1)
	(supports instrument2 spectrograph0)
	(supports instrument2 infrared1)
	(calibration_target instrument2 Star5)
	(calibration_target instrument2 Star8)
	(supports instrument3 image4)
	(calibration_target instrument3 Star5)
	(supports instrument4 image4)
	(supports instrument4 infrared1)
	(calibration_target instrument4 Star8)
	(calibration_target instrument4 GroundStation2)
	(on_board instrument2 satellite1)
	(on_board instrument3 satellite1)
	(on_board instrument4 satellite1)
	(power_avail satellite1)
	(pointing satellite1 Star7)
	(supports instrument5 infrared1)
	(supports instrument5 image3)
	(calibration_target instrument5 Star3)
	(supports instrument6 infrared1)
	(supports instrument6 image2)
	(supports instrument6 image4)
	(calibration_target instrument6 Star6)
	(calibration_target instrument6 Star3)
	(on_board instrument5 satellite2)
	(on_board instrument6 satellite2)
	(power_avail satellite2)
	(pointing satellite2 Star8)
	(supports instrument7 infrared1)
	(supports instrument7 image3)
	(calibration_target instrument7 GroundStation2)
	(calibration_target instrument7 Star7)
	(supports instrument8 image4)
	(supports instrument8 image3)
	(supports instrument8 infrared1)
	(calibration_target instrument8 GroundStation1)
	(calibration_target instrument8 Star6)
	(supports instrument9 image3)
	(supports instrument9 infrared1)
	(supports instrument9 image2)
	(calibration_target instrument9 Star7)
	(calibration_target instrument9 Star6)
	(calibration_target instrument9 GroundStation4)
	(on_board instrument7 satellite3)
	(on_board instrument8 satellite3)
	(on_board instrument9 satellite3)
	(power_avail satellite3)
	(pointing satellite3 GroundStation4)
)
(:goal (and
	(pointing satellite1 Star7)
	(have_image Phenomenon9 image4)
	(have_image Star10 image4)
	(have_image Phenomenon11 image2)
	(have_image Phenomenon12 infrared1)
))

)

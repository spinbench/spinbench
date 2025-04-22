(define (problem assembly-d3-m3-n1-h80-a20-r3-t3-o40)
   (:domain assembly)
   (:objects r0 - resource
             a-0-0 a-1-0 a-1-1 a-1-2 a-2-0 - assembly)


(:init 
(part-of a-1-0 a-0-0)
(part-of a-1-1 a-0-0)
(part-of a-1-2 a-0-0)
(part-of a-2-0 a-1-0)
(available a-1-1)
(available a-1-2)
(available a-2-0)
(available r0)
)


(:goal (complete a-0-0))
)
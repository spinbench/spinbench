(define (problem assembly-d2-m3-n1-h70-a30-r2-t5-o10)
   (:domain assembly)
   (:objects 
      r0 r1 - resource
      a-0-0 a-1-0 a-1-1 a-2-0 a-2-1 a-2-2 - assembly
   )
   (:init
      (part-of a-1-0 a-0-0)
      (part-of a-1-1 a-0-0)
      (part-of a-2-0 a-1-0)
      (part-of a-2-1 a-1-1)
      (part-of a-2-2 a-1-1)
      (requires a-0-0 r0)
      (requires a-1-0 r1)
      (available r0)
      (available r1)
      (available a-2-0)
      (available a-2-1)
      (available a-2-2)
   )
   (:goal (complete a-0-0))
)

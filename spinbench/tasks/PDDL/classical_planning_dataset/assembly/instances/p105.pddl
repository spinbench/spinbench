(define (problem assembly-d2-m3-n2-h60-a25-r3-t10-o15)
   (:domain assembly)
   (:objects 
      r0 r1 r2 - resource
      a-0-0 a-1-0 a-1-1 a-2-0 a-2-1 a-2-2 - assembly
   )
   (:init
      (part-of a-1-0 a-0-0)
      (part-of a-1-1 a-0-0)
      (part-of a-2-0 a-1-0)
      (part-of a-2-1 a-1-0)
      (part-of a-2-2 a-1-1)
      (requires a-0-0 r0)
      (requires a-1-0 r1)
      (requires a-1-1 r2)
      (available r0)
      (available r1)
      (available r2)
      (available a-2-0)
      (available a-2-1)
      (available a-2-2)
   )
   (:goal (complete a-0-0))
)

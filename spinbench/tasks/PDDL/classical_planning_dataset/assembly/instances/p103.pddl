(define (problem assembly-d3-m2-n2-h50-a20-r3-t15-o20)
   (:domain assembly)
   (:objects 
      r0 r1 r2 - resource
      a-0-0 a-1-0 a-1-1 a-2-0 a-2-1 a-3-0 a-3-1 - assembly
   )
   (:init
      (part-of a-1-0 a-0-0)
      (part-of a-1-1 a-0-0)
      (part-of a-2-0 a-1-0)
      (part-of a-2-1 a-1-1)
      (part-of a-3-0 a-2-0)
      (part-of a-3-1 a-2-1)
      (requires a-0-0 r0)
      (requires a-1-1 r1)
      (requires a-2-1 r2)
      (available r0)
      (available r1)
      (available r2)
      (available a-3-0)
      (available a-3-1)
   )
   (:goal (complete a-0-0))
)

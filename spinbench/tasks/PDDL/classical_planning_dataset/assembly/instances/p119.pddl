(define (problem assembly-d3-m3-h50-n4-r60-t30-a20-o10)
   (:domain assembly)
   (:objects 
      r0 r1 r2 r3 - resource
      a-0-0 a-1-0 a-1-1 a-2-0 a-2-1 a-2-2 - assembly
   )
   (:init
      ;; Assembly hierarchy
      (part-of a-1-0 a-0-0)
      (part-of a-1-1 a-0-0)
      (part-of a-2-0 a-1-0)
      (part-of a-2-1 a-1-0)
      (part-of a-2-2 a-1-1)

      ;; Resource requirements
      (requires a-0-0 r0)
      (requires a-1-0 r1)
      (requires a-1-1 r2)
      (requires a-2-0 r3)

      ;; Resources available
      (available r0)
      (available r1)
      (available r2)
      (available r3)

      ;; Assemblies already available
      (available a-2-0)
      (available a-2-1)
      (available a-2-2)

      ;; Additional ordering constraints
      (order a-2-0 a-1-0)
      (order a-2-1 a-1-0)
   )
   (:goal 
      (and 
         (complete a-0-0)
      )
   )
)

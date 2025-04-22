(define (problem assembly-d5-m5-n4-h100-a35-r5-t20-o3)
   (:domain assembly)
   (:objects 
      r0 r1 r2 r3 r4 r5 - resource
      a-0-0 a-1-0 a-1-1 a-2-0 a-2-1 a-2-2 a-3-0 a-3-1 a-4-0 a-4-1 - assembly
   )
   (:init
      ;; Assembly hierarchy
      (part-of a-1-0 a-0-0)
      (part-of a-1-1 a-0-0)
      (part-of a-2-0 a-1-0)
      (part-of a-2-1 a-1-1)
      (part-of a-2-2 a-1-1)
      (part-of a-3-0 a-2-0)
      (part-of a-3-1 a-2-1)
      (part-of a-4-0 a-3-0)
      (part-of a-4-1 a-3-1)

      ;; Resource requirements
      (requires a-0-0 r0)
      (requires a-1-0 r1)
      (requires a-1-1 r2)
      (requires a-2-0 r3)
      (requires a-3-1 r4)
      (requires a-4-0 r5)

      ;; Resources available
      (available r0)
      (available r1)
      (available r2)
      (available r3)
      (available r4)
      (available r5)

      ;; Assemblies already available
      (available a-4-0)
      (available a-4-1)
   )
   (:goal 
      (and 
         (complete a-0-0)
      )
   )
)

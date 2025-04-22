(define (problem assembly-d4-m3-n3-h50-a12-r3-t5-o4)
   (:domain assembly)
   (:objects 
      r0 r1 r2 - resource
      a-0-0 a-1-0 a-1-1 a-2-0 a-2-1 a-3-0 a-3-1 - assembly
   )
   (:init
      ;; Assembly hierarchy
      (part-of a-1-0 a-0-0)
      (part-of a-1-1 a-0-0)
      (part-of a-2-0 a-1-0)
      (part-of a-2-1 a-1-1)
      (part-of a-3-0 a-2-0)
      (part-of a-3-1 a-2-1)

      ;; Resource requirements
      (requires a-0-0 r0)
      (requires a-1-0 r1)
      (requires a-3-1 r2)

      ;; Resources available
      (available r0)
      (available r1)
      (available r2)

      ;; Assemblies already available
      (available a-3-0)
      (available a-3-1)
   )
   (:goal 
      (and 
         (complete a-0-0)
      )
   )
)

(define (problem assembly-d3-m3-n2-h60-a25-r3-t10-o1)
   (:domain assembly)
   (:objects 
      r0 r1 r2 r3 - resource
      a-0-0 a-1-0 a-1-1 a-2-0 a-2-1 a-3-0 - assembly
   )
   (:init
      ;; Assembly hierarchy
      (part-of a-1-0 a-0-0)
      (part-of a-1-1 a-0-0)
      (part-of a-2-0 a-1-0)
      (part-of a-2-1 a-1-1)
      (part-of a-3-0 a-2-0)

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
      (available a-3-0)
      (available a-2-1)
   )
   (:goal 
      (and 
         (complete a-0-0)
      )
   )
)

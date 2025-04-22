(define (problem assembly-d3-m3-n1-h50-a20-r2-t5-o4)
   (:domain assembly)
   (:objects 
      r0 r1 - resource
      a-0-0 a-1-0 a-1-1 a-2-0 - assembly
   )
   (:init
      ;; Assembly hierarchy
      (part-of a-1-0 a-0-0)
      (part-of a-1-1 a-0-0)
      (part-of a-2-0 a-1-0)

      ;; Resource requirements
      (requires a-0-0 r0)
      (requires a-1-0 r1)

      ;; Resources available
      (available r0)
      (available r1)

      ;; Assemblies already available
      (available a-2-0)
   )
   (:goal 
      (and 
         (complete a-0-0)
      )
   )
)

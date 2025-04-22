(define (problem assembly-d4-m3-h70-n3-r50-t30-a25-o15-s45678)
   (:domain assembly)
   (:objects 
      r0 r1 r2 - resource
      a-0-0 a-1-0 a-1-1 a-2-0 a-2-1 a-2-2 a-3-0 a-3-1 a-3-2 - assembly
   )
   (:init
      ;; Assembly hierarchy
      (part-of a-1-0 a-0-0)
      (part-of a-1-1 a-0-0)
      (part-of a-2-0 a-1-0)
      (part-of a-2-1 a-1-0)
      (part-of a-2-2 a-1-1)
      (part-of a-3-0 a-2-0)
      (part-of a-3-1 a-2-1)
      (part-of a-3-2 a-2-2)

      ;; Resource requirements
      (requires a-0-0 r0)
      (requires a-1-0 r1)
      (requires a-1-1 r2)
      (requires a-2-0 r0)
      (requires a-2-1 r1)
      (requires a-3-0 r2)

      ;; Resources available
      (available r0)
      (available r1)
      (available r2)

      ;; Assemblies already available
      (available a-3-0)
      (available a-3-1)
      (available a-3-2)

      ;; Additional ordering constraints
      (order a-1-0 a-0-0)
      (order a-2-0 a-1-0)
      (order a-2-1 a-1-0)
      (order a-3-0 a-2-0)

      ;; Transient parts
      (transient-part a-3-0 a-2-0)
      (transient-part a-3-1 a-1-0)
      (transient-part a-3-2 a-1-1)

      ;; Remove-order constraints
      (remove-order a-2-0 a-3-0 a-1-0)
      (remove-order a-2-1 a-3-1 a-1-0)
   )
   (:goal 
      (and 
         (complete a-0-0)
      )
   )
)

(define (problem auto-assembly)
   (:domain assembly)

   (:objects r0 r1 - resource a-0-0 a-1-0 a-1-1 a-1-2 a-2-0 a-2-1 a-2-2 a-3-0 - assembly)

   (:init
      (part-of a-1-0 a-0-0)
      (part-of a-1-1 a-0-0)
      (part-of a-1-2 a-0-0)
      (part-of a-2-0 a-1-0)
      (part-of a-2-1 a-1-1)
      (part-of a-2-2 a-1-2)
      (transient-part a-2-0 a-1-2)
      (transient-part a-2-2 a-1-1)
      (transient-part a-3-0 a-1-0)
      (transient-part a-3-0 a-1-2)
      (transient-part a-3-0 a-2-0)
      (available r0)
      (available r1)
      (available a-0-0)
      (available a-1-0)
      (available a-1-1)
      (available a-1-2)
      (available a-2-0)
      (available a-2-1)
      (available a-2-2)
      (available a-3-0)
      (requires a-1-1 r0)
      (assemble-order a-1-2 a-1-1 a-0-0)
   )

   (:goal (complete a-0-0))
)

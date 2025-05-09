(define (problem termes-sx4-sy4-h5-nti3-ntg2-sdi1-sdg11)
(:domain termes)
; Generated instance: termes-sx4-sy4-h5-nti3-ntg2-sdi1-sdg11
(:objects
  n0 - numb
  n1 - numb
  n2 - numb
  n3 - numb
  n4 - numb
  n5 - numb
  pos-0-0 - position
  pos-0-1 - position
  pos-0-2 - position
  pos-0-3 - position
  pos-1-0 - position
  pos-1-1 - position
  pos-1-2 - position
  pos-1-3 - position
  pos-2-0 - position
  pos-2-1 - position
  pos-2-2 - position
  pos-2-3 - position
  pos-3-0 - position
  pos-3-1 - position
  pos-3-2 - position
  pos-3-3 - position
)
(:init
  (height pos-0-0 n0)
  (height pos-1-0 n0)
  (height pos-2-0 n0)
  (height pos-3-0 n0)
  (height pos-0-1 n0)
  (height pos-1-1 n0)
  (height pos-2-1 n0)
  (height pos-3-1 n2)
  (height pos-0-2 n0)
  (height pos-1-2 n0)
  (height pos-2-2 n0)
  (height pos-3-2 n0)
  (height pos-0-3 n5)
  (height pos-1-3 n4)
  (height pos-2-3 n0)
  (height pos-3-3 n0)
  (SUCC n1 n0)
  (SUCC n2 n1)
  (SUCC n3 n2)
  (SUCC n4 n3)
  (SUCC n5 n4)
  (NEIGHBOR pos-0-0 pos-1-0)
  (NEIGHBOR pos-0-0 pos-0-1)
  (NEIGHBOR pos-0-1 pos-1-1)
  (NEIGHBOR pos-0-1 pos-0-0)
  (NEIGHBOR pos-0-1 pos-0-2)
  (NEIGHBOR pos-0-2 pos-1-2)
  (NEIGHBOR pos-0-2 pos-0-1)
  (NEIGHBOR pos-0-2 pos-0-3)
  (NEIGHBOR pos-0-3 pos-1-3)
  (NEIGHBOR pos-0-3 pos-0-2)
  (NEIGHBOR pos-1-0 pos-0-0)
  (NEIGHBOR pos-1-0 pos-2-0)
  (NEIGHBOR pos-1-0 pos-1-1)
  (NEIGHBOR pos-1-1 pos-0-1)
  (NEIGHBOR pos-1-1 pos-2-1)
  (NEIGHBOR pos-1-1 pos-1-0)
  (NEIGHBOR pos-1-1 pos-1-2)
  (NEIGHBOR pos-1-2 pos-0-2)
  (NEIGHBOR pos-1-2 pos-2-2)
  (NEIGHBOR pos-1-2 pos-1-1)
  (NEIGHBOR pos-1-2 pos-1-3)
  (NEIGHBOR pos-1-3 pos-0-3)
  (NEIGHBOR pos-1-3 pos-2-3)
  (NEIGHBOR pos-1-3 pos-1-2)
  (NEIGHBOR pos-2-0 pos-1-0)
  (NEIGHBOR pos-2-0 pos-3-0)
  (NEIGHBOR pos-2-0 pos-2-1)
  (NEIGHBOR pos-2-1 pos-1-1)
  (NEIGHBOR pos-2-1 pos-3-1)
  (NEIGHBOR pos-2-1 pos-2-0)
  (NEIGHBOR pos-2-1 pos-2-2)
  (NEIGHBOR pos-2-2 pos-1-2)
  (NEIGHBOR pos-2-2 pos-3-2)
  (NEIGHBOR pos-2-2 pos-2-1)
  (NEIGHBOR pos-2-2 pos-2-3)
  (NEIGHBOR pos-2-3 pos-1-3)
  (NEIGHBOR pos-2-3 pos-3-3)
  (NEIGHBOR pos-2-3 pos-2-2)
  (NEIGHBOR pos-3-0 pos-2-0)
  (NEIGHBOR pos-3-0 pos-3-1)
  (NEIGHBOR pos-3-1 pos-2-1)
  (NEIGHBOR pos-3-1 pos-3-0)
  (NEIGHBOR pos-3-1 pos-3-2)
  (NEIGHBOR pos-3-2 pos-2-2)
  (NEIGHBOR pos-3-2 pos-3-1)
  (NEIGHBOR pos-3-2 pos-3-3)
  (NEIGHBOR pos-3-3 pos-2-3)
  (NEIGHBOR pos-3-3 pos-3-2)
  (IS-DEPOT pos-2-2)
  (at pos-2-2)
)
(:goal (and
  (height pos-0-0 n0)
  (height pos-1-0 n0)
  (height pos-2-0 n5)
  (height pos-3-0 n0)
  (height pos-0-1 n0)
  (height pos-1-1 n0)
  (height pos-2-1 n0)
  (height pos-3-1 n0)
  (height pos-0-2 n0)
  (height pos-1-2 n0)
  (height pos-2-2 n0)
  (height pos-3-2 n0)
  (height pos-0-3 n2)
  (height pos-1-3 n0)
  (height pos-2-3 n0)
  (height pos-3-3 n0)
  (not (has-block))
))
)
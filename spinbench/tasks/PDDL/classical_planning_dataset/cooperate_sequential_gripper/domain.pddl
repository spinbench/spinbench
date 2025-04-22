(define (domain cooperate_sequential_gripper)
  (:requirements :strips :typing :negative-preconditions)

  ;; -----------------------------
  ;; 1) Types
  ;; -----------------------------
  (:types
    room
    robot
    object
    gripper - robot
  )

  ;; -----------------------------
  ;; 2) Predicates
  ;; -----------------------------
  (:predicates
    ;; Robot in a room
    (at-robby ?r - gripper ?x - room)

    ;; Object in a room
    (at ?o - object ?x - room)

    ;; Robot’s "virtual gripper" is free
    (free ?r - gripper)

    ;; Robot carrying object
    (carry ?r - gripper ?o - object)

    ;; Whether object is activated
    (activated ?o - object)

    ;; Robot can activate object
    (can-activate ?r - gripper ?o - object)

    ;; Robot can handle object
    (can-handle ?r - gripper ?o - object)

    ;; Single occupant indicator
    (room-occupied ?x - room)
  )

  ;; -----------------------------
  ;; 3) Actions
  ;; -----------------------------

  ;; Single-occupant move
  (:action move
    :parameters (?r - gripper ?from ?to - room)
    :precondition (and
      (at-robby ?r ?from)
      (room-occupied ?from)
      (not (room-occupied ?to)))
    :effect (and
      (at-robby ?r ?to)
      (room-occupied ?to)
      (not (at-robby ?r ?from))
      (not (room-occupied ?from)))
  )

  ;; Robot activates object
  (:action activate
    :parameters (?r - gripper ?o - object ?room - room)
    :precondition (and
      (can-activate ?r ?o)
      (at-robby ?r ?room)
      (at ?o ?room)
      (not (activated ?o)))
    :effect (and
      (activated ?o))
  )

  ;; Robot picks up object (must be activated, robot is free)
  (:action pick
    :parameters (?r - gripper ?o - object ?room - room)
    :precondition (and
      (can-handle ?r ?o)
      (activated ?o)
      (at-robby ?r ?room)
      (at ?o ?room)
      (free ?r))
    :effect (and
      (carry ?r ?o)
      (not (at ?o ?room))
      (not (free ?r)))
  )

  ;; Robot drops object
  (:action drop
    :parameters (?r - gripper ?o - object ?room - room)
    :precondition (and
      (carry ?r ?o)
      (at-robby ?r ?room))
    :effect (and
      (at ?o ?room)
      (free ?r)
      (not (carry ?r ?o)))
  )
)
  


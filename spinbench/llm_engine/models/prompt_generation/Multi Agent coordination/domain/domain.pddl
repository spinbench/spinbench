(define (domain domain)
  (:requirements :strips :typing)
  (:types room object robot gripper)

  (:predicates
    (at-robby ?r - robot ?x - room)
    (at ?o - object ?x - room)
    (free ?r - robot ?g - gripper)
    (carry ?r - robot ?o - object ?g - gripper)
    (carrying-collaboratively ?o - object)
    (needs-collaboration ?o - object)
    (robot-ready ?r - robot)
  )

  ;; Movement of robots between rooms
  (:action move
    :parameters (?r - robot ?from ?to - room)
    :precondition (and (at-robby ?r ?from))
    :effect (and (at-robby ?r ?to)
                 (not (at-robby ?r ?from)))
  )

  ;; Picking up objects individually
  (:action pick
    :parameters (?r - robot ?obj - object ?room - room ?g - gripper)
    :precondition (and (at ?obj ?room) (at-robby ?r ?room) (free ?r ?g) (not (needs-collaboration ?obj)))
    :effect (and (carry ?r ?obj ?g)
                 (not (at ?obj ?room))
                 (not (free ?r ?g)))
  )

  ;; Picking up objects collaboratively
  (:action pick-collaborative
    :parameters (?r1 ?r2 - robot ?obj - object ?room - room)
    :precondition (and (needs-collaboration ?obj)
                       (at-robby ?r1 ?room)
                       (at-robby ?r2 ?room)
                       (robot-ready ?r1)
                       (robot-ready ?r2))
    :effect (and (carrying-collaboratively ?obj)
                 (not (at ?obj ?room))
                 (not (robot-ready ?r1))
                 (not (robot-ready ?r2)))
  )

  ;; Dropping objects individually
  (:action drop
    :parameters (?r - robot ?obj - object ?room - room ?g - gripper)
    :precondition (and (carry ?r ?obj ?g) (at-robby ?r ?room))
    :effect (and (at ?obj ?room)
                 (free ?r ?g)
                 (not (carry ?r ?obj ?g)))
  )

  ;; Dropping objects collaboratively
  (:action drop-collaborative
    :parameters (?r1 ?r2 - robot ?obj - object ?room - room)
    :precondition (and (carrying-collaboratively ?obj)
                       (at-robby ?r1 ?room)
                       (at-robby ?r2 ?room))
    :effect (and (at ?obj ?room)
                 (robot-ready ?r1)
                 (robot-ready ?r2)
                 (not (carrying-collaboratively ?obj)))
  )
)

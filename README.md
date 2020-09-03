# constraints_problem_using_AI
A fuzzy scheduling problem in this scenario is specified by ignoring orders and giving a number
of tasks, each with a fixed duration in hours. Each task must start and finish on the same day,
within working hours (9am to 5pm). In addition, there can be constraints both on single tasks
and between two tasks. One type of constraint is that a task can have a deadline, which can be
“hard” (the deadline must be met in any valid schedule) or “soft” (the task may be finished late
– though still at or before 5pm – but with a “cost” per hour for missing the deadline). The aim
is to develop an overall schedule for all the tasks (in a single week) that minimizes the total cost
of all the tasks that finish late, provided that all the hard constraints on tasks are satisfied.

### OPTIMIZATION IDEA:

In ```Crossover_Fusion``` instead of having ```Next_Generation```, update ```_Generation``` **directly**, since we already have ```Processed_Indices```.

---

### OPTIMIZATION IDEA:

Make a way to copy the original *Level* without having to load the JSON every single time (probably another variable like ```Original_Data``` would work).

---

### IMPROVEMENT:

In ```Crossover_Fusion```, make a way to maximize the amount of *Individual*s that get paired for sharing a *State* (as it's not optimal now, for example: ```I1``` and ```I2``` may share *State*s, but ```I1``` could also share *State*s with ```I3```, ```I4``` and ```I6```, and ```I2``` could also share *State*s with ```I5```, so in this case, there's at least 1 pair of *State* sharing *Individual*s lost, which would in turn increase the amount of *Bi-BFS* needed to be done).

---

Maybe make *Level*, *Room* and *Explorer* ```dataclasses```? (also, check ```NamedTuple```, maybe some things would be better being that).

---

Comment all ```dataclasses``` and ```enums```.

---

Add *Fitness* function that scores each *Individual* by "Good Practices" (define what that means).

---

Explore Novelty-based *Fitness* functions.

---

Explore Policy-learning.

---

Explore Reinforcement learning.

---

Try my own Original Algorithm.
### OPTIMIZATION IDEA:

In ```Crossover_Fusion``` instead of having ```Next_Generation```, update ```_Generation``` **directly**, since we already have ```Processed_Indices```.

---

### OPTIMIZATION IDEA:

Make a way to copy the original *Level* without having to load the JSON every single time (probably another variable like ```Original_Data``` would work).

---

### IMPROVEMENT:

In ```Crossover_Fusion```, make a way to maximize the amount of *Individual*s that get paired for sharing a *State* (as it's not optimal now, for example: ```I1``` and ```I2``` may share *State*s, but ```I1``` could also share *State*s with ```I3```, ```I4``` and ```I6```, and ```I2``` could also share *State*s with ```I5```, so in this case, there's at least 1 pair of *State* sharing *Individual*s lost, which would in turn increase the amount of *Bi-BFS* needed to be done).

---

Maybe make *Level*, *Room* and *Explorer* ```dataclasse```s? (also, check ```NamedTuple```, maybe some things would be better being that).

---

Comment all ```dataclasse```s and ```enum```s.

---

Add *Fitness* function that scores each *Individual* by "Good Practices" (define what that means).

---

Explore Novelty-based *Fitness* functions.

---

Explore Policy-learning.

---

Explore Reinforcement learning.

---

Fix issue in *Crossover* with ```Crossover_Fusion_Cut_And_Generation``` where it could get the **entire** *Generation* stuck, with each one making *Loop*s.

---

Try my own Original Algorithms.

---

Implement multi-threading.

---

Update all *Functions* that create Log files to include a ```_Delete_Files``` *Parameter* using ```os.remove()```.

---

In ```SensitivityAnalysis.py```, update ```Reference_Attempts__Amount``` to calculate the amount of *File*s in the *Folder* dynamically instead of hard-coding it.

---

Re-run all Reference attempts (to now include the line with the Action history length).

---

Switch to C++.

---

Clean ```ProcessSensitivityAnalysis.py```.

---

Fix in ```Utility.Get__Averaged_Sensitivity_Stats``` the division should be by ```_Attempts```, but instead by only the successful attempts, which would be ```Output.Total_Attempts - Output.Failed_Attempts``` once all the attempts have been checked (which means that this calculation should be refactored to happen outside of the ```for``` loop).
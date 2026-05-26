from time import time


from Game import Game, Action_Type
from Algorithms.BruteForce import Backtracking, BFS
from Algorithms.GeneticAlgorithm import Individual, Generation_Creation_Parameters, Fitness_Gameplay_Parameters, Crossover_Fusion_Parameters, Mutate_Random_Ending_Parameters, Mutate_Cut_And_Generation_Parameters, Create_Generation, Evaluate_Fitness, Select_Parents, Perform_Crossover, Apply_Mutation



# Runs the Backtracking Algorithm and Logs the results
def Execute__Backtracking(_Levels: list[int], _Backtracking_Max_Depth: list[int]):
	"""
	Runs the Backtracking Algorithm (BFS) and Logs the results in a separate File for each Level, containing:

	- Iteration count
	- Elapsed time
	- Action history if beated the Level

	For each depth explored.
	"""


	for _Level in _Levels:
		print(f"Level {_Level}")


		File = open(f"Logs/Backtracking/Level {_Level} Benchmark.txt", "w")
		File.close()


		for _Max_Depth in range(1, _Backtracking_Max_Depth[_Level - 1] + 1):
			G = Game(_Level)
			Success, Actions, Iterations, Elapsed_Time = Backtracking(G, _Max_Depth)
		

			with open(f"Logs/Backtracking/Level {_Level} Benchmark.txt", "a") as File:
				File.write(f"Solution{" " if Success else " not "}found to Level {_Level} with Max Depth {_Max_Depth}, final iteration count: {Iterations:,}. Final time: {Elapsed_Time:.3f} seconds, or {(Elapsed_Time / 60):.3f} minutes, or {(Elapsed_Time / 3600):.3f} hours.\n")


				if Success:
					File.write("Actions:\n")


					for _Action in Actions[:: -1]:
						G.Undo_Action(_Action)
					
					for _Action in Actions:
						File.write(f"{f"Slide Room in {_Action.Instance_Position}" if _Action.Type == Action_Type.Room__Slide else f"Move Explorer in {_Action.Instance_Position}"} {_Action.Direction.Direction_Name()}\n")


						G.Execute_Action(_Action)


					if G.Has__Won():
						File.write(f"Action history verified.\n{"\n" if _Max_Depth < _Backtracking_Max_Depth[_Level - 1] else ""}")


			# for _Action in Actions:
			# 	print(f"{_Action}\n")



# Runs the BFS Algorithm Benchmark and Logs the results
def Execute__BFS_Benchmark(_Levels: list[int]):
	"""
	Runs the BFS Algorithm Benchmark and Logs the results in a separate File for each Level, containing:

	- Iteration count
	- Unique States visited
	- Elapsed time
	- Least amount of Actions required to beat the Level
	- Action history with a single possibility of the least amount of Actions required to beat the Level
	"""


	File = open("Logs/BFS/Benchmark.txt", "w")
	File.close()


	for _Level in _Levels:
		G = Game(_Level)


		print(f"Level {_Level}")


		Actions, Iterations, Unique_States_Count, Elapsed_Time = BFS(G)


		with open("Logs/BFS/Benchmark.txt", "a") as File:
			File.write(f"Solution found to Level {_Level} with length {len(Actions)}, final iteration count: {Iterations:,}, unique states visited: {Unique_States_Count:,}. Final time: {Elapsed_Time:.3f} seconds, or {(Elapsed_Time / 60):.3f} minutes, or {(Elapsed_Time / 3600):.3f} hours.\nActions:\n")


			for _Action in Actions[:: -1]:
				G.Undo_Action(_Action)

			for _Action in Actions:
				File.write(f"{f"Slide Room in {_Action.Instance_Position}" if _Action.Type == Action_Type.Room__Slide else f"Move Explorer in {_Action.Instance_Position}"} {_Action.Direction.Direction_Name()}\n")


				G.Execute_Action(_Action)


			if G.Has__Won():
				File.write(f"Action history verified.\n{"\n" if _Level < _Levels[-1] else ""}")


		# for _Action in Actions:
		# 	print(f"{_Action}\n")

# Runs the BFS Algorithm to find the amount of unique States up to each depth and Logs the results
def Execute__BFS_Search_Space(_Levels: list[int], _BFS_Search_Max_Depth: list[int]):
	"""
	Runs the BFS Algorithm to find the amount of unique States up to each depth and Logs the results in a separate File for each Level.
	"""


	for _Level in _Levels:
		print(f"Level {_Level}")


		File = open(f"Logs/BFS/Level {_Level} Search Space.txt", "w")
		File.close()


		for _Max_Depth in range(1, _BFS_Search_Max_Depth[_Level - 1] + 1):
			G = Game(_Level)
			_, Iterations, Unique_States_Count, Elapsed_Time = BFS(G, _Max_Depth = _Max_Depth)


			with open(f"Logs/BFS/Level {_Level} Search Space.txt", "a") as File:
				File.write(f"Search space with depth of {_Max_Depth} Actions complete, final iteration count: {Iterations:,}, unique states visited: {Unique_States_Count:,}. Final time: {Elapsed_Time:.3f} seconds, or {(Elapsed_Time / 60):.3f} minutes, or {(Elapsed_Time / 3600):.3f} hours.\n")



# Runs the Genetic Algorithm with the given Parameters to try to solve the given Levels, and Logs the results
def Execute__Genetic_Algorithm(_Levels: list[int], _Filename_Prefix: str, _Attempt: int, _Max__Generations: int, _Stop_At__Beating_Level: bool, _Generation_Parameters: Generation_Creation_Parameters, _Fitness_Parameters: Fitness_Gameplay_Parameters, _Crossover_Parameters: Crossover_Fusion_Parameters, _Mutation_Parameters: Mutate_Random_Ending_Parameters | Mutate_Cut_And_Generation_Parameters):
	"""
	Runs the Genetic Algorithm with the given Generation, Fitness, Crossover and Mutation Parameters to try to solve the given Levels, and Logs the results in a separate File for each Level, containing:

	- Elapsed time for each Phase of each Generation
	- Description and Action history of Fittest Individual of each Generation
	"""


	for _Level in _Levels:
		print(f"Level {_Level}")


		with open(f"Logs/Genetic Algorithm/Level {_Level}/{_Filename_Prefix} - Attempt {_Attempt}.txt", "w") as File:
			Initial_Time: float = time()


			Generation: list[Individual] = Create_Generation(_Generation_Parameters, _Level)
			Elapsed_Time: float = time() - Initial_Time


			# print(f"Created first generation. Total time: {Elapsed_Time:.3f} seconds, or {(Elapsed_Time / 60):.3f} minutes, or {(Elapsed_Time / 3600):.3f} hours.\n")
			File.write(f"Created first generation. Total time: {Elapsed_Time:.3f} seconds, or {(Elapsed_Time / 60):.3f} minutes, or {(Elapsed_Time / 3600):.3f} hours.\n\n")


			for _Generation__Number in range(_Max__Generations):
				print(f"\nGeneration {_Generation__Number + 1}\n")
				File.write(f"Generation {_Generation__Number + 1}\n\n")


				for _Individual in Generation:
					Evaluate_Fitness(_Individual, _Fitness_Parameters, _Level)


				Fittest_Individual: Individual = None
				Fittest_Individual_Game: Game = Game(_Level)


				for _Individual in Generation:
					if not Fittest_Individual or _Individual.Fitness.Score > Fittest_Individual.Fitness.Score:
						Fittest_Individual = _Individual


				Elapsed_Time = time() - Initial_Time


				print(f"Evaluated Fitness of Generation {_Generation__Number + 1}. Total time: {Elapsed_Time:.3f} seconds, or {(Elapsed_Time / 60):.3f} minutes, or {(Elapsed_Time / 3600):.3f} hours.\nDescription of fittest Individual:\n- Fitness: {Fittest_Individual.Fitness.Score}\n- Did it beat the Level: {"Yes" if Fittest_Individual.Fitness.Description.Has__Won else "No"}\n- Did it loop: {"Yes" if Fittest_Individual.Fitness.Description.Has__Looped else "No"}\n- Keys obtained: {Fittest_Individual.Fitness.Description.Obtained__Keys}\n- Keys used: {Fittest_Individual.Fitness.Description.Used__Keys}")
				# print("\nActions:\n")
				File.write(f"Evaluated Fitness of Generation {_Generation__Number + 1}. Total time: {Elapsed_Time:.3f} seconds, or {(Elapsed_Time / 60):.3f} minutes, or {(Elapsed_Time / 3600):.3f} hours.\nDescription of fittest Individual:\n- Fitness: {Fittest_Individual.Fitness.Score}\n- Did it beat the Level: {"Yes" if Fittest_Individual.Fitness.Description.Has__Won else "No"}\n- Did it loop: {"Yes" if Fittest_Individual.Fitness.Description.Has__Looped else "No"}\n- Keys obtained: {Fittest_Individual.Fitness.Description.Obtained__Keys}\n- Keys used: {Fittest_Individual.Fitness.Description.Used__Keys}\n\nActions:\n")


				for _Action__Index, _Action in enumerate(Fittest_Individual.Action_History):
					Fittest_Individual_Game.Execute_Action(_Action)


					# print(f"{_Action__Index}: {f"Slide Room in ({_Action.Instance_Position.x}, {_Action.Instance_Position.y})" if _Action.Type == Action_Type.Room__Slide else f"Move Explorer in ({_Action.Instance_Position.x}, {_Action.Instance_Position.y})"} {_Action.Direction.Direction_Name()}")
					File.write(f"{_Action__Index + 1}: {f"Slide Room in ({_Action.Instance_Position.x}, {_Action.Instance_Position.y})" if _Action.Type == Action_Type.Room__Slide else f"Move Explorer in ({_Action.Instance_Position.x}, {_Action.Instance_Position.y})"} {_Action.Direction.Direction_Name()}{" (Winning Action)" if Fittest_Individual_Game.Has__Won() else ""}\n")


				if _Stop_At__Beating_Level and Fittest_Individual.Fitness.Description.Has__Won:
					break


				Parents: list[Individual] = Select_Parents(Generation)
				Elapsed_Time = time() - Initial_Time


				# print(f"\nSelected parents of the next Generation. Total time: {Elapsed_Time:.3f} seconds, or {(Elapsed_Time / 60):.3f} minutes, or {(Elapsed_Time / 3600):.3f} hours.\n")
				File.write(f"\nSelected parents of the next Generation. Total time: {Elapsed_Time:.3f} seconds, or {(Elapsed_Time / 60):.3f} minutes, or {(Elapsed_Time / 3600):.3f} hours.\n\n")


				Generation = Perform_Crossover(Parents, _Crossover_Parameters, _Level)
				Elapsed_Time = time() - Initial_Time


				# print(f"Performed Crossing over of the parents, next Generation created. Total time: {Elapsed_Time:.3f} seconds, or {(Elapsed_Time / 60):.3f} minutes, or {(Elapsed_Time / 3600):.3f} hours.\n")
				File.write(f"Performed Crossing over of the parents, next Generation created. Total time: {Elapsed_Time:.3f} seconds, or {(Elapsed_Time / 60):.3f} minutes, or {(Elapsed_Time / 3600):.3f} hours.\n\n")


				for _Individual in Generation:
					Apply_Mutation(_Individual, _Level, _Mutation_Parameters)
				
				
				Elapsed_Time = time() - Initial_Time


				# print(f"Applied Mutations to the next Generation. Total time: {Elapsed_Time:.3f} seconds, or {(Elapsed_Time / 60):.3f} minutes, or {(Elapsed_Time / 3600):.3f} hours.")
				File.write(f"Applied Mutations to the next Generation. Total time: {Elapsed_Time:.3f} seconds, or {(Elapsed_Time / 60):.3f} minutes, or {(Elapsed_Time / 3600):.3f} hours.\n{"\n" if _Generation__Number < _Max__Generations - 1 else ""}")
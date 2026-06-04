from ExecuteAlgorithms import Execute__Backtracking, Execute__BFS_Benchmark, Execute__BFS_Search_Space, Execute__Genetic_Algorithm

from Algorithms.GeneticAlgorithm import Generation_Creation_Parameters, Fitness_Gameplay_Parameters, Crossover_Fusion_Parameters, Crossover_Fusion_Bi_BFS_Fallback_Parameters, Crossover_Fusion_Cut_And_Generation_Fallback_Parameters, Crossover_Fusion_Regeneration_Fallback_Parameters, Crossover_Fusion_Clone_Fallback_Parameters, Mutate_Random_Ending_Parameters, Mutate_Cut_And_Generation_Parameters


# Levels to run the Algorithms in
Levels: list[int] = [
	4
]



# Backtracking
# Max depth for the DFS to explore in each Level
Max_Depth = [
	10, 10, 20, 25, 50, 35, 50, 100
]



# Genetic Algorithm
Max__Generations: int = 100

Stop_At__Beating_Level: bool = True
Require__Beating_Level: bool = False
Require__No_Loop_Fittest_Individual: bool = False


# Parameters for the Creation of the first Generation
Generation_Parameters: Generation_Creation_Parameters = Generation_Creation_Parameters(
	Generation__Size = 100,
	Actions__Amount = 10
)

# Parameters for the Fitness function, to change Version, replace the current Version (Gameplay) and the necessary Parameters
Fitness_Parameters: Fitness_Gameplay_Parameters = Fitness_Gameplay_Parameters(
	Length__Weight = 10.0,
	Obtained_Keys__Bonus = 500.0,
	Used_Keys__Bonus = 1000.0,
	Has__Won__Bonus = 1000000.0,
	Has__Looped__Penalty = -1000000.0
)

# Parameters for the Crossover step, to change Version, replace the current Version (Fusion) and the necessary Parameters
# To change Fallback when no shared State is found, replace the current Version (Cut_And_Generation) and the necessary Parameters
Crossover_Parameters: Crossover_Fusion_Parameters = Crossover_Fusion_Parameters(
	Search_Start_Percent = 0.2,
	Search_End_Percent = 1.0,

	Fallback_Parameters = Crossover_Fusion_Bi_BFS_Fallback_Parameters(
		Max__Depth = 12
	)
	# Fallback_Parameters = Crossover_Fusion_Cut_And_Generation_Fallback_Parameters(
	# 	Cut_And_Generation_Parameters = Mutate_Cut_And_Generation_Parameters(
	# 		Random_Cut_Start_Percent = 0.3
	# 	)
	# )
	# Fallback_Parameters = Crossover_Fusion_Regeneration_Fallback_Parameters(
	# 	Nominal_Generation_Parameters
	# )
	# Fallback_Parameters = Crossover_Fusion_Cut_And_Generation_Fallback_Parameters(
	# 	Cut_And_Generation_Parameters = Mutate_Cut_And_Generation_Parameters(
	# 		Random_Cut_Start_Percent = 0.3
	# 	)
	# )
	# Fallback_Parameters = Crossover_Fusion_Cut_And_Generation_Fallback_Parameters(
	# 	Mutate_Cut_And_Generation_Parameters(
	# 		Last_Actions_To_Change = 10
	# 	)
	# )
	# Fallback_Parameters = Crossover_Fusion_Clone_Fallback_Parameters()
)

# Parameters for the Mutation step, to change Version, replace the current Version (Random_Ending) and the necessary Parameters
Mutation_Parameters: Mutate_Random_Ending_Parameters = Mutate_Random_Ending_Parameters(
	New_Actions__Amount = 5
)


File__Name_Prefix: str = f"Crossover with {"Bi-BFS" if isinstance(Crossover_Parameters.Fallback_Parameters, Crossover_Fusion_Bi_BFS_Fallback_Parameters) else "Cut and Generation"}"
Attempt: int = 5








# Brute-force
# DFS
# Execute__Backtracking(Levels, Max_Depth)


# BFS
# Execute__BFS_Benchmark(Levels)

# Execute__BFS_Search_Space(Levels)



# Genetic Algorithm
Execute__Genetic_Algorithm(Levels, File__Name_Prefix, Attempt, Max__Generations, Stop_At__Beating_Level, Require__Beating_Level, Require__No_Loop_Fittest_Individual, Generation_Parameters, Fitness_Parameters, Crossover_Parameters, Mutation_Parameters)
# Execute__Genetic_Algorithm(Levels, "Sensitivity Analysis/Temporary File", Attempt, Max__Generations, Stop_At__Beating_Level, Generation_Parameters, Fitness_Parameters, Crossover_Parameters, Mutation_Parameters)
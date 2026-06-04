from os import remove
from copy import deepcopy

from dataclasses import dataclass


from ExecuteAlgorithms import Execute__Genetic_Algorithm

from Algorithms.GeneticAlgorithm import Generation_Creation_Parameters, Fitness_Gameplay_Parameters, Crossover_Fusion_Parameters, Crossover_Fusion_Bi_BFS_Fallback_Parameters, Crossover_Fusion_Cut_And_Generation_Fallback_Parameters, Crossover_Fusion_Regeneration_Fallback_Parameters, Crossover_Fusion_Clone_Fallback_Parameters, Mutate_Random_Ending_Parameters, Mutate_Cut_And_Generation_Parameters


@dataclass
class Sensitivity_Stats:
	Average_Action_History__Length: float = 0.0
	Average_Elapsed_Time: float = 0.0

	Failed_Attempts: int = 0
	Total_Attempts: int = 0


	# Returns a string representing itself
	def __str__(self) -> str:
		return f"Average Action history length: {self.Average_Action_History__Length} actions\nAverage elapsed time: {self.Average_Elapsed_Time} seconds\n{f"No failed attempts out of {self.Total_Attempts} total." if self.Failed_Attempts == 0 else f"Failed {self.Failed_Attempts}/{self.Total_Attempts} attempts."}"



# Gets the averages of the Action history length and elapsed time of the given attempts with the given File name prefix at the Logs directory of the given Level.
def Get__Averaged_Sensitivity_Stats(_Level: int, _File__Name_Prefix: str, _Attempts: int, _Delete_Files: bool = False) -> Sensitivity_Stats:
	"""
	Calculates and returns the averages of the Action history length and elapsed time of the given attempts with the given File name prefix at the Logs directory of the given Level.
	"""


	Output: Sensitivity_Stats = Sensitivity_Stats(Total_Attempts = _Attempts)


	for _Attempt in range(_Attempts):
		File = open(f"Logs/Genetic Algorithm/Level {_Level}/{_File__Name_Prefix} - Attempt {_Attempt + 1}.txt", "r")
		Lines: list[str] = File.readlines()[:: -1]


		if "- Did it beat the Level: Yes\n" not in Lines:
			if _Delete_Files:
				File.close()
				remove(f"Logs/Genetic Algorithm/Level {_Level}/{_File__Name_Prefix} - Attempt {_Attempt + 1}.txt")


			Output.Failed_Attempts += 1


			continue


		Pivot_Line__Index: int = Lines.index("- Did it beat the Level: Yes\n")

		Action_History__Length_Start__Index: int = Lines[Pivot_Line__Index + 1].find(": ") + 2
		Action_History__Length: int = int(Lines[Pivot_Line__Index + 1][Action_History__Length_Start__Index :])
		Elapsed_Time_Start__Index: int = Lines[Pivot_Line__Index + 4].find(": ") + 2
		Elapsed_Time_End__Index: int = Lines[Pivot_Line__Index + 4].find(" seconds")
		Elapsed_Time: float = float(Lines[Pivot_Line__Index + 4][Elapsed_Time_Start__Index : Elapsed_Time_End__Index])


		Output.Average_Action_History__Length += Action_History__Length / _Attempts
		Output.Average_Elapsed_Time += Elapsed_Time / _Attempts


		File.close()


		if _Delete_Files:
			remove(f"Logs/Genetic Algorithm/Level {_Level}/{_File__Name_Prefix} - Attempt {_Attempt + 1}.txt")
	

	return Output


# Generates Temporary Files for each attempt of the Genetic Algorithm to calculate the averaged Sensitivity stats, and Logs them in Output.txt, inside the Sensitivity Analysis Folder of the given Level
def Generate__Sensitivity_Stats(_Level: int, _Parameter: Generation_Creation_Parameters | Fitness_Gameplay_Parameters | Crossover_Fusion_Parameters | Mutate_Random_Ending_Parameters | Mutate_Cut_And_Generation_Parameters, _Variable_Chain__Name: list[str], _Range: list[int | float], _Nominal__Value: int | float, _Sample_Size: int, _Max__Generations: int, _Stop_At__Beating_Level: bool, _Require__Beating_Level: bool, _Require__No_Loop_Fittest_Individual: bool, _Generation_Parameters: Generation_Creation_Parameters, _Fitness_Parameters: Fitness_Gameplay_Parameters, _Crossover_Parameters: Crossover_Fusion_Parameters, _Mutation_Parameters: Mutate_Random_Ending_Parameters | Mutate_Cut_And_Generation_Parameters):
	"""
	Generates Temporary Files for each attempt of the Genetic Algorithm to calculate the averaged Sensitivity stats, and Logs them in Output.txt, describing the changes and the resulting stats, inside the Sensitivity Analysis Folder of the given Level, deleting the Temporary Files when done.
	"""


	Parameter__Name: Generation_Creation_Parameters | Fitness_Gameplay_Parameters | Crossover_Fusion_Parameters | Mutate_Random_Ending_Parameters | Mutate_Cut_And_Generation_Parameters = type(_Parameter).__name__

	Variable_Chain__Length: int = len(_Variable_Chain__Name)


	for i in range(Variable_Chain__Length):
		Parameter__Name += f".{_Variable_Chain__Name[i]}"


		if i == Variable_Chain__Length - 1:
			break


		_Parameter = getattr(_Parameter, _Variable_Chain__Name[i])


	with open(f"Logs/Genetic Algorithm/Level {_Level}/Sensitivity Analysis/Output.txt", "a") as File:
		for _Variable__Value in _Range:
			for _Attempt in range(_Sample_Size):
				print(f"\n\nAttempt {_Attempt + 1}. {Parameter__Name} from {_Nominal__Value} to {_Variable__Value}")


				setattr(_Parameter, _Variable_Chain__Name[-1], _Variable__Value)
				Execute__Genetic_Algorithm([_Level], "Sensitivity Analysis/Temporary File", _Attempt + 1, _Max__Generations, _Stop_At__Beating_Level, _Require__Beating_Level, _Require__No_Loop_Fittest_Individual, _Generation_Parameters, _Fitness_Parameters, _Crossover_Parameters, _Mutation_Parameters)


			Test_Sensitivity_Stats: Sensitivity_Stats = Get__Averaged_Sensitivity_Stats(_Level, "Sensitivity Analysis/Temporary File", _Sample_Size, True)


			File.write(f"Stats of the Genetic Algorithm using Nominal values while changing Crossover and Mutation Versions to:\n{_Crossover_Parameters}\n{_Mutation_Parameters}\nAnd changing {Parameter__Name} from {_Nominal__Value} to {_Variable__Value}:\n{Test_Sensitivity_Stats}\n\n")


		setattr(_Parameter, _Variable_Chain__Name[-1], _Nominal__Value)



# Number of times to test each combination of Parameters
Sample_Size: int = 5


# Levels to run the Genetic Algorithm in
Levels: list[int] = [
	3
]



# Genetic Algorithm
Max__Generations: int = 100

Stop_At__Beating_Level: bool = True
Require__Beating_Level: bool = False
Require__No_Loop_Fittest_Individual: bool = True


# Nominal Parameters for the Creation of the first Generation
Nominal_Generation_Parameters: Generation_Creation_Parameters = Generation_Creation_Parameters(
	Generation__Size = 100,
	Actions__Amount = 10
)

Generation_Parameter_Size__Range: list[int] = [2, 5, 10, 20, 35, 50, 75, 200]
Generation_Parameter_Actions__Amount__Range: list[int] = [1, 3, 5, 15, 20, 30, 40, 50, 80, 100]


# Nominal Parameters for the Fitness function
Nominal_Fitness_Parameters: Fitness_Gameplay_Parameters = Fitness_Gameplay_Parameters(
	Length__Weight = 10.0,
	Obtained_Keys__Bonus = 500.0,
	Used_Keys__Bonus = 1000.0,
	Has__Won__Bonus = 1000000.0,
	Has__Looped__Penalty = -1000000.0
)

Fitness_Parameter_Length__Weight__Range: list[float] = [1.0, 5.0, 50.0, 100.0, 1000.0]
Fitness_Parameter_Obtained_Keys__Bonus__Range: list[float] = [10.0, 50.0, 100.0, 200.0, 350.0, 650.0, 800.0, 1000.0, 5000.0, 10000.0]
Fitness_Parameter_Used_Keys__Bones__Range: list[float] = [10.0, 50.0, 100.0, 200.0, 350.0, 500.0, 800.0, 2000.0, 5000.0, 10000.0]


# Nominal Parameters for the Crossover step
Nominal_Crossover_Parameters: Crossover_Fusion_Parameters = Crossover_Fusion_Parameters(
	Search_Start_Percent = 0.2,
	Search_End_Percent = 1.0,

	Fallback_Parameters = Crossover_Fusion_Bi_BFS_Fallback_Parameters()
)

# Nominal Fallback Versions for the Crossover step
Nominal_Crossover_Fallback_Versions: list[Crossover_Fusion_Bi_BFS_Fallback_Parameters | Crossover_Fusion_Regeneration_Fallback_Parameters | Crossover_Fusion_Cut_And_Generation_Fallback_Parameters | Crossover_Fusion_Clone_Fallback_Parameters] = [
	Crossover_Fusion_Bi_BFS_Fallback_Parameters(
		Max__Depth = 12
	),
	Crossover_Fusion_Cut_And_Generation_Fallback_Parameters(
		Mutate_Cut_And_Generation_Parameters(
			Random_Cut_Start_Percent = 0.3
		)
	),
	Crossover_Fusion_Cut_And_Generation_Fallback_Parameters(
		Mutate_Cut_And_Generation_Parameters(
			Last_Actions_To_Change = 10
		)
	),
	Crossover_Fusion_Regeneration_Fallback_Parameters(
		Nominal_Generation_Parameters
	),
	Crossover_Fusion_Clone_Fallback_Parameters()
]


Crossover_Parameter_Search_Start_Percent__Range: list[float] = [0.01, 0.05, 0.1, 0.15, 0.25, 0.35, 0.5, 0.6, 0.7, 0.8]
Crossover_Parameter_Search_End_Percent__Range: list[float] = [0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.6, 0.7, 0.8, 0.9]

Crossover_Fallback_Parameter_Bi_BFS_Max__Depth__Range: list[int] = [1, 2, 3, 5, 8, 10, 15, 18]
Crossover_Fallback_Parameter_Cut_And_Generation_Random_Cut_Start_Percent__Range: list[float] = [0.01, 0.05, 0.1, 0.15, 0.2, 0.4, 0.5, 0.6, 0.7, 0.8]
Crossover_Fallback_Parameter_Cut_And_Generation_Last_Actions_To_Change__Range: list[float] = [1, 3, 5, 8, 15, 25, 35, 50, 80, 100]


# Nominal Parameters for the Mutation step
Nominal_Mutation_Parameters: Mutate_Random_Ending_Parameters = Mutate_Random_Ending_Parameters(
	New_Actions__Amount = 5
)

Nominal_Mutation_Versions: list[Mutate_Random_Ending_Parameters | Mutate_Cut_And_Generation_Parameters] = [
	Mutate_Random_Ending_Parameters(
		New_Actions__Amount = 5
	),
	Mutate_Cut_And_Generation_Parameters(
		Random_Cut_Start_Percent = 0.3
	),
	Mutate_Cut_And_Generation_Parameters(
		Last_Actions_To_Change = 10
	)
]


Mutation_Random_Ending_Parameter_New_Actions__Amount__Range: list[int] = [1, 2, 3, 8, 10, 20, 35, 50]
Mutation_Cut_And_Generation_Parameter_Random_Cut_Start_Percent__Range: list[float] = [0.01, 0.05, 0.1, 0.15, 0.2, 0.4, 0.5, 0.6, 0.7, 0.8]
Mutation_Cut_And_Generation_Parameter_Last_Actions_To_Change__Range: list[float] = [1, 3, 5, 8, 15, 25, 35, 50, 80, 100]



# References
Reference_Attempts__Amount: int = 3


Generation_Parameters: Generation_Creation_Parameters = deepcopy(Nominal_Generation_Parameters)
Fitness_Parameters: Fitness_Gameplay_Parameters = deepcopy(Nominal_Fitness_Parameters)
Crossover_Parameters: Crossover_Fusion_Parameters = deepcopy(Nominal_Crossover_Parameters)
Mutation_Parameters: Mutate_Random_Ending_Parameters | Mutate_Cut_And_Generation_Parameters = deepcopy(Nominal_Mutation_Parameters)
Reference_Sensitivity_Stats: Sensitivity_Stats = Get__Averaged_Sensitivity_Stats(3, "Crossover with Bi-BFS", Reference_Attempts__Amount)

# Sensitivity Analysis for each given Level
for _Level in Levels:
	Reference_Sensitivity_Stats: Sensitivity_Stats = Get__Averaged_Sensitivity_Stats(_Level, "Crossover with Bi-BFS", Reference_Attempts__Amount)


	with open(f"Logs/Genetic Algorithm/Level {_Level}/Sensitivity Analysis/Output.txt", "w") as File:
		File.write(f"Reference Sensitivity Stats:\n{Reference_Sensitivity_Stats}\n\n\n\n")


	for _Crossover_Fallback_Version in Nominal_Crossover_Fallback_Versions:
		Crossover_Parameters.Fallback_Parameters = _Crossover_Fallback_Version


		for _Mutation_Version in Nominal_Mutation_Versions:
			Mutation_Parameters = _Mutation_Version


			# Generation Parameters
			Generate__Sensitivity_Stats(
				_Level,
				Generation_Parameters,
				["Generation__Size"],
				Generation_Parameter_Size__Range,
				Nominal_Generation_Parameters.Generation__Size,
				Sample_Size,
				Max__Generations,
				Stop_At__Beating_Level,
				Require__Beating_Level,
				Require__No_Loop_Fittest_Individual,
				Generation_Parameters,
				Fitness_Parameters,
				Crossover_Parameters,
				Mutation_Parameters
			)

			Generate__Sensitivity_Stats(
				_Level,
				Generation_Parameters,
				["Actions__Amount"],
				Generation_Parameter_Actions__Amount__Range,
				Nominal_Generation_Parameters.Actions__Amount,
				Sample_Size,
				Max__Generations,
				Stop_At__Beating_Level,
				Require__Beating_Level,
				Require__No_Loop_Fittest_Individual,
				Generation_Parameters,
				Fitness_Parameters,
				Crossover_Parameters,
				Mutation_Parameters
			)


			# Fitness Parameters
			Generate__Sensitivity_Stats(
				_Level,
				Fitness_Parameters,
				["Length__Weight"],
				Fitness_Parameter_Length__Weight__Range,
				Nominal_Fitness_Parameters.Length__Weight,
				Sample_Size,
				Max__Generations,
				Stop_At__Beating_Level,
				Require__Beating_Level,
				Require__No_Loop_Fittest_Individual,
				Generation_Parameters,
				Fitness_Parameters,
				Crossover_Parameters,
				Mutation_Parameters
			)

			Generate__Sensitivity_Stats(
				_Level,
				Fitness_Parameters,
				["Obtained_Keys__Bonus"],
				Fitness_Parameter_Obtained_Keys__Bonus__Range,
				Nominal_Fitness_Parameters.Obtained_Keys__Bonus,
				Sample_Size,
				Max__Generations,
				Stop_At__Beating_Level,
				Require__Beating_Level,
				Require__No_Loop_Fittest_Individual,
				Generation_Parameters,
				Fitness_Parameters,
				Crossover_Parameters,
				Mutation_Parameters
			)

			Generate__Sensitivity_Stats(
				_Level,
				Fitness_Parameters,
				["Used_Keys__Bonus"],
				Fitness_Parameter_Used_Keys__Bones__Range,
				Nominal_Fitness_Parameters.Used_Keys__Bonus,
				Sample_Size,
				Max__Generations,
				Stop_At__Beating_Level,
				Require__Beating_Level,
				Require__No_Loop_Fittest_Individual,
				Generation_Parameters,
				Fitness_Parameters,
				Crossover_Parameters,
				Mutation_Parameters
			)


			# Crossover Parameters
			Generate__Sensitivity_Stats(
				_Level,
				Crossover_Parameters,
				["Search_Start_Percent"],
				Crossover_Parameter_Search_Start_Percent__Range,
				Nominal_Crossover_Parameters.Search_Start_Percent,
				Sample_Size,
				Max__Generations,
				Stop_At__Beating_Level,
				Require__Beating_Level,
				Require__No_Loop_Fittest_Individual,
				Generation_Parameters,
				Fitness_Parameters,
				Crossover_Parameters,
				Mutation_Parameters
			)

			Generate__Sensitivity_Stats(
				_Level,
				Crossover_Parameters,
				["Search_End_Percent"],
				Crossover_Parameter_Search_End_Percent__Range,
				Nominal_Crossover_Parameters.Search_End_Percent,
				Sample_Size,
				Max__Generations,
				Stop_At__Beating_Level,
				Require__Beating_Level,
				Require__No_Loop_Fittest_Individual,
				Generation_Parameters,
				Fitness_Parameters,
				Crossover_Parameters,
				Mutation_Parameters
			)

			if isinstance(_Crossover_Fallback_Version, Crossover_Fusion_Bi_BFS_Fallback_Parameters):
				Generate__Sensitivity_Stats(
					_Level,
					Crossover_Parameters,
					["Fallback_Parameters", "Max__Depth"],
					Crossover_Fallback_Parameter_Bi_BFS_Max__Depth__Range,
					Nominal_Crossover_Fallback_Versions[0].Max__Depth,
					Sample_Size,
					Max__Generations,
					Stop_At__Beating_Level,
					Require__Beating_Level,
					Require__No_Loop_Fittest_Individual,
					Generation_Parameters,
					Fitness_Parameters,
					Crossover_Parameters,
					Mutation_Parameters
				)

			if isinstance(_Crossover_Fallback_Version, Crossover_Fusion_Cut_And_Generation_Fallback_Parameters) and _Crossover_Fallback_Version.Cut_And_Generation_Parameters.Random_Cut_Start_Percent != -1.0:
				Generate__Sensitivity_Stats(
					_Level,
					Crossover_Parameters,
					["Fallback_Parameters", "Cut_And_Generation_Parameters", "Random_Cut_Start_Percent"],
					Crossover_Fallback_Parameter_Cut_And_Generation_Random_Cut_Start_Percent__Range,
					Nominal_Crossover_Fallback_Versions[1].Cut_And_Generation_Parameters.Random_Cut_Start_Percent,
					Sample_Size,
					Max__Generations,
					Stop_At__Beating_Level,
					Require__Beating_Level,
					Require__No_Loop_Fittest_Individual,
					Generation_Parameters,
					Fitness_Parameters,
					Crossover_Parameters,
					Mutation_Parameters
				)
			elif isinstance(_Crossover_Fallback_Version, Crossover_Fusion_Cut_And_Generation_Fallback_Parameters) and _Crossover_Fallback_Version.Cut_And_Generation_Parameters.Last_Actions_To_Change != 0:
				Generate__Sensitivity_Stats(
					_Level,
					Crossover_Parameters,
					["Fallback_Parameters", "Cut_And_Generation_Parameters", "Last_Actions_To_Change"],
					Crossover_Fallback_Parameter_Cut_And_Generation_Last_Actions_To_Change__Range,
					Nominal_Crossover_Fallback_Versions[2].Cut_And_Generation_Parameters.Last_Actions_To_Change,
					Sample_Size,
					Max__Generations,
					Stop_At__Beating_Level,
					Require__Beating_Level,
					Require__No_Loop_Fittest_Individual,
					Generation_Parameters,
					Fitness_Parameters,
					Crossover_Parameters,
					Mutation_Parameters
				)


			# Mutation Parameters
			if isinstance(_Mutation_Version, Mutate_Random_Ending_Parameters):
				Generate__Sensitivity_Stats(
					_Level,
					Mutation_Parameters,
					["New_Actions__Amount"],
					Mutation_Random_Ending_Parameter_New_Actions__Amount__Range,
					Nominal_Mutation_Versions[0].New_Actions__Amount,
					Sample_Size,
					Max__Generations,
					Stop_At__Beating_Level,
					Require__Beating_Level,
					Require__No_Loop_Fittest_Individual,
					Generation_Parameters,
					Fitness_Parameters,
					Crossover_Parameters,
					Mutation_Parameters
				)
			else:
				if _Mutation_Version.Random_Cut_Start_Percent != -1.0:
					Generate__Sensitivity_Stats(
						_Level,
						Mutation_Parameters,
						["Random_Cut_Start_Percent"],
						Mutation_Cut_And_Generation_Parameter_Random_Cut_Start_Percent__Range,
						Nominal_Mutation_Versions[1].Random_Cut_Start_Percent,
						Sample_Size,
						Max__Generations,
						Stop_At__Beating_Level,
						Require__Beating_Level,
						Require__No_Loop_Fittest_Individual,
						Generation_Parameters,
						Fitness_Parameters,
						Crossover_Parameters,
						Mutation_Parameters
					)
				elif _Mutation_Version.Last_Actions_To_Change != 0:
					Generate__Sensitivity_Stats(
						_Level,
						Mutation_Parameters,
						["Last_Actions_To_Change"],
						Mutation_Cut_And_Generation_Parameter_Last_Actions_To_Change__Range,
						Nominal_Mutation_Versions[2].Last_Actions_To_Change,
						Sample_Size,
						Max__Generations,
						Stop_At__Beating_Level,
						Require__Beating_Level,
						Require__No_Loop_Fittest_Individual,
						Generation_Parameters,
						Fitness_Parameters,
						Crossover_Parameters,
						Mutation_Parameters
					)
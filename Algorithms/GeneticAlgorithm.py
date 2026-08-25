from random import choice, choices, randint

from dataclasses import dataclass, field


from Game import Game, Action_Type, Action
from Algorithms.BruteForce import Bi_BFS



@dataclass
class Fitness_Gameplay_Description:
	Has__Won: bool = False
	Has__Looped: bool = False

	Obtained__Keys: int = 0
	Used__Keys: int = 0

@dataclass
class Fitness_Evaluation:
	Score: int = 0
	Description: Fitness_Gameplay_Description = field(default_factory = Fitness_Gameplay_Description)

@dataclass
class Individual:
	Action_History: list[Action] = field(default_factory = list)
	Fitness: Fitness_Evaluation = field(default_factory = Fitness_Evaluation)



@dataclass
class Generation_Creation_Parameters:
	Generation__Size: int
	Actions__Amount: int


	# Returns a string representing itself
	def __str__(self, _Indentation__Amount: int = 0) -> str:
		return f"Generation Version: Creation. Parameters:\n{"  " * _Indentation__Amount}- Generation__Size: {self.Generation__Size}\n{"  " * _Indentation__Amount}- Actions__Amount: {self.Actions__Amount}"



@dataclass
class Fitness_Gameplay_Parameters:
	Length__Weight: float
	Obtained_Keys__Bonus: float
	Used_Keys__Bonus: float
	Has__Won__Bonus: float
	Has__Looped__Penalty: float


	# Returns a string representing itself
	def __str__(self) -> str:
		return f"Fitness Version: Gameplay. Parameters:\n- Length__Weight: {self.Length__Weight}\n- Obtained_Keys__Bonus: {self.Obtained_Keys__Bonus}\n- Used_Keys__Bonus: {self.Used_Keys__Bonus}\n- Has__Won__Bonus: {self.Has__Won__Bonus}\n- Has__Looped__Penalty: {self.Has__Looped__Penalty}"



@dataclass
class Crossover_Fusion_Bi_BFS_Fallback_Parameters:
	Max__Depth: int = -1


	# Returns a string representing itself
	def __str__(self, _Indentation__Amount: int = 0) -> str:
		return f"Crossover Fallback Version: Bi-BFS. Parameters:\n{"  " * _Indentation__Amount}- Max__Depth: {self.Max__Depth}"


@dataclass
class Mutate_Cut_And_Generation_Parameters:
	Random_Cut_Start_Percent: float = -1.0
	Last_Actions_To_Change: int = 0


	# Returns a string representing itself
	def __str__(self, _Indentation__Amount: int = 0) -> str:
		return f"Mutation Version: Cut and Generation. Parameters:\n{"  " * _Indentation__Amount}- Random_Cut_Start_Percent: {self.Random_Cut_Start_Percent}\n{"  " * _Indentation__Amount}- Last_Actions_To_Change: {self.Last_Actions_To_Change}"


@dataclass
class Crossover_Fusion_Cut_And_Generation_Fallback_Parameters:
	Cut_And_Generation_Parameters: Mutate_Cut_And_Generation_Parameters


	# Returns a string representing itself
	def __str__(self, _Indentation__Amount: int = 0) -> str:
		return f"Crossover Fallback Version: Cut and Generation. Parameters:\n{"  " * _Indentation__Amount}- Cut_And_Generation_Parameters: {self.Cut_And_Generation_Parameters.__str__(_Indentation__Amount + 1)}"

@dataclass
class Crossover_Fusion_Regeneration_Fallback_Parameters:
	Generation_Parameters: Generation_Creation_Parameters


	# Returns a string representing itself
	def __str__(self, _Indentation__Amount: int = 0) -> str:
		return f"Crossover Fallback Version: Regeneration. Parameters:\n{"  " * _Indentation__Amount}- Generation_Parameters: {self.Generation_Parameters.__str__(_Indentation__Amount + 1)}"

@dataclass
class Crossover_Fusion_Clone_Fallback_Parameters:
	# Returns a string representing itself
	def __str__(self, _Indentation__Amount: int = 0) -> str:
		return "Crossover Fallback Version: Clone (doesn't have any Parameters)"

@dataclass
class Crossover_Fusion_Parameters:
	Search_Start_Percent: float
	Search_End_Percent: float

	Fallback_Parameters: Crossover_Fusion_Bi_BFS_Fallback_Parameters | Crossover_Fusion_Regeneration_Fallback_Parameters |  Crossover_Fusion_Cut_And_Generation_Fallback_Parameters | Crossover_Fusion_Clone_Fallback_Parameters


	# Returns a string representing itself
	def __str__(self) -> str:
		return f"Crossover Version: Fusion. Parameters:\n- Search_Start_Percent: {self.Search_Start_Percent}\n- Search_End_Percent: {self.Search_End_Percent}\n- Fallback_Parameters: {self.Fallback_Parameters.__str__(1)}"



@dataclass
class Mutate_Random_Ending_Parameters:
	New_Actions__Amount: int


	# Returns a string representing itself
	def __str__(self) -> str:
		return f"Mutation Version: Random Ending. Parameters:\n- New_Actions__Amount: {self.New_Actions__Amount}"



# Creates a randomly generated Generation with the given Parameters
def Create_Generation(_Parameters: Generation_Creation_Parameters, _Level: int) -> list[Individual]:
	"""
	Creates and returns a randomly generated Generation with the given Parameters.
	"""


	Generation: list[Individual] = []


	for _ in range(_Parameters.Generation__Size):
		Individual_Game: Game = Game(_Level)
		_Individual: Individual = Individual()


		for __ in range(_Parameters.Actions__Amount):
			Chosen_Action: Action = choice(Individual_Game.Get_Decision_Space())


			Individual_Game.Execute_Action(Chosen_Action)
			_Individual.Action_History.append(Chosen_Action)
		

		Generation.append(_Individual)


	return Generation



# Fitness function that evaluates the given Individual based on events ocurred during gameplay
def Fitness_Gameplay(_Individual: Individual, _Parameters: Fitness_Gameplay_Parameters, _Level: int) -> None:
	"""
	Fitness function that evaluates the given Individual based on:

	- The amount of Actions made
	- The amount of Keys found
	- The amount of Keys used

	Furthermore, it adds an important bonus if the Individual beats the Level, and subtracts an important penalty if the Individual reaches a State it has already visited before.
	"""


	Individual_Game: Game = Game(_Level)
	Visited_States: list[str] = [str(Individual_Game)]


	for _Action__Index, _Action in enumerate(_Individual.Action_History):
		if _Action.Type == Action_Type.Explorer__Move:
			Required_Keys: int = Individual_Game.Get_Required_Keys(Individual_Game.Explorers[0], _Action.Direction)

			_Individual.Fitness.Score += _Parameters.Used_Keys__Bonus * Required_Keys
			_Individual.Fitness.Description.Used__Keys += Required_Keys


			if _Action.Undo_Data.Entry_Room.Initial_Has == "Key":
				_Individual.Fitness.Score += _Parameters.Obtained_Keys__Bonus
				_Individual.Fitness.Description.Obtained__Keys += 1



		Individual_Game.Execute_Action(_Action)


		Current_State: str = str(Individual_Game)


		if Current_State in Visited_States:
			_Individual.Fitness.Score += _Parameters.Has__Looped__Penalty
			_Individual.Fitness.Description.Has__Looped = True


			break


		if Individual_Game.Has__Won():
			_Individual.Fitness.Score += _Parameters.Has__Won__Bonus
			_Individual.Fitness.Description.Has__Won = True


			break


		Visited_States.append(Current_State)
	

	_Individual.Fitness.Score += _Parameters.Length__Weight * (_Action__Index + 1)


# Intermediate function that Evaluates the given Individual with the Fitness function determined by the given Version
def Evaluate_Fitness(_Individual: Individual, _Parameters: Fitness_Gameplay_Parameters, _Level: int) -> None:
	"""
	Intermediate function that Evaluates the given Individual with the Fitness function determined by the given Version, which can be:

	- "Gameplay"
	"""


	match _Parameters:
		case Fitness_Gameplay_Parameters():
			Fitness_Gameplay(_Individual, _Parameters, _Level)



# Selection function that chooses Individuals from the given Generation with chances weighted by their Fitness
def Select_Parents(_Generation: list[Individual]) -> list[Individual]:
	"""
	Selection function that returns a list of the same size as the Generation with the Selected Individuals, chosen at random with each Individual's Fitness as its Weight.

	If all Fitnesses are negative, the Weight of each Individual becomes the difference between its Fitness and the worst one in the Generation, this makes the worst Individuals impossible to be Selected. (If all Individuals share the same negative Fitness, the Selection occurs with equal probability.)
	"""


	if all(_Individual.Fitness.Score <= 0.0 for _Individual in _Generation):
		Worst_Fitness: float = min([_Individual.Fitness.Score for _Individual in _Generation])


		if all(_Individual.Fitness.Score - Worst_Fitness == 0.0 for _Individual in _Generation):
			return choices(_Generation, k = len(_Generation))


		return choices(_Generation, [_Individual.Fitness.Score - Worst_Fitness for _Individual in _Generation], k = len(_Generation))


	return choices(_Generation, [max(_Individual.Fitness.Score, 0.0) for _Individual in _Generation], k = len(_Generation))



# Crossover function that crosses Individuals from the given Generation if they share a State, otherwise it performs the given Fallback
def Crossover_Fusion(_Generation: list[Individual], _Parameters: Crossover_Fusion_Parameters, _Level: int) -> list[Individual]:
	"""
	Crossover function that crosses Individuals from the given Generation and returns the next Generation based on 2 cases:

	- If the Individuals share a State, the shortest Action history to it between the two is kept for both children, and then each parent's following Action history is added to one child.
	- If no more Individuals share a State, the given Fallback is performed, which can be:
		- For each Individual, a random State is chosen, it gets crossed with the next available Individual, which also gets a random State chosen. The second child will have the first parent's Action history up to the chosen State, then this State will get connected with the chosen State of the other parent with Bi-BFS, adding the rest of its Action history afterwards. The first child will be a clone of the most Fit parent. If the Bi-BFS reaches the given maximum depth, the second child will be a clone of the other parent.
		- Regenerate each Individual with a given amount of starting Actions.
		- For each Individual, apply the Mutation Cut and Generation, which selects some starting part of the Action history, and generates Actions until reaching the original Action history's length.
		- Clone each Individual.
	"""


	Next_Generation: list[Individual] = []
	Processed_Indices: list[int] = []


	for i_A in range(len(_Generation)):
		for i_B in range(i_A + 1, len(_Generation)):
			if _Generation[i_A] is _Generation[i_B] or i_A in Processed_Indices or i_B in Processed_Indices:
				continue


			Game_A: Game = Game(_Level)
			Game_B: Game = Game(_Level)

			Start_A__Index: int = int(_Parameters.Search_Start_Percent * (len(_Generation[i_A].Action_History) - 1))
			Start_B__Index: int = int(_Parameters.Search_Start_Percent * (len(_Generation[i_B].Action_History) - 1))


			for i in range(Start_A__Index):
				Game_A.Execute_Action(_Generation[i_A].Action_History[i])

			for i in range(Start_B__Index):
				Game_B.Execute_Action(_Generation[i_B].Action_History[i])


			Saved_States_A: list[str] = []
			Saved_States_B: list[str] = []


			for i in range(Start_A__Index, int(_Parameters.Search_End_Percent * len(_Generation[i_A].Action_History))):
				Game_A.Execute_Action(_Generation[i_A].Action_History[i])


				Saved_States_A.append(str(Game_A))

			for i in range(Start_B__Index, int(_Parameters.Search_End_Percent * len(_Generation[i_B].Action_History))):
				Game_B.Execute_Action(_Generation[i_B].Action_History[i])


				Saved_States_B.append(str(Game_B))


			for State_A__Index in range(len(Saved_States_A)):
				if Saved_States_A[State_A__Index] in Saved_States_B:
					State_B__Index: int = Saved_States_B.index(Saved_States_A[State_A__Index])

					Is__Cloned_Individual_A: bool = Start_A__Index + State_A__Index <= Start_B__Index + State_B__Index
					Cloned_Individual: Individual = Individual(_Generation[i_A].Action_History.copy() if Is__Cloned_Individual_A else _Generation[i_B].Action_History.copy())
					Next_Generation.append(Cloned_Individual)


					if Is__Cloned_Individual_A:
						Next_Generation.append(Individual(Cloned_Individual.Action_History[: Start_A__Index + State_A__Index + 1] + _Generation[i_B].Action_History[Start_B__Index + State_B__Index + 1 :]))
					else:
						Next_Generation.append(Individual(Cloned_Individual.Action_History[: Start_B__Index + State_B__Index + 1] + _Generation[i_A].Action_History[Start_A__Index + State_A__Index + 1 :]))

					
					Processed_Indices.append(i_A)
					Processed_Indices.append(i_B)


					break


	if len(Processed_Indices) == len(_Generation):
		return Next_Generation


	match _Parameters.Fallback_Parameters:
		case Crossover_Fusion_Bi_BFS_Fallback_Parameters():
			for i_A in range(len(_Generation)):
				for i_B in range(i_A + 1, len(_Generation)):
					if i_A in Processed_Indices or i_B in Processed_Indices:
						continue


					Game_A: Game = Game(_Level)
					Game_B: Game = Game(_Level)

					State_A__Index = randint(1, len(_Generation[i_A].Action_History))
					State_B__Index = randint(0, len(_Generation[i_B].Action_History) - 1)


					for i in range(State_A__Index):
						Game_A.Execute_Action(_Generation[i_A].Action_History[i])

					for i in range(State_B__Index):
						Game_B.Execute_Action(_Generation[i_B].Action_History[i])


					Next_Generation.append(Individual(_Generation[i_A].Action_History.copy() if _Generation[i_A].Fitness.Score >= _Generation[i_B].Fitness.Score else _Generation[i_B].Action_History.copy()))


					Bi_BFS_Actions: tuple[list[Action], float] | None = Bi_BFS(Game_A, Game_B, _Parameters.Fallback_Parameters.Max__Depth)


					if Bi_BFS_Actions:
						Bi_BFS_Actions = Bi_BFS_Actions[0]


						Next_Generation.append(Individual(_Generation[i_A].Action_History[: State_A__Index] + Bi_BFS_Actions + _Generation[i_B].Action_History[State_B__Index :]))
					else:
						Next_Generation.append(Individual(_Generation[i_A].Action_History.copy() if _Generation[i_A].Fitness.Score < _Generation[i_B].Fitness.Score else _Generation[i_B].Action_History.copy()))


					Processed_Indices.append(i_A)
					Processed_Indices.append(i_B)

		case Crossover_Fusion_Cut_And_Generation_Fallback_Parameters():
			for i, _Individual in enumerate(_Generation):
				if i in Processed_Indices:
					continue


				New_Individual: Individual = Individual(_Individual.Action_History.copy())
				Mutate_Cut_And_Generation(New_Individual, _Parameters.Fallback_Parameters.Cut_And_Generation_Parameters, _Level)


				Next_Generation.append(New_Individual)

		case Crossover_Fusion_Regeneration_Fallback_Parameters():
			Next_Generation += Create_Generation(
				Generation_Creation_Parameters(
					_Parameters.Fallback_Parameters.Generation_Parameters.Generation__Size - len(Next_Generation),
					_Parameters.Fallback_Parameters.Generation_Parameters.Actions__Amount
				),
				_Level
			)

		case Crossover_Fusion_Clone_Fallback_Parameters():
			for i, _Individual in enumerate(_Generation):
				if i in Processed_Indices:
					continue
				

				Next_Generation.append(Individual(_Individual.Action_History.copy()))


	return Next_Generation


# Intermediate function that Performs the Crossing over of the given Generation with the function determined by the given Version
def Perform_Crossover(_Generation: list[Individual], _Parameters: Crossover_Fusion_Parameters, _Level: int) -> list[Individual]:
	"""
	Intermediate function that Performs the Crossing over of the Generation with the function determined by the given Version, which can be:

	- "Fusion"
	"""


	match _Parameters:
		case Crossover_Fusion_Parameters():
			return Crossover_Fusion(_Generation, _Parameters, _Level)



# Mutation function that mutates the given Individual by adding the given amount of valid new Actions at the end of the Action history
def Mutate_Random_Ending(_Individual: Individual, _Parameters: Mutate_Random_Ending_Parameters, _Level: int) -> None:
	"""
	Mutation function that mutates the given Individual by adding the given amount of valid new Actions at the end of the Action history.
	"""


	Individual_Game: Game = Game(_Level)


	for _Action in _Individual.Action_History:
		Individual_Game.Execute_Action(_Action)
	

	for _ in range(_Parameters.New_Actions__Amount):
		Chosen_Action: Action = choice(Individual_Game.Get_Decision_Space())


		Individual_Game.Execute_Action(Chosen_Action)
		_Individual.Action_History.append(Chosen_Action)

# Mutation function that mutates the given Individual by cutting its Action history in a random position (considering a start offset for the random selection), or in a given amount of Actions from the last, and generating random valid Actions until reaching the original history's length
def Mutate_Cut_And_Generation(_Individual: Individual, _Parameters: Mutate_Cut_And_Generation_Parameters, _Level: int) -> None:
	"""
	Mutation function that mutates the given Individual by cutting its Action history in a random position (considering a start offset for the random selection), or in a given amount of Actions from the last, and generating random valid Actions until reaching the original history's length.

	If the Individual has looped, the Mutation will regenerate the entire Action history until reaching the original one's length.
	"""


	Individual_Game: Game = Game(_Level)

	Original_Action_Length: int = len(_Individual.Action_History)


	if _Individual.Fitness.Description.Has__Looped:
		_Individual.Action_History = []
	else:
		if _Parameters.Random_Cut_Start_Percent != -1.0:
			_Individual.Action_History = _Individual.Action_History[: randint(int(_Parameters.Random_Cut_Start_Percent * len(_Individual.Action_History)), len(_Individual.Action_History))]
		else:
			_Individual.Action_History = _Individual.Action_History[: max(0, len(_Individual.Action_History) - _Parameters.Last_Actions_To_Change)]


	for _Action__Index in range(len(_Individual.Action_History)):
		Individual_Game.Execute_Action(_Individual.Action_History[_Action__Index])


	while len(_Individual.Action_History) < Original_Action_Length:
		Chosen_Action: Action = choice(Individual_Game.Get_Decision_Space())


		Individual_Game.Execute_Action(Chosen_Action)
		_Individual.Action_History.append(Chosen_Action)


# Intermediate function that Applies a Mutation to the given Individual determined by the given Version
def Apply_Mutation(_Individual: Individual, _Level: int, _Parameters: Mutate_Random_Ending_Parameters | Mutate_Cut_And_Generation_Parameters) -> None:
	"""
	Intermediate function that Applies a Mutation to the given Individual determined by the given Version, which can be:

	- "Random_Ending"
	- "Random_Cut_And_Generation"
	"""


	match _Parameters:
		case Mutate_Random_Ending_Parameters():
			Mutate_Random_Ending(_Individual, _Parameters, _Level)
		
		case Mutate_Cut_And_Generation_Parameters():
			Mutate_Cut_And_Generation(_Individual, _Parameters, _Level)
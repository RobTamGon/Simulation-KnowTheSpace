from time import time
from dataclasses import dataclass
# from sys import setrecursionlimit


from Game import Game, Action


# setrecursionlimit(100000)


Iterations: int = 0


# The setup of the Backtracking algorithm (DFS)
def Backtracking(_Game: Game, _Max_Depth: int) -> tuple[bool, list[Action], int, float]:
	"""
	Initializes the Backtracking algorithm (DFS) and tracks the elapsed time until reaching a winning State to the Level in the given Game.

	Returns a list with the sequence of Actions the algorithm found to reach a winning State.
	"""


	global Iterations
	Iterations = 0


	Action_History: list[Action] = []
	Visited_States: list[str] = []


	Initial_Time: float = time()
	Success = Backtracking_Iteration(_Game, Visited_States, Action_History, _Max_Depth)
	Elapsed_Time: float = time() - Initial_Time


	print(f"Solution{" " if Success else " not "}found with Max Depth {_Max_Depth}, final iteration count: {Iterations:,}. Final time: {Elapsed_Time:.3f} seconds, or {(Elapsed_Time / 60):.3f} minutes, or {(Elapsed_Time / 3600):.3f} hours.\n")


	return Success, Action_History, Iterations, Elapsed_Time

# An iteration of the Backtracking algorithm, equivalent to one Action (Sliding a Room one Tile, or Moving the Explorer one Tile)
def Backtracking_Iteration(_Game: Game, _Visited_States: list[str], _Action_History: list[Action], _Max_Depth: int, _Current_Depth: int = 0) -> bool:
	"""
	The actual implementation of the Backtracking algorithm, an iteration follows this sequence of steps:

	- If there is an Action in the History, execute the last Action there
	- Check if the State reached with that Action has already been visited, return if so
	- Check if the current State is a winning State, return if so
	- Check if continuing would exceed the given _Max_Depth of Actions allowed, return if so
	- Add the current State to the visited States list
	- Get the Decision Space for the current State, and call itself with one of the Actions in that Space, return if that Action leads to a winning State. Otherwise, undo the Action and try another one, repeat until exhausting all possible Actions in the current State
	- If no Actions lead to a winning State, remove the current State from the visited States list and return, since this means going back in the "Graph" / "Tree"
	"""


	global Iterations
	Iterations += 1

	if Iterations % 50000 == 0:
		print(f"Iterations: {Iterations:,}")


	Current_State: str = ""


	if len(_Action_History) > 0:
		_Game.Execute_Action(_Action_History[-1])


		Current_State = str(_Game)


		if Current_State in _Visited_States:
			return False


	if _Game.Has__Won():
		return True


	if _Current_Depth + 1 > _Max_Depth:
		return False


	_Visited_States.append(Current_State if Current_State != "" else str(_Game))


	for _Action in _Game.Get_Decision_Space():
		_Action_History.append(_Action)


		if Backtracking_Iteration(_Game, _Visited_States, _Action_History, _Max_Depth, _Current_Depth + 1):
			return True


		_Game.Undo_Action(_Action_History.pop())


	_Visited_States.pop()


	return False


# BFS algorithm
def BFS(_Game: Game, _Target_State: str = "", _Max_Depth: int = -1) -> tuple[list[Action], int, int, float]:
	"""
	Implementation of the BFS algorithm, tracks the elapsed time until reaching a winning State to the Level in the given Game, or the _Target_State if given.

	Returns a list with the sequence of Actions the algorithm found to reach the desired State, plus some other metrics.
	"""


	Iterations: int = 0

	Action_History: list[Action] = []
	Visited_States: list[str] = []

	Initial_Time: float = time()
	Elapsed_Time: float = -1.0


	if (_Target_State == "" and not _Game.Has__Won()) or (_Target_State != "" and str(_Game) != _Target_State):
		Queue: list[list[Action]] = []
		Visited_States.append(str(_Game))


		for _Action in _Game.Get_Decision_Space():
			Action_History.append(_Action)
			Queue.append(Action_History.copy())
			Action_History.pop()


		while len(Queue) > 0:
			Iterations += 1

			if Iterations % 50000 == 0:
				Previous_Time: float = Elapsed_Time
				Elapsed_Time = time() - Initial_Time


				print(f"{Iterations:,} iterations in {Elapsed_Time:.3f} seconds, or {(Elapsed_Time / 60):.3f} minutes, or {(Elapsed_Time / 3600):.3f} hours.{f" {(Elapsed_Time - Previous_Time):.3f} seconds since last log." if Elapsed_Time != -1 else ""}\n")


			Target_History: list[Action] = Queue.pop(0)


			while len(Action_History) > 0 and Action_History != Target_History[: len(Action_History)]:
				_Game.Undo_Action(Action_History.pop())


			for _Action in Target_History[len(Action_History) :]:
				_Game.Execute_Action(_Action)


			Current_State: str = str(_Game)
			Action_History = Target_History


			if Current_State in Visited_States:
				continue
			

			if _Max_Depth != -1 and len(Action_History) > _Max_Depth:
				Iterations -= 1


				break


			Visited_States.append(Current_State)


			if _Target_State != "":
				if Current_State == _Target_State:
					break
			elif _Game.Has__Won():
				if _Max_Depth == -1:
					break
				else:
					continue


			for _Action in _Game.Get_Decision_Space():
				Action_History.append(_Action)
				Queue.append(Action_History.copy())
				Action_History.pop()

	
	Elapsed_Time = time() - Initial_Time


	print(f"{f"Solution found with length {len(Action_History)}" if _Max_Depth == -1 else f"Search space with depth of {_Max_Depth} Actions complete"}, final iteration count: {Iterations:,}, unique states visited: {len(Visited_States):,}. Final time: {Elapsed_Time:.3f} seconds, or {(Elapsed_Time / 60):.3f} minutes, or {(Elapsed_Time / 3600):.3f} hours.")


	return Action_History, Iterations, len(Visited_States), Elapsed_Time


@dataclass
class State:
	String: str
	Action_History: list[Action]


# Bidirectional BFS Algorithm
def Bi_BFS(_Game_A: Game, _Game_B: Game, _Max__Depth: int = -1) -> tuple[list[Action], float] | None:
	"""
	Implementation of the Bidirectional BFS algorithm, tracks the elapsed time until reaching a common State between _Game_A and _Game_B.

	Returns a list with the sequence of Actions the algorithm found to reach the common State from the initial _Game_A State, and then the initial _Game_B State, plus some other metrics.
	"""


	Initial_Time: float = time()


	Found_Solution: bool = str(_Game_A) == str(_Game_B)
	Initialized_First_Queues: bool = False


	Current_Depth_A: int = 1
	Current_Depth_B: int = 1

	Connection_Index_A: int = -1
	Connection_Index_B: int = -1

	Action_History_A: list[Action] = []
	Action_History_B: list[Action] = []

	Queue_A: list[list[Action]] = []
	Queue_B: list[list[Action]] = []

	Visited_States_A: list[State] = []
	Visited_States_B: list[State] = []


	if Found_Solution:
		Elapsed_Time = time() - Initial_Time


		return [], Elapsed_Time


	while not Found_Solution:
		if _Max__Depth != -1 and Current_Depth_A > _Max__Depth:
			return None


		if Current_Depth_A >= 10:
			print(f"Bi-BFS is searching deeply, current depth: {Current_Depth_A} | {Current_Depth_B}")


		if not Initialized_First_Queues:
			Initialized_First_Queues = True

			Visited_States_A.append(State(str(_Game_A), Action_History_A.copy()))
			Visited_States_B.append(State(str(_Game_B), Action_History_B.copy()))


			for _Action in _Game_A.Get_Decision_Space():
				Action_History_A.append(_Action)
				Queue_A.append(Action_History_A.copy())
				Action_History_A.pop()

			for _Action in _Game_B.Get_Decision_Space():
				Action_History_B.append(_Action)
				Queue_B.append(Action_History_B.copy())
				Action_History_B.pop()


		while len(Queue_A) > 0 and len(Queue_A[0]) == Current_Depth_A:
			Target_History_A: list[Action] = Queue_A.pop(0)


			while len(Action_History_A) > 0 and Action_History_A != Target_History_A[: len(Action_History_A)]:
				_Game_A.Undo_Action(Action_History_A.pop())


			for _Action in Target_History_A[len(Action_History_A) :]:
				_Game_A.Execute_Action(_Action)
			

			Current_State_A: str = str(_Game_A)
			Action_History_A = Target_History_A


			if any(Current_State_A == _State.String for _State in Visited_States_A):
				continue


			Visited_States_A.append(State(Current_State_A, Action_History_A.copy()))


			for i, _State in enumerate(Visited_States_B):
				if Current_State_A == _State.String:
					Found_Solution = True
					Connection_Index_B = i


					break
			

			if Found_Solution:
				break


			for _Action in _Game_A.Get_Decision_Space():
				Action_History_A.append(_Action)
				Queue_A.append(Action_History_A.copy())
				Action_History_A.pop()


		if Found_Solution:
			break


		while len(Queue_B) > 0 and len(Queue_B[0]) == Current_Depth_B:
			Target_History_B: list[Action] = Queue_B.pop(0)


			while len(Action_History_B) > 0 and Action_History_B != Target_History_B[: len(Action_History_B)]:
				_Game_B.Undo_Action(Action_History_B.pop())


			for _Action in Target_History_B[len(Action_History_B) :]:
				_Game_B.Execute_Action(_Action)
			

			Current_State_B: str = str(_Game_B)
			Action_History_B = Target_History_B


			if any(Current_State_B == _State.String for _State in Visited_States_B):
				continue


			Visited_States_B.append(State(Current_State_B, Action_History_B.copy()))


			for i, _State in enumerate(Visited_States_A):
				if Current_State_B == _State.String:
					Found_Solution = True
					Connection_Index_A = i


					break


			if Found_Solution:
				break


			for _Action in _Game_B.Get_Decision_Space():
				Action_History_B.append(_Action)
				Queue_B.append(Action_History_B.copy())
				Action_History_B.pop()


		Current_Depth_A += 1
		Current_Depth_B += 1


	Elapsed_Time = time() - Initial_Time


	# print(f"Found the closest common Game State between the 2 Games. Final time: {Elapsed_Time:.3f} seconds, or {(Elapsed_Time / 60):.3f} minutes, or {(Elapsed_Time / 3600):.3f} hours.")


	return Visited_States_A[Connection_Index_A].Action_History + [_Action.Reversed() for _Action in reversed(Visited_States_B[Connection_Index_B].Action_History)], Elapsed_Time
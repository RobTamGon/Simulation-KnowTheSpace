from time import time
from dataclasses import dataclass
from copy import deepcopy
from collections.abc import Callable
from math import inf as C_Infinity

import heapq


from Game import Game, Action, Vector2


@dataclass
class AStar_Queue_Node:
	State: Game
	Action_History: list[Action]
	G_Cost: int
	H_Cost: int
	Final_Cost: float

@dataclass
class AStar_Discovered_Node:
	G_Cost: int | float = 0
	Is__Closed: bool = False


# Initializes Heuristic (Lambda) Functions
Lambda_Zero_H_Cost: Callable[[Game], int] = lambda _Game: 0
Lambda_Explorer_Goal_H_Cost: Callable[[Game], int] = lambda _Game: _Game.Explorers[0].Position.Get_Manhattan_Distance(_Game.Index_Goal().Position)
# ↓ [Inadmissible] ↓
Lambda_Explorer_Key_Goal_Plus_Explorer_Goal_H_Cost: Callable[[Game], int] = lambda _Game: Get_Explorer_Key_Goal_H_Cost(_Game) + Lambda_Explorer_Goal_H_Cost(_Game)

# Gets the sum of the shortest Manhattan distance between the Explorer and a Room with a Key, and between a Room with a Key and the Room with the Goal
def Get_Explorer_Key_Goal_H_Cost(_Game: Game) -> int:
	"""
	Gets and returns the sum of the shortest Manhattan distance between the Explorer and a Room with a Key (remembering the Rooms that previously had Keys), and between a Room with a Key and the Room with the Goal.

	Note: This function minimizes both distances independently.
	"""


	Goal_Position: Vector2 = _Game.Index_Goal().Position

	Minimum_Explorer_Key_Distance: int = C_Infinity
	Minimum_Key_Goal_Distance: int = C_Infinity


	for _Row in _Game.Rooms:
		for _Room in _Row:
			if _Room is None:
				continue


			if _Room.Had == "Key":
				Current_Explorer_Key_Distance: int = _Game.Explorers[0].Position.Get_Manhattan_Distance(_Room.Position)
				Current_Key_Goal_Distance: int = _Room.Position.Get_Manhattan_Distance(Goal_Position)


				if Current_Explorer_Key_Distance < Minimum_Explorer_Key_Distance:
					Minimum_Explorer_Key_Distance = Current_Explorer_Key_Distance

				if Current_Key_Goal_Distance < Minimum_Key_Goal_Distance:
					Minimum_Key_Goal_Distance = Current_Key_Goal_Distance


	if Minimum_Explorer_Key_Distance == C_Infinity:
		Minimum_Explorer_Key_Distance = 0

	if Minimum_Key_Goal_Distance == C_Infinity:
		Minimum_Key_Goal_Distance = 0


	return Minimum_Explorer_Key_Distance + Minimum_Key_Goal_Distance

# [Inadmissible] Gets the sum of the shortest Manhattan distance between the Explorer and a Room with a Key, multiplied by the amount of Keys given to be needed that haven't been obtained yet, and between a Room with a Key and the Room with the Goal
def Old_Get_Explorer_nKeys_Goal_H_Cost(_Game: Game, _Parameters: dict[str, int]) -> int:
	"""
	[Inadmissible]

	Gets and returns the sum of the shortest Manhattan distance between the Explorer and a Room with a Key (remembering the Rooms that previously had Keys), multiplied by the amount of Keys given to be needed that haven't been obtained yet, and between a Room with a Key and the Room with the Goal.

	Heuristic Parameters:

	"Keys": int: Amount of Keys needed to beat the Level.

	Note: This function minimizes both distances independently.
	"""


	Goal_Position: Vector2 = _Game.Index_Goal().Position
	
	Minimum_Explorer_Key_Distance: int = C_Infinity
	Minimum_Key_Goal_Distance: int = C_Infinity


	nKeys_Multiplier: int = _Parameters["Keys"]


	for _Row in _Game.Rooms:
		for _Room in _Row:
			if _Room is None:
				continue


			if _Room.Had == "Key":
				Current_Explorer_Key_Distance: int = _Game.Explorers[0].Position.Get_Manhattan_Distance(_Room.Position)
				Current_Key_Goal_Distance: int = _Room.Position.Get_Manhattan_Distance(Goal_Position)


				if Current_Explorer_Key_Distance < Minimum_Explorer_Key_Distance:
					Minimum_Explorer_Key_Distance = Current_Explorer_Key_Distance

				if Current_Key_Goal_Distance < Minimum_Key_Goal_Distance:
					Minimum_Key_Goal_Distance = Current_Key_Goal_Distance


				if _Room.Has != "Key":
					nKeys_Multiplier = max(nKeys_Multiplier - 1, 0)


	if Minimum_Explorer_Key_Distance == C_Infinity:
		Minimum_Explorer_Key_Distance = 0

	if Minimum_Key_Goal_Distance == C_Infinity:
		Minimum_Key_Goal_Distance = 0


	return Minimum_Explorer_Key_Distance * nKeys_Multiplier + Minimum_Key_Goal_Distance

# Gets the sum of the shortest Manhattan distance between the Explorer and a Room with a Key, multiplied by the amount of Keys given to be needed that haven't been obtained yet, and between a Room with a Key and the Room with the Goal
def Get_Explorer_nKeys_Goal_H_Cost(_Game: Game, _Parameters: dict[str, int]) -> int:
	"""
	Gets and returns the sum of the shortest Manhattan distance between the Explorer and a Room with a Key (remembering the Rooms that previously had Keys), multiplied by the amount of Keys given to be needed that haven't been obtained yet, and between a Room with a Key and the Room with the Goal.

	If the amount of Keys given to be needed that haven't been obtained yet reaches 0, returns the Manhattan distance between the Explorer and the Room with the Goal.

	Heuristic Parameters:

	"Keys": int: Amount of Keys needed to beat the Level.

	Note: This function minimizes both distances independently.
	"""


	Goal_Position: Vector2 = _Game.Index_Goal().Position
	
	Minimum_Explorer_Key_Distance: int = C_Infinity
	Minimum_Key_Goal_Distance: int = C_Infinity


	nKeys_Multiplier: int = _Parameters["Keys"]


	for _Row in _Game.Rooms:
		for _Room in _Row:
			if _Room is None:
				continue


			if _Room.Had == "Key":
				Current_Explorer_Key_Distance: int = _Game.Explorers[0].Position.Get_Manhattan_Distance(_Room.Position)
				Current_Key_Goal_Distance: int = _Room.Position.Get_Manhattan_Distance(Goal_Position)


				if Current_Explorer_Key_Distance < Minimum_Explorer_Key_Distance:
					Minimum_Explorer_Key_Distance = Current_Explorer_Key_Distance

				if Current_Key_Goal_Distance < Minimum_Key_Goal_Distance:
					Minimum_Key_Goal_Distance = Current_Key_Goal_Distance


				if _Room.Has != "Key":
					nKeys_Multiplier = max(nKeys_Multiplier - 1, 0)


	if nKeys_Multiplier == 0:
		return _Game.Explorers[0].Position.Get_Manhattan_Distance(Goal_Position)


	if Minimum_Explorer_Key_Distance == C_Infinity:
		Minimum_Explorer_Key_Distance = 0

	if Minimum_Key_Goal_Distance == C_Infinity:
		Minimum_Key_Goal_Distance = 0


	return Minimum_Explorer_Key_Distance * nKeys_Multiplier + Minimum_Key_Goal_Distance



# A* Algorithm
def AStar(_Game: Game, _Heuristic: Callable[[Game], int] | Callable[[Game, dict], int], _Heuristic_Parameters: dict = {}, _Greedy: bool = False, _Weight: float = 1.0) -> tuple[list[Action], int, int, float]:
	"""
	Implementation of the A* algorithm, tracks the elapsed time until reaching the Goal Room.

	Returns a list with the sequence of Actions the algorithm found to reach the Goal Room from the initial _Game, plus some other metrics.
	"""


	Initial_Time: float = time()
	Elapsed_Time: float = time() - Initial_Time
	Last_Log_Time_Step: float = Elapsed_Time


	if _Game.Has__Won():
		return [], 0, 0, Elapsed_Time,


	Counter: int = 0


	H_Cost: int = _Heuristic(_Game, _Heuristic_Parameters) if len(_Heuristic_Parameters) > 0 else _Heuristic(_Game)

	Current_Node: AStar_Queue_Node = AStar_Queue_Node(
		_Game,
		[],
		0,
		H_Cost,
		_Weight * H_Cost
	)

	Discovered_Nodes: dict[str, AStar_Discovered_Node] = {str(_Game): AStar_Discovered_Node()}

	Closed_Count: int = 0


	Open: list[AStar_Queue_Node] = []
	heapq.heappush(Open, (Current_Node.Final_Cost, Current_Node.H_Cost, Counter, Current_Node))


	while len(Open) > 0:
		Current_Node = heapq.heappop(Open)[3]
		State_String: str = str(Current_Node.State)


		if Current_Node.G_Cost > Discovered_Nodes.get(State_String, AStar_Discovered_Node(G_Cost = C_Infinity)).G_Cost:
			continue

		if Discovered_Nodes.get(State_String, AStar_Discovered_Node(Is__Closed = False)).Is__Closed:
			continue


		Elapsed_Time = time() - Initial_Time

		Discovered_Nodes[State_String].Is__Closed = True

		Closed_Count += 1


		if Elapsed_Time - Last_Log_Time_Step > 5:
			Last_Log_Time_Step = time() - Initial_Time - (time() - Initial_Time) % 5


			print(f"Visited/Discovered Nodes: {Closed_Count:,}/{len(Discovered_Nodes):,}. Time elapsed: {(Elapsed_Time):.3f} seconds, or {((Elapsed_Time) / 60):.3f} minutes, or {((Elapsed_Time) / 3600):.3f} hours.")


		if Current_Node.State.Has__Won():
			return Current_Node.Action_History, Closed_Count, len(Discovered_Nodes), Elapsed_Time


		New_Node: AStar_Queue_Node = deepcopy(Current_Node)
		New_G: int = Current_Node.G_Cost + 1 if not _Greedy else 0


		for _Action in Current_Node.State.Get_Decision_Space():
			Elapsed_Time = time() - Initial_Time


			if Elapsed_Time - Last_Log_Time_Step > 5:
				Last_Log_Time_Step = time() - Initial_Time - (time() - Initial_Time) % 5
	
	
				print(f"Visited/Discovered Nodes: {Closed_Count:,}/{len(Discovered_Nodes):,}. Time elapsed: {(Elapsed_Time):.3f} seconds, or {((Elapsed_Time) / 60):.3f} minutes, or {((Elapsed_Time) / 3600):.3f} hours.")


			New_Node.State.Execute_Action(_Action)
			New_Node.Action_History.append(_Action)

			State_String = str(New_Node.State)


			if _Greedy or New_G < Discovered_Nodes.get(State_String, AStar_Discovered_Node(G_Cost = C_Infinity)).G_Cost:
				Discovered_Nodes[State_String] = AStar_Discovered_Node(G_Cost = New_G)
				Counter += 1


				New_Node.G_Cost = New_G
				New_Node.H_Cost = _Heuristic(New_Node.State, _Heuristic_Parameters) if len(_Heuristic_Parameters) > 0 else _Heuristic(New_Node.State)
				New_Node.Final_Cost = New_Node.G_Cost + _Weight * New_Node.H_Cost


				heapq.heappush(Open, (New_Node.Final_Cost, New_Node.H_Cost, Counter, deepcopy(New_Node)))


			New_Node.State.Undo_Action(_Action)
			New_Node.Action_History.pop()


	return [], Closed_Count, len(Discovered_Nodes), time() - Initial_Time
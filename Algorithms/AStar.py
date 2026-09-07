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


# A* Algorithm
def AStar(_Game: Game, _Heuristic: Callable[[Game], int], _Weight: float = 1.0) -> tuple[list[Action], int, int, float]:
	"""
	Implementation of the A* algorithm, tracks the elapsed time until reaching the Goal Room.

	Returns a list with the sequence of Actions the algorithm found to reach the Goal Room from the initial _Game, plus some other metrics.
	"""


	Initial_Time: float = time()
	Elapsed_Time: float = time() - Initial_Time
	Last_Log_Time: float = Elapsed_Time


	if _Game.Has__Won():
		return [], 0, 0, Elapsed_Time,


	Counter: int = 0


	H_Cost: int = _Heuristic(_Game)

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


		if Elapsed_Time - Last_Log_Time > 5:
			Last_Log_Time = time() - Initial_Time


			print(f"Visited/Discovered Nodes: {Closed_Count:,}/{len(Discovered_Nodes):,}. Time elapsed: {(Elapsed_Time):.3f} seconds, or {((Elapsed_Time) / 60):.3f} minutes, or {((Elapsed_Time) / 3600):.3f} hours.")


		if Current_Node.State.Has__Won():
			return Current_Node.Action_History, Closed_Count, len(Discovered_Nodes), Elapsed_Time


		New_Node: AStar_Queue_Node = deepcopy(Current_Node)
		New_G: int = Current_Node.G_Cost + 1


		for _Action in Current_Node.State.Get_Decision_Space():
			Elapsed_Time = time() - Initial_Time


			if Elapsed_Time - Last_Log_Time > 5:
				Last_Log_Time = time() - Initial_Time
	
	
				print(f"Visited/Discovered Nodes: {Closed_Count:,}/{len(Discovered_Nodes):,}. Time elapsed: {(Elapsed_Time):.3f} seconds, or {((Elapsed_Time) / 60):.3f} minutes, or {((Elapsed_Time) / 3600):.3f} hours.")


			New_Node.State.Execute_Action(_Action)
			New_Node.Action_History.append(_Action)

			State_String = str(New_Node.State)


			if New_G < Discovered_Nodes.get(State_String, AStar_Discovered_Node(G_Cost = C_Infinity)).G_Cost:
				Discovered_Nodes[State_String] = AStar_Discovered_Node(G_Cost = New_G)
				Counter += 1


				New_Node.G_Cost = New_G
				New_Node.H_Cost = _Heuristic(New_Node.State)
				New_Node.Final_Cost = New_Node.G_Cost + _Weight * New_Node.H_Cost


				heapq.heappush(Open, (New_Node.Final_Cost, New_Node.H_Cost, Counter, deepcopy(New_Node)))


			New_Node.State.Undo_Action(_Action)
			New_Node.Action_History.pop()


	return [], Closed_Count, len(Discovered_Nodes), time() - Initial_Time
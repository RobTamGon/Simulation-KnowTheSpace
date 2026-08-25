from time import time
from dataclasses import dataclass
from copy import deepcopy

import heapq


from Game import Game, Action, Vector2
from Utility import Display__Explorer_VS_Goal


@dataclass
class AStar_Queue_Node:
	State: Game
	Action_History: list[Action]
	G_Cost: int
	H_Cost: int
	Final_Cost: int


# Gets the Manhattan distance from the Explorer to the Goal as the Heuristic Cost
def Get_Manhattan_H_Cost(_Game: Game):
	"""
	Calculates and returns the Manhattan distance from the Explorer to the Goal as the Heuristic Cost.
	"""


	Distance_Vector: Vector2 = _Game.Explorers[0].Position.Moved(_Game.Index_Goal().Position.Negated())


	return abs(Distance_Vector.x) + abs(Distance_Vector.y)


# A* Algorithm
def AStar(_Game: Game) -> tuple[list[Action], float]:
	"""
	Implementation of the A* algorithm, tracks the elapsed time until reaching the Goal Room.

	Returns a list with the sequence of Actions the algorithm found to reach the Goal Room from the initial _Game, plus some other metrics.
	"""


	Initial_Time: float = time()


	if _Game.Has__Won():
		return [], time() - Initial_Time


	Counter: int = 0


	H_Cost: int = Get_Manhattan_H_Cost(_Game)

	Current_Node: AStar_Queue_Node = AStar_Queue_Node(
		_Game,
		[],
		0,
		H_Cost,
		H_Cost
	)
	Visited_Nodes: list[AStar_Queue_Node] = []


	Queue: list[AStar_Queue_Node] = []
	heapq.heappush(Queue, (Current_Node.Final_Cost, Current_Node.H_Cost, Counter, Current_Node))


	New_Node__Is_In__Queue: bool = False


	while len(Queue) > 0:
		Current_Node = heapq.heappop(Queue)[3]
		New_Node = deepcopy(Current_Node)


		if len(Visited_Nodes) % 100 == 0:
			print(f"Visited Nodes: {len(Visited_Nodes)}. Time elapsed: {(time() - Initial_Time):.3f} seconds, or {((time() - Initial_Time) / 60):.3f} minutes, or {((time() - Initial_Time) / 3600):.3f} hours.")
		# 	Display__Explorer_VS_Goal(Current_Node.State)


		if Current_Node.State.Has__Won():
			return Current_Node.Action_History, time() - Initial_Time


		Visited_Nodes.append(Current_Node)


		for _Action in Current_Node.State.Get_Decision_Space():
			New_Node.State.Execute_Action(_Action)
			New_Node.Action_History.append(_Action)


			if not any([str(New_Node.State) == str(_Node.State) for _Node in Visited_Nodes]):
				New_Node__Is_In__Queue = False

				New_Node.G_Cost = Current_Node.G_Cost + 1
				New_Node.H_Cost = Get_Manhattan_H_Cost(New_Node.State)
				New_Node.Final_Cost = (New_Node.G_Cost + New_Node.H_Cost) * 100000 + New_Node.H_Cost


				for _Queue_Node in Queue:
					if str(_Queue_Node[3].State) == str(New_Node.State) and _Queue_Node[3].Final_Cost > New_Node.Final_Cost:
						New_Node__Is_In__Queue = True

						_Queue_Node[3].Final_Cost = (New_Node.G_Cost + _Queue_Node[3].H_Cost) * 100000 + _Queue_Node[3].H_Cost


						break


				if not New_Node__Is_In__Queue:
					Counter += 1


					New_Node.Final_Cost = (New_Node.G_Cost + New_Node.H_Cost) * 100000 + New_Node.H_Cost

					heapq.heappush(Queue, (New_Node.Final_Cost, New_Node.H_Cost, Counter, deepcopy(New_Node)))


			New_Node.State.Undo_Action(_Action)
			New_Node.Action_History.pop()
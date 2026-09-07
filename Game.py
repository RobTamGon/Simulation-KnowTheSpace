from json import load
from copy import deepcopy
from dacite import from_dict

from dataclasses import dataclass
from enum import Enum



@dataclass
class Vector2:
	x: int = 0
	y: int = 0


	# Gets the Name of the current Vector2 Direction
	def Direction_Name(self) -> str:
		"""
		Returns either "Left", "Right", "Up" or "Down" depending on the Direction of the Vector2.
		"""


		if self.x == -1:
			return "Left"
		
		if self.x == 1:
			return "Right"
		
		if self.y == -1:
			return "Up"
		
		if self.y == 1:
			return "Down"


	# Gets the Manhattan distance between the Vector2s
	def Get_Manhattan_Distance(self, _Target: "Vector2") -> int:
		"""
		Gets and returns the Manhattan distance between the Vector2s.
		"""


		return abs(_Target.x - self.x) + abs(_Target.y - self.y)


	# Adds the Translation Vector2 to the current Vector2
	def Move(self, _Translation: "Vector2") -> None:
		"""
		Updates the Vector2 to be equivalent to Vector2 + _Translation.
		"""


		self.x += _Translation.x
		self.y += _Translation.y

	# Adds the Translation Vector2 to the current Vector2
	def Moved(self, _Translation: "Vector2") -> "Vector2":
		"""
		Returns a new Vector2 equivalent to Vector2 + _Translation.
		"""


		return Vector2(self.x + _Translation.x, self.y + _Translation.y)


	# Gets the negative Vector2 (-Vector2)
	def Negated(self) -> "Vector2":
		"""
		Returns a new Vector2 equivalent to -Vector2.
		"""


		return Vector2(self.x * -1, self.y * -1)
	

	# Creates an independent copy of the Vector2
	def Copy(self) -> "Vector2":
		"""
		Creates and returns an independent copy of the Vector2.
		"""


		return Vector2(self.x, self.y)


class Direction(Enum):
	Left = Vector2(-1, 0)
	Right = Vector2(1, 0)
	Up = Vector2(0, -1)
	Down = Vector2(0, 1)



@dataclass
class Connection:
	Exists: bool
	Locked_By: str | None = None


@dataclass
class Level_Data:
	Tiles: list[list[bool]]
	Walls: dict[str, list[list[bool]]]
	Rooms: list[dict[str, str | dict[str, Connection] | None] | None]
	Explorers: list[dict[str, list[int]]]



# Loads and holds the original and static Level data
class Level:
	def __init__(self, _ID: int) -> None:
		self.ID: int = _ID
		self.Data: Level_Data = from_dict(Level_Data, load(open(f"Levels/Level {self.ID}.json", "r")))
		self.Size: Vector2 = Vector2(
			self.Data.Tiles[0].__len__(),
			self.Data.Tiles.__len__()
		)


# Piece that can Slide to another Tile
class Room:
	def __init__(self, _Initial_Position: Vector2, _Has: str, _Connections: dict[str, Connection]) -> None:
		self.Position: Vector2 = _Initial_Position
		self.Has: str = _Has
		self.Connections: dict[str, Connection] = _Connections

@dataclass
class Room_State_Data:
	Position: Vector2
	Has: str
	Connections: dict[str, Connection]

@dataclass
class Room_Exit_Undo_Data:
	Position: Vector2
	Initial_Connection_Direction: str
	Initial_Connection: Connection

@dataclass
class Room_Entry_Undo_Data:
	Position: Vector2
	Initial_Has: str
	Initial_Connection_Direction: str
	Initial_Connection: Connection


# Player character that can Move between Rooms
class Explorer:
	def __init__(self, _Initial_Position: Vector2) -> None:
		self.Position: Vector2 = _Initial_Position
		self.Keys: int = 0

@dataclass
class Explorer_State_Data:
	Position: Vector2
	Keys: int

@dataclass
class Explorer_Undo_Data:
	Initial_Position: Vector2
	Initial_Keys: int



class Action_Type(Enum):
	Room__Slide = "Room.Slide"
	Explorer__Move = "Explorer.Move"

@dataclass
class Undo_Action_Data:
	Exit_Room: Room_Exit_Undo_Data
	Entry_Room: Room_Entry_Undo_Data
	Explorer: Explorer_Undo_Data

@dataclass
class Action:
	Type: Action_Type
	Instance_Position: Vector2
	Direction: Vector2
	Undo_Data: Undo_Action_Data = None


	# Gets the Reversed Action
	def Reversed(self) -> "Action":
		"""
		Creates and returns an independent Action with Reversed Parameters.
		"""


		return Action(self.Type, self.Instance_Position.Moved(self.Direction), self.Direction.Negated())



# The main class, manipulates the dynamic Level data
class Game:
	# Loads the Level data and copies the Rooms and Explorer(s) data to dynamically change them when performing actions
	def __init__(self, _Initial_Level_ID: int) -> None:
		self.Level: Level = Level(_Initial_Level_ID)


		self.Rooms: list[list[Room | None]] = []
		Room_Count: int = 0


		for _y in range(self.Level.Size.y):
			self.Rooms.append([])

			for _x in range(self.Level.Size.x):
				if not self.Level.Data.Tiles[_y][_x]:
					self.Rooms[_y].append(None)


					continue


				self.Rooms[_y].append(Room(
					Vector2(_x, _y),
					self.Level.Data.Rooms[Room_Count]["Has"],
					self.Level.Data.Rooms[Room_Count]["Connections"]
				) if self.Level.Data.Rooms[Room_Count] else None)
				Room_Count += 1


		self.Explorers: list[Explorer] = [
			Explorer(Vector2(self.Level.Data.Explorers[i]["Position"][0], self.Level.Data.Explorers[i]["Position"][1])) for i in range(len(self.Level.Data.Explorers))
		]


	# Returns a string representing the State of the Game, containing all the Rooms and Explorers data
	def __str__(self) -> str:
		Output: dict[str, list[Room_State_Data] | list[Explorer_State_Data]] = {
			"Rooms": [],
			"Explorers": []
		}


		for _y in range(self.Level.Size.y):
			for _x in range(self.Level.Size.x):
				Output["Rooms"].append(Room_State_Data(
					self.Rooms[_y][_x].Position,
					self.Rooms[_y][_x].Has,
					self.Rooms[_y][_x].Connections
				) if self.Rooms[_y][_x] else None)

	
		for _Explorer in self.Explorers:
			Output["Explorers"].append(Explorer_State_Data(
				_Explorer.Position,
				_Explorer.Keys
			))


		return str(Output)


	# Checks and returns if the proposed Position is inside the boundaries of the Level
	def Is__In_Bounds(self, _Position: Vector2) -> bool:
		"""
		Checks and returns whether the proposed Position is inside the boundaries of the Level or not by checking the range of the Rooms grid and whether the Tile in that position is Enabled or not.
		"""


		if _Position.x < 0 or _Position.x >= self.Level.Size.x or _Position.y < 0 or _Position.y >= self.Level.Size.y:
			return False

		if not self.Level.Data.Tiles[_Position.y][_Position.x]:
			return False


		return True


	# Checks and returns if there is a Wall of the given type in the given Position
	def Is__Wall(self, _Direction_Value: int, _Wall_Type: str, _Position: Vector2):
		"""
		Checks and returns if there is a Wall of the given type in the given Position by looking at the Wall Level Data.
		"""


		return self.Level.Data.Walls[_Wall_Type][_Position.y - (1 if _Wall_Type == "Horizontal" and _Direction_Value == -1 else 0)][_Position.x - (1 if _Wall_Type == "Vertical" and _Direction_Value == -1 else 0)]


	# Checks and returns if it is possible to Slide a Room in the given Direction
	def Can__Room__Slide(self, _Room: Room, _Direction: Vector2) -> bool:
		"""
		Checks and returns if it is possible to Slide a Room in the given Direction by testing all the necessary conditions, which are:

		- The Room exists
		- There is not an Explorer in that Room
		- There is not a Wall between the Room's current Position and the target Position
		- There is not another Room in the target Position
		"""


		if _Room is None:
			return False

		for _E in self.Explorers:
			if _E.Position == _Room.Position:
				return False

		if _Direction.x != 0 and self.Is__Wall(_Direction.x, "Vertical", _Room.Position):
			return False

		if _Direction.y != 0 and self.Is__Wall(_Direction.y, "Horizontal", _Room.Position):
			return False

		if self.Rooms[_Room.Position.y + _Direction.y][_Room.Position.x + _Direction.x]:
			return False


		return True

	# Slides a Room
	def Room__Slide(self, _Room: Room, _Direction: Vector2) -> None:
		"""
		Slides a Room by swapping the data in the corresponding grid locations.
		"""


		New_Position: Vector2 = _Room.Position.Moved(_Direction)


		self.Rooms[_Room.Position.y][_Room.Position.x], self.Rooms[New_Position.y][New_Position.x] = self.Rooms[New_Position.y][New_Position.x], self.Rooms[_Room.Position.y][_Room.Position.x]
		_Room.Position = New_Position
	

	# Gets the Explorer instance that matches the given Position
	def Index_Explorer(self, _Position: Vector2) -> Explorer:
		"""
		Finds and returns the Explorer instance that matches the given Position.
		"""


		for _Explorer in self.Explorers:
			if _Explorer.Position == _Position:
				return _Explorer
		

		return None


	# Gets the Room instance that Has a Goal
	def Index_Goal(self) -> Room:
		"""
		Finds and returns the Room instance that Has a Goal.
		"""


		for _Row in self.Rooms:
			for _Room in _Row:
				if _Room is not None and _Room.Has == "Goal":
					return _Room



		return None


	# Gets the number of Keys required for an Explorer to Move in the given Direction
	def Get_Required_Keys(self, _Explorer: Explorer, _Direction: Vector2) -> int:
		"""
		Returns the number of Keys required for an Explorer to Move in the given Direction, through 2 Connections (one from the Room it's exiting and one from the Room it's entering).
		"""


		Exit_Connection: Connection = self.Rooms[_Explorer.Position.y][_Explorer.Position.x].Connections[_Direction.Direction_Name()]
		Entry_Connection: Connection = self.Rooms[_Explorer.Position.y + _Direction.y][_Explorer.Position.x + _Direction.x].Connections[_Direction.Negated().Direction_Name()]


		return (1 if Exit_Connection.Exists and Exit_Connection.Locked_By == "Key" else 0) + (1 if Entry_Connection.Exists and Entry_Connection.Locked_By == "Key" else 0)

	# Checks if it is possible to Move an Explorer in the given Direction
	def Can__Explorer__Move(self, _Explorer: Explorer, _Direction: Vector2) -> bool:
		"""
		Checks if it is possible to Move an Explorer in the given Direction by testing all the necessary conditions, which are:

		- There is another Room in the target Position
		- Both necessary Connections exist and aren't Locked by Keys, or can be Unlocked with the amount of Keys currently held by the Explorer
		- There is not a Wall between the Explorer's current Position and the target Position
		"""


		if not self.Rooms[_Explorer.Position.y + _Direction.y][_Explorer.Position.x + _Direction.x]:
			return False

		if not self.Rooms[_Explorer.Position.y][_Explorer.Position.x].Connections[_Direction.Direction_Name()].Exists or not self.Rooms[_Explorer.Position.y + _Direction.y][_Explorer.Position.x + _Direction.x].Connections[_Direction.Negated().Direction_Name()].Exists:
			return False
		
		if self.Get_Required_Keys(_Explorer, _Direction) > _Explorer.Keys:
			return False

		if _Direction.x != 0 and self.Is__Wall(_Direction.x, "Vertical", _Explorer.Position):
			return False
		
		if _Direction.y != 0 and self.Is__Wall(_Direction.y, "Horizontal", _Explorer.Position):
			return False


		return True

	# Moves an Explorer
	def Explorer__Move(self, _Explorer: Explorer, _Direction: Vector2) -> Undo_Action_Data:
		"""
		Moves an Explorer by updating its Position and the amount of held Keys.

		Returns a Dictionary with the Action's initial data, so that it can be used when undoing the Action.
		"""

		_Direction_Name: str = _Direction.Direction_Name()
		_Opposite_Direction_Name: str = _Direction.Negated().Direction_Name()

		Exit_Room: Room = self.Rooms[_Explorer.Position.y][_Explorer.Position.x]
		Entry_Room: Room = self.Rooms[_Explorer.Position.y + _Direction.y][_Explorer.Position.x + _Direction.x]


		Undo_Data: Undo_Action_Data = Undo_Action_Data(
			Room_Exit_Undo_Data(Exit_Room.Position.Copy(), _Direction_Name, deepcopy(Exit_Room.Connections[_Direction_Name])),
			Room_Entry_Undo_Data(Entry_Room.Position.Copy(), Entry_Room.Has, _Opposite_Direction_Name, deepcopy(Entry_Room.Connections[_Opposite_Direction_Name])),
			Explorer_Undo_Data(_Explorer.Position.Copy(), _Explorer.Keys)
		)


		_Explorer.Keys -= self.Get_Required_Keys(_Explorer, _Direction)

		Exit_Room.Connections[_Direction_Name].Locked_By = None
		Entry_Room.Connections[_Opposite_Direction_Name].Locked_By = None

		_Explorer.Position.Move(_Direction)


		if Entry_Room.Has == "Key":
			Entry_Room.Has = None

			_Explorer.Keys += 1
		

		return Undo_Data



	# Checks whether the Level has been beaten, which can only happen if all Explorers are inside a Room with a Goal at the same time
	def Has__Won(self) -> bool:
		"""
		Checks whether the Level has been beaten, which can only happen if all Explorers are inside a Room with a Goal at the same time.
		"""


		for _Explorer in self.Explorers:
			if self.Rooms[_Explorer.Position.y][_Explorer.Position.x].Has != "Goal":
				return False
		

		return True



	# Gets all the possible decisions in the current State of the Game
	def Get_Decision_Space(self) -> list[Action]:
		"""
		Gets the Decision Space of the current State of the Game by searching for empty Tiles and testing if any Rooms could be moved towards them, and by testing each Explorer going in each possible Direction.
		"""


		Decision_Space: list[Action] = []


		for _y in range(len(self.Rooms)):
			for _x in range(len(self.Rooms[_y])):
				if self.Rooms[_y][_x]:
					continue
				
				
				for _Direction in Direction:
					Target_Room_Position: Vector2 = _Direction.value.Negated().Moved(Vector2(_x, _y))


					if self.Is__In_Bounds(Target_Room_Position) and self.Can__Room__Slide(self.Rooms[Target_Room_Position.y][Target_Room_Position.x], _Direction.value):
						Decision_Space.append(Action(Action_Type.Room__Slide, Target_Room_Position, _Direction.value))
		

		for _Explorer in self.Explorers:
			for _Direction in Direction:
				if self.Is__In_Bounds(_Explorer.Position.Moved(_Direction.value)) and self.Can__Explorer__Move(_Explorer, _Direction.value):
					Decision_Space.append(Action(Action_Type.Explorer__Move, _Explorer.Position.Copy(), _Direction.value))
		

		return Decision_Space


	# Executes the given Action
	def Execute_Action(self, _Action: Action) -> None:
		"""
		Executes the given Action, updating its Undo Data in the process.
		"""


		match _Action.Type:
			case Action_Type.Room__Slide:
				_Action.Undo_Data = self.Room__Slide(
					self.Rooms[_Action.Instance_Position.y][_Action.Instance_Position.x],
					_Action.Direction
				)

			case Action_Type.Explorer__Move:
				_Action.Undo_Data = self.Explorer__Move(
					self.Index_Explorer(_Action.Instance_Position),
					_Action.Direction
				)

	# Undos the given Action
	def Undo_Action(self, _Action: Action) -> None:
		"""
		Undos the given Action by generating the inverse Action and performing it:

		- Sliding a Room only needs to Slide the Room in the opposite direction.
		- Moving an Explorer requires moving in the opposite direction, possibly restoring Key-Locked Connections, changing the Has property of the Entry Room, and the amount of Keys held by the Explorer.
		"""


		match _Action.Type:
			case Action_Type.Room__Slide:
				self.Room__Slide(self.Rooms[_Action.Instance_Position.y + _Action.Direction.y][_Action.Instance_Position.x + _Action.Direction.x], _Action.Direction.Negated())
			
			case Action_Type.Explorer__Move:
				self.Rooms[_Action.Undo_Data.Exit_Room.Position.y][_Action.Undo_Data.Exit_Room.Position.x].Connections[_Action.Undo_Data.Exit_Room.Initial_Connection_Direction] = _Action.Undo_Data.Exit_Room.Initial_Connection

				self.Rooms[_Action.Undo_Data.Entry_Room.Position.y][_Action.Undo_Data.Entry_Room.Position.x].Has = _Action.Undo_Data.Entry_Room.Initial_Has
				self.Rooms[_Action.Undo_Data.Entry_Room.Position.y][_Action.Undo_Data.Entry_Room.Position.x].Connections[_Action.Undo_Data.Entry_Room.Initial_Connection_Direction] = _Action.Undo_Data.Entry_Room.Initial_Connection


				_Explorer: Explorer = self.Index_Explorer(_Action.Undo_Data.Explorer.Initial_Position.Moved(_Action.Direction))
				_Explorer.Position.Move(_Action.Direction.Negated())
				_Explorer.Keys = _Action.Undo_Data.Explorer.Initial_Keys
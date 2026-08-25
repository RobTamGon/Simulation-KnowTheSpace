from Game import Game


def Display__Explorer_VS_Goal(_Game: Game):
	print("\n")


	for _Y in range(_Game.Level.Size.y):
		print("\n")


		for _X in range(_Game.Level.Size.x):
			if _Game.Explorers[0].Position.x == _X and _Game.Explorers[0].Position.y == _Y:
				print("@", end = " ")
			elif _Game.Rooms[_Y][_X] is None:
				print(" ", end = " ")
			else:
				match _Game.Rooms[_Y][_X].Has:
					case "Goal":
						print("G", end = " ")
					case "Key":
						print("K", end = " ")


					case _:
						print("·", end = " ")
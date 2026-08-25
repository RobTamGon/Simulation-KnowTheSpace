from os import remove

from dataclasses import dataclass


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
			File.close()
			
			
			if _Delete_Files:
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
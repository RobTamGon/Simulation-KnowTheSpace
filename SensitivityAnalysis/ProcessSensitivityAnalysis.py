import pandas as PD
import matplotlib.pyplot as PyPlot

from dataclasses import dataclass
from enum import Enum


from Algorithms.GeneticAlgorithm import Generation_Creation_Parameters, Crossover_Fusion_Parameters, Crossover_Fusion_Bi_BFS_Fallback_Parameters, Crossover_Fusion_Cut_And_Generation_Fallback_Parameters, Crossover_Fusion_Regeneration_Fallback_Parameters, Crossover_Fusion_Clone_Fallback_Parameters, Mutate_Random_Ending_Parameters, Mutate_Cut_And_Generation_Parameters

from SensitivityAnalysis.Utility import Sensitivity_Stats, Get__Averaged_Sensitivity_Stats


PyPlot.rcParams["figure.figsize"] = [16, 12]
PyPlot.rcParams["figure.autolayout"] = True
PyPlot.rcParams["axes.titlesize"] = 18
PyPlot.rcParams["axes.labelsize"] = 18
PyPlot.rcParams["legend.fontsize"] = 18
PyPlot.rcParams["xtick.labelsize"] = 12
PyPlot.rcParams["ytick.labelsize"] = 12


Level: int = 3
Reference_File__Name_Prefix: str = "Crossover with Bi-BFS"
Reference_Attempts__Amount: int = 3

File__Path: str = f"Logs/Genetic Algorithm/Level {Level}/Sensitivity Analysis/Output.txt"

Minimum_Success_Rate: float = 0.6


class Line_Offset(Enum):
	Start = 7
	Entry_Start = 2

	Search_Start_Percent = 0
	Search_End_Percent = 1


	Crossover_Fallback_Version = 2

	Crossover_Fusion_Bi_BFS__Max__Depth = 3
	Crossover_Fusion_Bi_BFS__Mutation_Version_Base = 4

	Crossover_Fusion_Cut_And_Generation__Random_Cut_Start_Percent = 4
	Crossover_Fusion_Cut_And_Generation__Last_Actions_To_Change = 5
	Crossover_Fusion_Cut_And_Generation__Mutation_Version_Base = 6

	Crossover_Fusion_Regeneration__Generation__Size = 4
	Crossover_Fusion_Regeneration__Actions__Amount = 5
	Crossover_Fusion_Regeneration__Mutation_Version_Base = 6

	Crossover_Fusion_Clone__Mutation_Version_Base = 3


	Mutation_Random_Ending__New_Actions__Amount = 1
	Mutation_Cut_And_Generation__Random_Cut_Start_Percent = 1
	Mutation_Cut_And_Generation__Last_Actions_To_Change = 2


	Changed_Parameter = 1
	Average_Action_History_Length = 2
	Average_Elapsed_Time = 3
	Attempts = 4

class Text_Offset(Enum):
	Search_Start_Percent = len("- Search_Start_Percent: ")
	Search_End_Percent = len("- Search_End_Percent: ")

	Parameter_Starter = "-"


	Crossover_Fallback_Version = len("- Fallback_Parameters: Crossover Fallback Version: ")
	Crossover_Fallback_Version_Separator = "."

	Crossover_Fusion_Bi_BFS__Max__Depth = len("- Max__Depth: ")

	Crossover_Fusion_Cut_And_Generation__Random_Cut_Start_Percent = len("- Random_Cut_Start_Percent: ")
	Crossover_Fusion_Cut_And_Generation__Last_Actions_To_Change = len("- Last_Actions_To_Change: ")

	Crossover_Fusion_Regeneration__Generation__Size = len("- Generation__Size: ")
	Crossover_Fusion_Regeneration__Actions__Amount = len("- Actions__Amount: ")


	Mutation_Version = len("Mutation Version: ")
	Mutation_Version_Separator = "."

	Mutation_Random_Ending__New_Actions__Amount = len("- New_Actions__Amount: ")
	Mutation_Cut_And_Generation__Random_Cut_Start_Percent = len("- Random_Cut_Start_Percent: ")
	Mutation_Cut_And_Generation__Last_Actions_To_Change = len("- Last_Actions_To_Change: ")


	Changed_Parameter_Starter = len("And changing ")
	Changed_Parameter_Terminator = " from "
	Changed_Parameter_Terminator_Length = len(Changed_Parameter_Terminator)
	Changed_Parameter_Separator = " to "

	Average_Action_History_Length_Starter = len("Average Action history length: ")
	Average_Action_History_Length_Terminator = " actions"

	Average_Elapsed_Time_Starter = len("Average elapsed time: ")
	Average_Elapsed_Time_Terminator = " seconds"


	Failed_Attempts_Starter = len("Failed ")
	Failed_Attempts_Terminator = " attempts."
	Failed_Attempts_Separator = "/"

	No_Failed_Attempts_Starter = len("No failed attempts out of ")
	No_Failed_Attempts_Terminator = " total."


@dataclass
class Analysis_Entry:
	Crossover_Version: Crossover_Fusion_Parameters
	Crossover_Fallback_Version_Name: str
	Mutation_Version: Mutate_Random_Ending_Parameters | Mutate_Cut_And_Generation_Parameters
	Mutation_Version_Name: str
	Changed_Parameter_Name: str
	Changed_Parameter_FromTo: tuple[int, int] | tuple[float, float]
	Stats: Sensitivity_Stats


@dataclass
class Analysis_Parameter_Data:
	Crossover_Fallback_Version_Name: str
	Mutation_Version_Name: str
	Changed_Parameter_Name: str
	Changed_Parameter_FromsTos: list[tuple[int, int] | tuple[float, float]]
	Stats_List: list[Sensitivity_Stats]

@dataclass
class Analysis_Best_Parameter_Data:
	Crossover_Fallback_Version_Name: str
	Mutation_Version_Name: str
	Changed_Parameter_Names: list[str]
	Changed_Parameter_FromsTos: list[tuple[int, int] | tuple[float, float]]
	Stats_List: list[Sensitivity_Stats]

@dataclass
class Analysis_Best_Method_Data:
	Crossover_Fallback_Version_Names: list[str]
	Mutation_Version_Names: list[str]
	Changed_Parameter_Names: list[str]
	Changed_Parameter_FromsTos: list[tuple[int, int] | tuple[float, float]]
	Stats_List: list[Sensitivity_Stats]


# Gets and returns the Mutation Version and Parameters, as well as the changed Parameter and the results of trying the Genetic Algorithm with that change from the given output Entry
def Get__Entry_Post_Crossover_Data(_Entry_Text: list[str], _Crossover_Fusion_Fallback__Mutation_Version_Base_Line_Offset: int) -> tuple[Mutate_Random_Ending_Parameters | Mutate_Cut_And_Generation_Parameters, str, str, tuple[int | float, int | float], Sensitivity_Stats]:
	"""
	Gets and returns the Mutation Version and Parameters, as well as the changed Parameter and the results of trying the Genetic Algorithm with that change from the given output Entry.
	"""


	Mutation_Version_Name: str = _Entry_Text[_Crossover_Fusion_Fallback__Mutation_Version_Base_Line_Offset][Text_Offset.Mutation_Version.value : _Entry_Text[_Crossover_Fusion_Fallback__Mutation_Version_Base_Line_Offset].find(Text_Offset.Mutation_Version_Separator.value)]


	match Mutation_Version_Name:
		case "Random Ending":
			New_Actions__Amount_Entry_Line: str = _Entry_Text[_Crossover_Fusion_Fallback__Mutation_Version_Base_Line_Offset + Line_Offset.Mutation_Random_Ending__New_Actions__Amount.value]

			Changed_Parameter_Entry_Line: str = _Entry_Text[_Crossover_Fusion_Fallback__Mutation_Version_Base_Line_Offset + Line_Offset.Mutation_Random_Ending__New_Actions__Amount.value + Line_Offset.Changed_Parameter.value]
			Average_Action_History_Length_Entry_Line: str = _Entry_Text[_Crossover_Fusion_Fallback__Mutation_Version_Base_Line_Offset + Line_Offset.Mutation_Random_Ending__New_Actions__Amount.value + Line_Offset.Average_Action_History_Length.value]
			Average_Elapsed_Time_Entry_Line: str = _Entry_Text[_Crossover_Fusion_Fallback__Mutation_Version_Base_Line_Offset + Line_Offset.Mutation_Random_Ending__New_Actions__Amount.value + Line_Offset.Average_Elapsed_Time.value]
			Attempts_Entry_Line: str = _Entry_Text[_Crossover_Fusion_Fallback__Mutation_Version_Base_Line_Offset + Line_Offset.Mutation_Random_Ending__New_Actions__Amount.value + Line_Offset.Attempts.value]

			Changed_Parameter_FromTo: list[str] = Changed_Parameter_Entry_Line[Changed_Parameter_Entry_Line.find(Text_Offset.Changed_Parameter_Terminator.value) + Text_Offset.Changed_Parameter_Terminator_Length.value : len(Changed_Parameter_Entry_Line) - 2].split(Text_Offset.Changed_Parameter_Separator.value)

			Failed_Any_Attempt: bool = Text_Offset.Failed_Attempts_Separator.value in Attempts_Entry_Line
			Attempts: tuple[int, int] = (
				int(Attempts_Entry_Line[Text_Offset.Failed_Attempts_Starter.value : Attempts_Entry_Line.find(Text_Offset.Failed_Attempts_Separator.value)]),
				int(Attempts_Entry_Line[Attempts_Entry_Line.find(Text_Offset.Failed_Attempts_Separator.value) + 1 : Attempts_Entry_Line.find(Text_Offset.Failed_Attempts_Terminator.value)])
			) if Failed_Any_Attempt else (
				0, int(Attempts_Entry_Line[Text_Offset.No_Failed_Attempts_Starter.value : Attempts_Entry_Line.find(Text_Offset.No_Failed_Attempts_Terminator.value)])
			)


			return (
				Mutate_Random_Ending_Parameters(
					New_Actions__Amount = int(New_Actions__Amount_Entry_Line[Text_Offset.Mutation_Random_Ending__New_Actions__Amount.value + New_Actions__Amount_Entry_Line.find(Text_Offset.Parameter_Starter.value) :])
				),
				Mutation_Version_Name,
				Changed_Parameter_Entry_Line[Text_Offset.Changed_Parameter_Starter.value : Changed_Parameter_Entry_Line.find(Text_Offset.Changed_Parameter_Terminator.value)],
				(int(Changed_Parameter_FromTo[0]), int(Changed_Parameter_FromTo[1])) if Changed_Parameter_FromTo[0].isdigit() else (float(Changed_Parameter_FromTo[0]), float(Changed_Parameter_FromTo[1])),
				Sensitivity_Stats(
					Average_Action_History__Length = float(Average_Action_History_Length_Entry_Line[Text_Offset.Average_Action_History_Length_Starter.value : Average_Action_History_Length_Entry_Line.find(Text_Offset.Average_Action_History_Length_Terminator.value)]),
					Average_Elapsed_Time = float(Average_Elapsed_Time_Entry_Line[Text_Offset.Average_Elapsed_Time_Starter.value : Average_Elapsed_Time_Entry_Line.find(Text_Offset.Average_Elapsed_Time_Terminator.value)]),
					Failed_Attempts = Attempts[0],
					Total_Attempts = Attempts[1]
				)
			)
		case "Cut and Generation":
			Default_Cut_And_Generation: Mutate_Cut_And_Generation_Parameters = Mutate_Cut_And_Generation_Parameters()

			Random_Cut_Start_Percent_Entry_Line: str = _Entry_Text[_Crossover_Fusion_Fallback__Mutation_Version_Base_Line_Offset + Line_Offset.Mutation_Cut_And_Generation__Random_Cut_Start_Percent.value]
			Last_Actions_To_Change_Entry_Line: str = _Entry_Text[_Crossover_Fusion_Fallback__Mutation_Version_Base_Line_Offset + Line_Offset.Mutation_Cut_And_Generation__Last_Actions_To_Change.value]

			Random_Cut_Start_Percent: float = float(Random_Cut_Start_Percent_Entry_Line[Text_Offset.Mutation_Cut_And_Generation__Random_Cut_Start_Percent.value + Random_Cut_Start_Percent_Entry_Line.find(Text_Offset.Parameter_Starter.value) :])
			Last_Actions_To_Change: int = int(Last_Actions_To_Change_Entry_Line[Text_Offset.Mutation_Cut_And_Generation__Last_Actions_To_Change.value + Last_Actions_To_Change_Entry_Line.find(Text_Offset.Parameter_Starter.value) :])


			if Random_Cut_Start_Percent != Default_Cut_And_Generation.Random_Cut_Start_Percent:
				Mutation_Version_Name = f"{Mutation_Version_Name} - Random Cut"
			else:
				Mutation_Version_Name = f"{Mutation_Version_Name} - Last Actions"


			Changed_Parameter_Entry_Line: str = _Entry_Text[_Crossover_Fusion_Fallback__Mutation_Version_Base_Line_Offset + Line_Offset.Mutation_Cut_And_Generation__Last_Actions_To_Change.value + Line_Offset.Changed_Parameter.value]
			Average_Action_History_Length_Entry_Line: str = _Entry_Text[_Crossover_Fusion_Fallback__Mutation_Version_Base_Line_Offset + Line_Offset.Mutation_Cut_And_Generation__Last_Actions_To_Change.value + Line_Offset.Average_Action_History_Length.value]
			Average_Elapsed_Time_Entry_Line: str = _Entry_Text[_Crossover_Fusion_Fallback__Mutation_Version_Base_Line_Offset + Line_Offset.Mutation_Cut_And_Generation__Last_Actions_To_Change.value + Line_Offset.Average_Elapsed_Time.value]
			Attempts_Entry_Line: str = _Entry_Text[_Crossover_Fusion_Fallback__Mutation_Version_Base_Line_Offset + Line_Offset.Mutation_Cut_And_Generation__Last_Actions_To_Change.value + Line_Offset.Attempts.value]

			Changed_Parameter_FromTo: list[str] = Changed_Parameter_Entry_Line[Changed_Parameter_Entry_Line.find(Text_Offset.Changed_Parameter_Terminator.value) + Text_Offset.Changed_Parameter_Terminator_Length.value : len(Changed_Parameter_Entry_Line) - 2].split(Text_Offset.Changed_Parameter_Separator.value)

			Failed_Any_Attempt: bool = Text_Offset.Failed_Attempts_Separator.value in Attempts_Entry_Line
			Attempts: tuple[int, int] = (
				int(Attempts_Entry_Line[Text_Offset.Failed_Attempts_Starter.value : Attempts_Entry_Line.find(Text_Offset.Failed_Attempts_Separator.value)]),
				int(Attempts_Entry_Line[Attempts_Entry_Line.find(Text_Offset.Failed_Attempts_Separator.value) + 1 : Attempts_Entry_Line.find(Text_Offset.Failed_Attempts_Terminator.value)])
			) if Failed_Any_Attempt else (
				0, int(Attempts_Entry_Line[Text_Offset.No_Failed_Attempts_Starter.value : Attempts_Entry_Line.find(Text_Offset.No_Failed_Attempts_Terminator.value)])
			)


			return (
				Mutate_Cut_And_Generation_Parameters(
					Random_Cut_Start_Percent = Random_Cut_Start_Percent,
					Last_Actions_To_Change = Last_Actions_To_Change
				),
				Mutation_Version_Name,
				Changed_Parameter_Entry_Line[Text_Offset.Changed_Parameter_Starter.value : Changed_Parameter_Entry_Line.find(Text_Offset.Changed_Parameter_Terminator.value)],
				((int(Changed_Parameter_FromTo[0]), int(Changed_Parameter_FromTo[1])) if Changed_Parameter_FromTo[0].isdigit() else (float(Changed_Parameter_FromTo[0]), float(Changed_Parameter_FromTo[1]))),
				Sensitivity_Stats(
					Average_Action_History__Length = float(Average_Action_History_Length_Entry_Line[Text_Offset.Average_Action_History_Length_Starter.value : Average_Action_History_Length_Entry_Line.find(Text_Offset.Average_Action_History_Length_Terminator.value)]),
					Average_Elapsed_Time = float(Average_Elapsed_Time_Entry_Line[Text_Offset.Average_Elapsed_Time_Starter.value : Average_Elapsed_Time_Entry_Line.find(Text_Offset.Average_Elapsed_Time_Terminator.value)]),
					Failed_Attempts = Attempts[0],
					Total_Attempts = Attempts[1]
				)
			)

# Parses the given Sensitivity Analysis Output File and extracts the individual Entries within it
def Parse__Analysis(_File__Path: str) -> list[Analysis_Entry]:
	"""
	Parses the given Sensitivity Analysis Output File and extracts and returns the individual Entries within it.
	"""


	Entries: list[Analysis_Entry] = []


	with open(_File__Path, "r") as File:
		Lines: list[str] = File.readlines()[Line_Offset.Start.value :]


	while len(Lines) > 0:
		Separator__Index: int = Lines.index("\n")
		Entry_Text: list[str] = Lines[Line_Offset.Entry_Start.value : Separator__Index]

		Lines = Lines[Separator__Index + 1 :]

		Search_Start_Percent: float = float(Entry_Text[Line_Offset.Search_Start_Percent.value][Text_Offset.Search_Start_Percent.value :])
		Search_End_Percent: float = float(Entry_Text[Line_Offset.Search_End_Percent.value][Text_Offset.Search_End_Percent.value :])

		Crossover_Fallback_Version: Crossover_Fusion_Bi_BFS_Fallback_Parameters | Crossover_Fusion_Cut_And_Generation_Fallback_Parameters | Crossover_Fusion_Regeneration_Fallback_Parameters | Crossover_Fusion_Clone_Fallback_Parameters | None = None
		Crossover_Fallback_Version_Name: str = Entry_Text[Line_Offset.Crossover_Fallback_Version.value][Text_Offset.Crossover_Fallback_Version.value : Entry_Text[Line_Offset.Crossover_Fallback_Version.value].find(Text_Offset.Crossover_Fallback_Version_Separator.value)]
		Mutation_Version: Mutate_Random_Ending_Parameters | Mutate_Cut_And_Generation_Parameters | str = ""

		Changed_Parameter_Name: str = ""
		Changed_Parameter_FromTo: tuple[int | float, int | float] = (0, 0)
		Stats: Sensitivity_Stats = Sensitivity_Stats()



		match Crossover_Fallback_Version_Name:
			case "Bi-BFS":
				Max__Depth_Entry_Line: str = Entry_Text[Line_Offset.Crossover_Fusion_Bi_BFS__Max__Depth.value]

				Crossover_Fallback_Version = Crossover_Fusion_Bi_BFS_Fallback_Parameters(
					Max__Depth = int(Max__Depth_Entry_Line[Text_Offset.Crossover_Fusion_Bi_BFS__Max__Depth.value + Max__Depth_Entry_Line.find(Text_Offset.Parameter_Starter.value) :])
				)

				Mutation_Version, Mutation_Version_Name, Changed_Parameter_Name, Changed_Parameter_FromTo, Stats = Get__Entry_Post_Crossover_Data(Entry_Text, Line_Offset.Crossover_Fusion_Bi_BFS__Mutation_Version_Base.value)
			case "Cut and Generation":
				Default_Cut_And_Generation: Mutate_Cut_And_Generation_Parameters = Mutate_Cut_And_Generation_Parameters()

				Random_Cut_Start_Percent_Entry_Line: str = Entry_Text[Line_Offset.Crossover_Fusion_Cut_And_Generation__Random_Cut_Start_Percent.value]
				Last_Actions_To_Change_Entry_Line: str = Entry_Text[Line_Offset.Crossover_Fusion_Cut_And_Generation__Last_Actions_To_Change.value]

				Random_Cut_Start_Percent: float = float(Random_Cut_Start_Percent_Entry_Line[Text_Offset.Crossover_Fusion_Cut_And_Generation__Random_Cut_Start_Percent.value + Random_Cut_Start_Percent_Entry_Line.find(Text_Offset.Parameter_Starter.value) :])
				Last_Actions_To_Change: int = int(Last_Actions_To_Change_Entry_Line[Text_Offset.Crossover_Fusion_Cut_And_Generation__Last_Actions_To_Change.value + Last_Actions_To_Change_Entry_Line.find(Text_Offset.Parameter_Starter.value) :])

				if Random_Cut_Start_Percent != Default_Cut_And_Generation.Random_Cut_Start_Percent:
					Crossover_Fallback_Version_Name = f"{Crossover_Fallback_Version_Name} - Random Cut"
				else:
					Crossover_Fallback_Version_Name = f"{Crossover_Fallback_Version_Name} - Last Actions"


				Crossover_Fallback_Version = Crossover_Fusion_Cut_And_Generation_Fallback_Parameters(
					Mutate_Cut_And_Generation_Parameters(
						Random_Cut_Start_Percent = Random_Cut_Start_Percent,
						Last_Actions_To_Change = Last_Actions_To_Change
					)
				)

				Mutation_Version, Mutation_Version_Name, Changed_Parameter_Name, Changed_Parameter_FromTo, Stats = Get__Entry_Post_Crossover_Data(Entry_Text, Line_Offset.Crossover_Fusion_Cut_And_Generation__Mutation_Version_Base.value)
			case "Regeneration":
				Generation__Size_Entry_Line: str = Entry_Text[Line_Offset.Crossover_Fusion_Regeneration__Generation__Size.value]
				Actions__Amount_Entry_Lines: str = Entry_Text[Line_Offset.Crossover_Fusion_Regeneration__Actions__Amount.value]

				Crossover_Fallback_Version = Crossover_Fusion_Regeneration_Fallback_Parameters(
					Generation_Parameters = Generation_Creation_Parameters(
						Generation__Size = int(Generation__Size_Entry_Line[Text_Offset.Crossover_Fusion_Regeneration__Generation__Size.value + Generation__Size_Entry_Line.find(Text_Offset.Parameter_Starter.value) :]),
						Actions__Amount = int(Actions__Amount_Entry_Lines[Text_Offset.Crossover_Fusion_Regeneration__Actions__Amount.value + Actions__Amount_Entry_Lines.find(Text_Offset.Parameter_Starter.value) :])
					)
				)

				Mutation_Version, Mutation_Version_Name, Changed_Parameter_Name, Changed_Parameter_FromTo, Stats = Get__Entry_Post_Crossover_Data(Entry_Text, Line_Offset.Crossover_Fusion_Regeneration__Mutation_Version_Base.value)
			case "Clone":
				Crossover_Fallback_Version = Crossover_Fusion_Clone_Fallback_Parameters()

				Mutation_Version, Mutation_Version_Name, Changed_Parameter_Name, Changed_Parameter_FromTo, Stats = Get__Entry_Post_Crossover_Data(Entry_Text, Line_Offset.Crossover_Fusion_Clone__Mutation_Version_Base.value)


		#TEMPORARY FIX UNTIL Get__Averaged_Sensitivity_Stats GETS FIXED WITH THE AVERAGE CALCULATIONS (SEE TO DO LIST)
		Stats.Average_Action_History__Length = 0 if Stats.Total_Attempts == Stats.Failed_Attempts else (Stats.Average_Action_History__Length * Stats.Total_Attempts) / (Stats.Total_Attempts - Stats.Failed_Attempts)
		Stats.Average_Elapsed_Time = 0 if Stats.Total_Attempts == Stats.Failed_Attempts else (Stats.Average_Elapsed_Time * Stats.Total_Attempts) / (Stats.Total_Attempts - Stats.Failed_Attempts)


		Entries.append(Analysis_Entry(
			Crossover_Version = Crossover_Fusion_Parameters(
				Search_Start_Percent = Search_Start_Percent,
				Search_End_Percent = Search_End_Percent,
				Fallback_Parameters = Crossover_Fallback_Version
			),
			Crossover_Fallback_Version_Name = Crossover_Fallback_Version_Name,
			Mutation_Version = Mutation_Version,
			Mutation_Version_Name = Mutation_Version_Name,
			Changed_Parameter_Name = Changed_Parameter_Name,
			Changed_Parameter_FromTo = Changed_Parameter_FromTo,
			Stats = Stats
		))


	return Entries



# [CONTINUE COMMENTING FROM HERE ON ↓]
Level_Sensitivity_Stats: Sensitivity_Stats = Get__Averaged_Sensitivity_Stats(Level, Reference_File__Name_Prefix, Reference_Attempts__Amount)

Entries: list[Analysis_Entry] = Parse__Analysis(File__Path)


Parameter_Groups: list[Analysis_Parameter_Data] = []

Action_Best_Parameter_Groups: list[Analysis_Best_Parameter_Data] = []
Time_Best_Parameter_Groups: list[Analysis_Best_Parameter_Data] = []

Action_Best_Method_Group: Analysis_Best_Method_Data = Analysis_Best_Method_Data(
	Crossover_Fallback_Version_Names = [],
	Mutation_Version_Names = [],
	Changed_Parameter_Names = [],
	Changed_Parameter_FromsTos = [],
	Stats_List = []
)
Time_Best_Method_Group: Analysis_Best_Method_Data = Analysis_Best_Method_Data(
	Crossover_Fallback_Version_Names = [],
	Mutation_Version_Names = [],
	Changed_Parameter_Names = [],
	Changed_Parameter_FromsTos = [],
	Stats_List = []
)

Best_Of_Both_Criteria: Analysis_Best_Method_Data = Analysis_Best_Method_Data(
	Crossover_Fallback_Version_Names = [],
	Mutation_Version_Names = [],
	Changed_Parameter_Names = [],
	Changed_Parameter_FromsTos = [],
	Stats_List = []
)


for _Entry in Entries:
	if len(Parameter_Groups) == 0 or _Entry.Crossover_Fallback_Version_Name != Parameter_Groups[-1].Crossover_Fallback_Version_Name or _Entry.Mutation_Version_Name != Parameter_Groups[-1].Mutation_Version_Name or _Entry.Changed_Parameter_Name != Parameter_Groups[-1].Changed_Parameter_Name:
		Parameter_Groups.append(Analysis_Parameter_Data(
			Crossover_Fallback_Version_Name = _Entry.Crossover_Fallback_Version_Name,
			Mutation_Version_Name = _Entry.Mutation_Version_Name,
			Changed_Parameter_Name = _Entry.Changed_Parameter_Name,
			Changed_Parameter_FromsTos = [_Entry.Changed_Parameter_FromTo],
			Stats_List = [_Entry.Stats]
		))
	else:
		Parameter_Groups[-1].Changed_Parameter_FromsTos.append(_Entry.Changed_Parameter_FromTo)
		Parameter_Groups[-1].Stats_List.append(_Entry.Stats)


	if 1 - (_Entry.Stats.Failed_Attempts / _Entry.Stats.Total_Attempts) >= Minimum_Success_Rate:
		if len(Action_Best_Parameter_Groups) == 0 or _Entry.Crossover_Fallback_Version_Name != Action_Best_Parameter_Groups[-1].Crossover_Fallback_Version_Name or _Entry.Mutation_Version_Name != Action_Best_Parameter_Groups[-1].Mutation_Version_Name:
			Action_Best_Parameter_Groups.append(Analysis_Best_Parameter_Data(
				Crossover_Fallback_Version_Name = _Entry.Crossover_Fallback_Version_Name,
				Mutation_Version_Name = _Entry.Mutation_Version_Name,
				Changed_Parameter_Names = [_Entry.Changed_Parameter_Name],
				Changed_Parameter_FromsTos = [_Entry.Changed_Parameter_FromTo],
				Stats_List = [_Entry.Stats]
			))
		elif _Entry.Changed_Parameter_Name != Action_Best_Parameter_Groups[-1].Changed_Parameter_Names[-1]:
			Action_Best_Parameter_Groups[-1].Changed_Parameter_Names.append(_Entry.Changed_Parameter_Name)
			Action_Best_Parameter_Groups[-1].Changed_Parameter_FromsTos.append(_Entry.Changed_Parameter_FromTo)
			Action_Best_Parameter_Groups[-1].Stats_List.append(_Entry.Stats)
		elif _Entry.Stats.Average_Action_History__Length < Action_Best_Parameter_Groups[-1].Stats_List[-1].Average_Action_History__Length:
			Action_Best_Parameter_Groups[-1].Changed_Parameter_FromsTos[-1] = _Entry.Changed_Parameter_FromTo
			Action_Best_Parameter_Groups[-1].Stats_List[-1] = _Entry.Stats

		if len(Time_Best_Parameter_Groups) == 0 or _Entry.Crossover_Fallback_Version_Name != Time_Best_Parameter_Groups[-1].Crossover_Fallback_Version_Name or _Entry.Mutation_Version_Name != Time_Best_Parameter_Groups[-1].Mutation_Version_Name:
			Time_Best_Parameter_Groups.append(Analysis_Best_Parameter_Data(
				Crossover_Fallback_Version_Name = _Entry.Crossover_Fallback_Version_Name,
				Mutation_Version_Name = _Entry.Mutation_Version_Name,
				Changed_Parameter_Names = [_Entry.Changed_Parameter_Name],
				Changed_Parameter_FromsTos = [_Entry.Changed_Parameter_FromTo],
				Stats_List = [_Entry.Stats]
			))
		elif _Entry.Changed_Parameter_Name != Time_Best_Parameter_Groups[-1].Changed_Parameter_Names[-1]:
			Time_Best_Parameter_Groups[-1].Changed_Parameter_Names.append(_Entry.Changed_Parameter_Name)
			Time_Best_Parameter_Groups[-1].Changed_Parameter_FromsTos.append(_Entry.Changed_Parameter_FromTo)
			Time_Best_Parameter_Groups[-1].Stats_List.append(_Entry.Stats)
		elif _Entry.Stats.Average_Elapsed_Time < Time_Best_Parameter_Groups[-1].Stats_List[-1].Average_Elapsed_Time:
			Time_Best_Parameter_Groups[-1].Changed_Parameter_FromsTos[-1] = _Entry.Changed_Parameter_FromTo
			Time_Best_Parameter_Groups[-1].Stats_List[-1] = _Entry.Stats

for _Group in Action_Best_Parameter_Groups:
	Action_Best_Method_Group.Crossover_Fallback_Version_Names.append(_Group.Crossover_Fallback_Version_Name)
	Action_Best_Method_Group.Mutation_Version_Names.append(_Group.Mutation_Version_Name)
	Action_Best_Method_Group.Changed_Parameter_Names.append(_Group.Changed_Parameter_Names[0])
	Action_Best_Method_Group.Changed_Parameter_FromsTos.append(_Group.Changed_Parameter_FromsTos[0])
	Action_Best_Method_Group.Stats_List.append(_Group.Stats_List[0])


	for i in range(1, len(_Group.Stats_List)):
		if _Group.Stats_List[i].Average_Action_History__Length < Action_Best_Method_Group.Stats_List[-1].Average_Action_History__Length:
			Action_Best_Method_Group.Changed_Parameter_Names[-1] = _Group.Changed_Parameter_Names[i]
			Action_Best_Method_Group.Changed_Parameter_FromsTos[-1] = _Group.Changed_Parameter_FromsTos[i]
			Action_Best_Method_Group.Stats_List[-1] = _Group.Stats_List[i]

for _Group in Time_Best_Parameter_Groups:
	Time_Best_Method_Group.Crossover_Fallback_Version_Names.append(_Group.Crossover_Fallback_Version_Name)
	Time_Best_Method_Group.Mutation_Version_Names.append(_Group.Mutation_Version_Name)
	Time_Best_Method_Group.Changed_Parameter_Names.append(_Group.Changed_Parameter_Names[0])
	Time_Best_Method_Group.Changed_Parameter_FromsTos.append(_Group.Changed_Parameter_FromsTos[0])
	Time_Best_Method_Group.Stats_List.append(_Group.Stats_List[0])


	for i in range(1, len(_Group.Stats_List)):
		if _Group.Stats_List[i].Average_Action_History__Length < Time_Best_Method_Group.Stats_List[-1].Average_Action_History__Length:
			Time_Best_Method_Group.Changed_Parameter_Names[-1] = _Group.Changed_Parameter_Names[i]
			Time_Best_Method_Group.Changed_Parameter_FromsTos[-1] = _Group.Changed_Parameter_FromsTos[i]
			Time_Best_Method_Group.Stats_List[-1] = _Group.Stats_List[i]

for _Group in [Action_Best_Method_Group, Time_Best_Method_Group]:
	Best_Of_Both_Criteria.Crossover_Fallback_Version_Names.append(_Group.Crossover_Fallback_Version_Names[0])
	Best_Of_Both_Criteria.Mutation_Version_Names.append(_Group.Mutation_Version_Names[0])
	Best_Of_Both_Criteria.Changed_Parameter_Names.append(_Group.Changed_Parameter_Names[0])
	Best_Of_Both_Criteria.Changed_Parameter_FromsTos.append(_Group.Changed_Parameter_FromsTos[0])
	Best_Of_Both_Criteria.Stats_List.append(_Group.Stats_List[0])


	for i in range(1, len(_Group.Stats_List)):
		if (_Group.Stats_List[i].Average_Action_History__Length < Best_Of_Both_Criteria.Stats_List[-1].Average_Action_History__Length) if _Group is Action_Best_Method_Group else (_Group.Stats_List[i].Average_Elapsed_Time < Best_Of_Both_Criteria.Stats_List[-1].Average_Elapsed_Time):
			Best_Of_Both_Criteria.Crossover_Fallback_Version_Names[-1] = _Group.Crossover_Fallback_Version_Names[i]
			Best_Of_Both_Criteria.Mutation_Version_Names[-1] = _Group.Mutation_Version_Names[i]
			Best_Of_Both_Criteria.Changed_Parameter_Names[-1] = _Group.Changed_Parameter_Names[i]
			Best_Of_Both_Criteria.Changed_Parameter_FromsTos[-1] = _Group.Changed_Parameter_FromsTos[i]
			Best_Of_Both_Criteria.Stats_List[-1] = _Group.Stats_List[i]
		

for _Group in Parameter_Groups:
	Parameter_Data_Frame: PD.DataFrame = PD.DataFrame(
		[[
			f"{_Group.Changed_Parameter_FromsTos[i][1]} ({_Group.Stats_List[i].Total_Attempts - _Group.Stats_List[i].Failed_Attempts}/{_Group.Stats_List[i].Total_Attempts})",
			_Group.Stats_List[i].Average_Action_History__Length,
			_Group.Stats_List[i].Average_Elapsed_Time
		] for i in range(len(_Group.Stats_List))],
		columns = [
			f"New\n[{_Group.Changed_Parameter_Name}]\nValues (Successful / Total attempts)",
			"Average Action Amount",
			"Average Elapsed Time (Seconds)"
		]
	)

	Plot = Parameter_Data_Frame.plot(
		x = Parameter_Data_Frame.columns[0],
		kind = "bar",
		stacked = False,
		secondary_y = Parameter_Data_Frame.columns[2],
		mark_right = False,
		legend = False
	)

	Handles_Left, Labels_Left = Plot.get_legend_handles_labels()
	Handles_Right, Labels_Right = Plot.right_ax.get_legend_handles_labels()


	Plot.set_title(f"Combination of [{_Group.Crossover_Fallback_Version_Name}] Crossover Fallback Version\nand [{_Group.Mutation_Version_Name}] Mutation Version\nChanging\n[{_Group.Changed_Parameter_Name}]\nfrom nominal value: [{_Group.Changed_Parameter_FromsTos[0][0]}]")
	Plot.right_ax.legend(Handles_Left + Handles_Right, Labels_Left + Labels_Right, loc = "upper right")
	Plot.set_ylabel("Actions")
	Plot.right_ax.set_ylabel("Time (Seconds)")
	Plot.locator_params("y", integer = True)
	Plot.right_ax.locator_params("y", integer = True)
	Plot.get_figure().savefig(f"SensitivityAnalysis/Graphs/Level 3/Raw/Combination of [{_Group.Crossover_Fallback_Version_Name}] and [{_Group.Mutation_Version_Name}] - Changing [{_Group.Changed_Parameter_Name}] from [{_Group.Changed_Parameter_FromsTos[0][0]}].png")

	PyPlot.close()


	print(f"Finished: Combination of [{_Group.Crossover_Fallback_Version_Name}] and [{_Group.Mutation_Version_Name}] - Changing [{_Group.Changed_Parameter_Name}] from [{_Group.Changed_Parameter_FromsTos[0][0]}]")

for _Group in Action_Best_Parameter_Groups:
	Action_Best_Parameter_Data_Frame: PD.DataFrame = PD.DataFrame(
		[[f"{_Group.Changed_Parameter_Names[i].split(".")[-1]} = {_Group.Changed_Parameter_FromsTos[i][1]} ({_Group.Stats_List[i].Total_Attempts - _Group.Stats_List[i].Failed_Attempts}/{_Group.Stats_List[i].Total_Attempts})",
			_Group.Stats_List[i].Average_Action_History__Length,
			_Group.Stats_List[i].Average_Elapsed_Time
		] for i in range(len(_Group.Stats_List))],
		columns = [
			"Action Best Parameter Values (Successful / Total attempts)",
			"Average Action Amount",
			"Average Elapsed Time (Seconds)"
		]
	)

	Plot = Action_Best_Parameter_Data_Frame.plot(
		x = Action_Best_Parameter_Data_Frame.columns[0],
		kind = "bar",
		stacked = False,
		secondary_y = Action_Best_Parameter_Data_Frame.columns[2],
		mark_right = False,
		legend = False
	)

	Handles_Left, Labels_Left = Plot.get_legend_handles_labels()
	Handles_Right, Labels_Right = Plot.right_ax.get_legend_handles_labels()


	Plot.set_title(f"Action Best Parameter Values for Combination of [{_Group.Crossover_Fallback_Version_Name}] Crossover Fallback Version\nand [{_Group.Mutation_Version_Name}] Mutation Version")
	Plot.right_ax.legend(Handles_Left + Handles_Right, Labels_Left + Labels_Right, loc = "upper right")
	Plot.set_ylabel("Actions")
	Plot.right_ax.set_ylabel("Time (Seconds)")
	Plot.locator_params("y", integer = True)
	Plot.right_ax.locator_params("y", integer = True)
	Plot.get_figure().savefig(f"SensitivityAnalysis/Graphs/Level 3/Best of each Parameter/Actions/Action Best Parameter Values for Combination of [{_Group.Crossover_Fallback_Version_Name}] and [{_Group.Mutation_Version_Name}].png")

	PyPlot.close()


	print(f"Finished: Action Best Parameter Values for Combination of [{_Group.Crossover_Fallback_Version_Name}] and [{_Group.Mutation_Version_Name}]")

for _Group in Time_Best_Parameter_Groups:
	Time_Best_Parameter_Data_Frame: PD.DataFrame = PD.DataFrame(
		[[f"{_Group.Changed_Parameter_Names[i].split(".")[-1]} = {_Group.Changed_Parameter_FromsTos[i][1]} ({_Group.Stats_List[i].Total_Attempts - _Group.Stats_List[i].Failed_Attempts}/{_Group.Stats_List[i].Total_Attempts})",
			_Group.Stats_List[i].Average_Action_History__Length,
			_Group.Stats_List[i].Average_Elapsed_Time
		] for i in range(len(_Group.Stats_List))],
		columns = [
			"Time Best Parameter Values (Successful / Total attempts)",
			"Average Action Amount",
			"Average Elapsed Time (Seconds)"
		]
	)

	Plot = Time_Best_Parameter_Data_Frame.plot(
		x = Time_Best_Parameter_Data_Frame.columns[0],
		kind = "bar",
		stacked = False,
		secondary_y = Time_Best_Parameter_Data_Frame.columns[2],
		mark_right = False,
		legend = False
	)

	Handles_Left, Labels_Left = Plot.get_legend_handles_labels()
	Handles_Right, Labels_Right = Plot.right_ax.get_legend_handles_labels()


	Plot.set_title(f"Time Best Parameter Values for Combination of [{_Group.Crossover_Fallback_Version_Name}] Crossover Fallback Version\nand [{_Group.Mutation_Version_Name}] Mutation Version")
	Plot.right_ax.legend(Handles_Left + Handles_Right, Labels_Left + Labels_Right, loc = "upper right")
	Plot.set_ylabel("Actions")
	Plot.right_ax.set_ylabel("Time (Seconds)")
	Plot.locator_params("y", integer = True)
	Plot.right_ax.locator_params("y", integer = True)
	Plot.get_figure().savefig(f"SensitivityAnalysis/Graphs/Level 3/Best of each Parameter/Time/Time Best Parameter Values for Combination of [{_Group.Crossover_Fallback_Version_Name}] and [{_Group.Mutation_Version_Name}].png")

	PyPlot.close()


	print(f"Finished: Time Best Parameter Values for Combination of [{_Group.Crossover_Fallback_Version_Name}] and [{_Group.Mutation_Version_Name}]")


Action_Best_Method_Data_Frame: PD.DataFrame = PD.DataFrame(
	[[f"{Action_Best_Method_Group.Crossover_Fallback_Version_Names[i]}\nwith {Action_Best_Method_Group.Mutation_Version_Names[i]}:\n{Action_Best_Method_Group.Changed_Parameter_Names[i].split(".")[-1]} = {Action_Best_Method_Group.Changed_Parameter_FromsTos[i][1]} ({Action_Best_Method_Group.Stats_List[i].Total_Attempts - Action_Best_Method_Group.Stats_List[i].Failed_Attempts}/{Action_Best_Method_Group.Stats_List[i].Total_Attempts})",
		Action_Best_Method_Group.Stats_List[i].Average_Action_History__Length,
		Action_Best_Method_Group.Stats_List[i].Average_Elapsed_Time
	] for i in range(len(Action_Best_Method_Group.Stats_List))],
	columns = [
		"Action Best Method Combinations and Parameter Values (Successful / Total attempts)",
		"Average Action Amount",
		"Average Elapsed Time (Seconds)"
	]
)

Plot = Action_Best_Method_Data_Frame.plot(
	x = Action_Best_Method_Data_Frame.columns[0],
	kind = "bar",
	stacked = False,
	secondary_y = Action_Best_Method_Data_Frame.columns[2],
	mark_right = False,
	legend = False
)

Handles_Left, Labels_Left = Plot.get_legend_handles_labels()
Handles_Right, Labels_Right = Plot.right_ax.get_legend_handles_labels()


Plot.set_title(f"Action Best Method Combinations and Parameter Values")
Plot.right_ax.legend(Handles_Left + Handles_Right, Labels_Left + Labels_Right, loc = "upper right")
Plot.set_ylabel("Actions")
Plot.right_ax.set_ylabel("Time (Seconds)")
Plot.locator_params("y", integer = True)
Plot.right_ax.locator_params("y", integer = True)
Plot.get_figure().savefig(f"SensitivityAnalysis/Graphs/Level 3/Best of each Method/Action Best Method Combinations and Parameter Values.png")

PyPlot.close()


print(f"Finished: Action Best Method Combinations and Parameter Values")


Time_Best_Method_Data_Frame: PD.DataFrame = PD.DataFrame(
	[[f"{Time_Best_Method_Group.Crossover_Fallback_Version_Names[i]}\nwith {Time_Best_Method_Group.Mutation_Version_Names[i]}:\n{Time_Best_Method_Group.Changed_Parameter_Names[i].split(".")[-1]} = {Time_Best_Method_Group.Changed_Parameter_FromsTos[i][1]} ({Time_Best_Method_Group.Stats_List[i].Total_Attempts - Time_Best_Method_Group.Stats_List[i].Failed_Attempts}/{Time_Best_Method_Group.Stats_List[i].Total_Attempts})",
		Time_Best_Method_Group.Stats_List[i].Average_Action_History__Length,
		Time_Best_Method_Group.Stats_List[i].Average_Elapsed_Time
	] for i in range(len(Time_Best_Method_Group.Stats_List))],
	columns = [
		"Time Best Method Combinations and Parameter Values (Successful / Total attempts)",
		"Average Action Amount",
		"Average Elapsed Time (Seconds)"
	]
)

Plot = Time_Best_Method_Data_Frame.plot(
	x = Time_Best_Method_Data_Frame.columns[0],
	kind = "bar",
	stacked = False,
	secondary_y = Time_Best_Method_Data_Frame.columns[2],
	mark_right = False,
	legend = False
)

Handles_Left, Labels_Left = Plot.get_legend_handles_labels()
Handles_Right, Labels_Right = Plot.right_ax.get_legend_handles_labels()


Plot.set_title(f"Time Best Method Combinations and Parameter Values")
Plot.right_ax.legend(Handles_Left + Handles_Right, Labels_Left + Labels_Right, loc = "upper right")
Plot.set_ylabel("Actions")
Plot.right_ax.set_ylabel("Time (Seconds)")
Plot.locator_params("y", integer = True)
Plot.right_ax.locator_params("y", integer = True)
Plot.get_figure().savefig(f"SensitivityAnalysis/Graphs/Level 3/Best of each Method/Time Best Method Combinations and Parameter Values.png")

PyPlot.close()


print(f"Finished: Time Best Method Combinations and Parameter Values")


Best_Of_Both_Criteria_Data_Frame: PD.DataFrame = PD.DataFrame(
	[[f"{Best_Of_Both_Criteria.Crossover_Fallback_Version_Names[i]}\nwith {Best_Of_Both_Criteria.Mutation_Version_Names[i]}:\n{Best_Of_Both_Criteria.Changed_Parameter_Names[i].split(".")[-1]} = {Best_Of_Both_Criteria.Changed_Parameter_FromsTos[i][1]} ({Best_Of_Both_Criteria.Stats_List[i].Total_Attempts - Best_Of_Both_Criteria.Stats_List[i].Failed_Attempts}/{Best_Of_Both_Criteria.Stats_List[i].Total_Attempts})",
		Best_Of_Both_Criteria.Stats_List[i].Average_Action_History__Length,
		Best_Of_Both_Criteria.Stats_List[i].Average_Elapsed_Time
	] for i in range(len(Best_Of_Both_Criteria.Stats_List))],
	columns = [
		"↑ Prioritizing Action amount | Change description (Successful / Total attempts) | Prioritizing execution Time ↑",
		"Average Action Amount",
		"Average Elapsed Time (Seconds)"
	]
)

Plot = Best_Of_Both_Criteria_Data_Frame.plot(
	x = Best_Of_Both_Criteria_Data_Frame.columns[0],
	kind = "bar",
	stacked = False,
	secondary_y = Best_Of_Both_Criteria_Data_Frame.columns[2],
	mark_right = False,
	legend = False
)

Handles_Left, Labels_Left = Plot.get_legend_handles_labels()
Handles_Right, Labels_Right = Plot.right_ax.get_legend_handles_labels()


Plot.set_title(f"Best Changes when prioritizing Action amount v/s execution Time")
Plot.right_ax.legend(Handles_Left + Handles_Right, Labels_Left + Labels_Right, loc = "upper right")
Plot.set_ylabel("Actions")
Plot.right_ax.set_ylabel("Time (Seconds)")
Plot.locator_params("y", integer = True)
Plot.right_ax.locator_params("y", integer = True)
Plot.get_figure().savefig(f"SensitivityAnalysis/Graphs/Level 3/Best Changes.png")

PyPlot.close()


print(f"Finished: Best Changes when prioritizing Action amount v/s execution Time")


print(f"Total: {len(Parameter_Groups) + len(Action_Best_Parameter_Groups) + len(Time_Best_Parameter_Groups) + 3} graphs.")
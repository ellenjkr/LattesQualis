import pandas as pd
from pprint import pprint
from jellyfish import jaro_distance
import unidecode

from _Classes.PyscopusModified import ScopusModified
from _Classes.Author import Author
from _Classes.Individuals import Student, Egress
from _Classes.Indicators import Indicators

from _Funções_e_Valores.verify_authors import search_authors_list, treat_exceptions
from _Funções_e_Valores._exceptions import scopus_articles_exceptions
from _Funções_e_Valores.values import quadrennium, FILE, HAS_EVENTS, FULL_PERIOD_AUTHORS, REQUEST_SCOPUS_DATA, EGRESS, SCOPUS_APIKEY


class Data():
	def __init__(self, professors, egress, students, qualis_2016, qualis_2020, qualis_2016_events, qualis_2020_events):
		super(Data, self).__init__()
		self.professors = professors
		self.egress = egress
		self.students = students
		self.qualis_2016 = qualis_2016
		self.qualis_2020 = qualis_2020
		self.qualis_2016_events = qualis_2016_events
		self.qualis_2020_events = qualis_2020_events

		self.exceptions = {'Nome Trabalho':[], 'Nome Evento Cadastrado':[], 'Nome Evento Canônico':[]} # For the exceptions sheet from the excel file
		self.reports = {'Author':[], 'Report':[]} # Reports by author

		self.authors_dict = {"Author":[], "A/E":[]} # Dictionary of authors (Professors, Students and Egress)
		columns = []
		for year in quadrennium:
			if year not in columns:
				columns.append(year)
		for col in columns:
			self.authors_dict[f"20{col}"] = []

		self.art_prof = pd.DataFrame() # Articles by professor
		self.authors_average = [] # List with the "average number of authors per article" of each professor
		
		self.irestritos_2016 = {'Total com trava':None, 'Total sem trava':None, 'Anais com trava':None, 'Anais sem trava':None, 'Periódicos':None}
		self.igerais_2016 = {'Total com trava':None, 'Total sem trava':None, 'Anais com trava':None, 'Anais sem trava':None, 'Periódicos':None}

		self.authors_indicators_2016 = [] # Indicators of each professor qualis 2016
		self.authors_indicators_2019 = [] # Indicators of each professor qualis 2019
		self.general_indicators_2016 = [] # Indicators for all professors together qualis 2016
		self.general_indicators_2019 = [] # Indicators for all professors together qualis 2019

		self.authors_indicators_2016_journals = [] # Indicators of each professor qualis 2016 (Journals)
		self.authors_indicators_2019_journals = [] # Indicators of each professor qualis 2019 (Journals)
		self.general_indicators_2016_journals = [] # Indicators for all professors together qualis 2016 (Journals)
		self.general_indicators_2019_journals = [] # Indicators for all professors together qualis 2019 (Journals)

		self.authors_indicators_2016_proceedings = [] # Indicators of each professor qualis 2016 (Proceedings)
		self.authors_indicators_2019_proceedings = [] # Indicators of each professor qualis 2019 (Proceedings)
		self.general_indicators_2016_proceedings = [] # Indicators for all professors together qualis 2016 (Proceedings)
		self.general_indicators_2019_proceedings = [] # Indicators for all professors together qualis 2019 (Proceedings)

		self.journals_a1_a4_2019 = None
		self.journals_a1_a4_SE_2019 = None
		self.journals_a1_a4_2016 = None
		self.journals_a1_a4_SE_2016 = None
		self.journal_metrics_2019 = None
		self.journal_metrics_2016 = None
		self.proceedings_metrics_2019 = None
		self.proceedings_metrics_2016 = None



	def treat_data(self):
		# Get the list of egress and students with their names and active-period
		egress = Egress(self.egress, quadrennium)
		self.egress_list = egress.get_egress_list()
		students = Student(self.students, quadrennium)
		self.students_list = students.get_students_list()

		if HAS_EVENTS == True:
			# Lowercase events
			for pos, i in enumerate(self.qualis_2016_events['Nome Padrão']):
				self.qualis_2016_events['Nome Padrão'][pos] = str(self.qualis_2016_events['Nome Padrão'][pos]).lower()
			for pos, i in enumerate(self.qualis_2020_events['Nome Padrão']):
				self.qualis_2020_events['Nome Padrão'][pos] = str(self.qualis_2020_events['Nome Padrão'][pos]).lower()

		# Remove "-" from ISSN
		for i in range(len(self.qualis_2016["ISSN"])):
			self.qualis_2016["ISSN"][i] = self.qualis_2016["ISSN"][i].replace("-", "")
		for i in range(len(self.qualis_2020["ISSN"])):
			self.qualis_2020["ISSN"][i] = self.qualis_2020["ISSN"][i].replace("-", "")


	def get_author_period(self, pos):
		if FULL_PERIOD_AUTHORS == True:
			period = {}
			for year in quadrennium:
				period[year] = True
		else:
			period = {}
			for year in quadrennium:
				period[year] = False

			if EGRESS == True:
				start = str(self.professors['Ingresso'][pos])[7:]
				start = start.replace('-', '')
				end = quadrennium[-1] # There's no limit
			else:
				if FILE == "UFSC 2017-2020":
					start = str(self.professors["Início do Vínculo"][pos])[2:4]
				else:
					start = str(self.professors["Início do Vínculo"][pos])[8:]
				end = str(self.professors["Fim do Vínculo"][pos])

				if end == "-":
					end = quadrennium[-1]
				else:
					if FILE == "UFSC 2017-2020":
						end = str(self.professors["Fim do Vínculo"][pos])[2:4]
					else:
						end = str(self.professors["Fim do Vínculo"][pos])[8:]

					if int(end) > int(quadrennium[-1]):
						end = quadrennium[-1]

			start_position = None
			end_position = None
			

			for pos, key in enumerate(period.keys()): # For each year of the quadrennium
				if pos == 0 and int(start) < int(quadrennium[0]): # If the start year is lower than the first year of the quadrennium
					start = quadrennium[0]
				if key == start:
					start_position = pos # The position of the start year on the quadrennium
				if key == end:
					end_position = pos # The position of the end year on the quadrennium


			for pos, key in enumerate(period.keys()):
				if int(end) >= int(quadrennium[0]):
					if pos >= start_position and pos <= end_position: # The start year, the end year and the years in between are true
						period[key] = True

		return period


	def get_authors_reports(self):
		# Iterates through the professors 
		for pos, professor in enumerate(self.professors["Nome"]):
			if str(professor) != 'nan':
				professor = str(professor)

				period = self.get_author_period(pos) # Get the period of valid publications
				author = Author(professor, period, self.qualis_2016, self.qualis_2020, self.qualis_2016_events, self.qualis_2020_events, self.professors, self.authors_dict["Author"])
				# print(professor)
				# print(pd.DataFrame(author.info))
				self.authors_dict["Author"] = author.authors_list # Updates the authors list
				self.reports['Author'].append(professor) # Adds the professor to the list of reports
				self.reports['Report'].append(pd.DataFrame(author.info)) # Adds the professor's report to the list of reports
				self.authors_average.append(author.get_authors_average()) # Adds the "average number of authors per article" to the list of averages

				for title in author.exceptions['Nome Trabalho']:
					self.exceptions['Nome Trabalho'].append(title)
				for event_registered in author.exceptions['Nome Evento Cadastrado']:
					self.exceptions['Nome Evento Cadastrado'].append(event_registered)
				for canon_event in author.exceptions['Nome Evento Canônico']:
					self.exceptions['Nome Evento Canônico'].append(canon_event)

		self.exceptions = pd.DataFrame(self.exceptions)


	def treat_names(self): # Looks for convergence between names written in different ways and replaces for the right name
		egress_names = []
		for egress in self.egress_list:
			egress_names.append(treat_exceptions(egress.name.strip()))

		students_names = []
		for student in self.students_list:
			students_names.append(treat_exceptions(student.name.strip()))

		for pos, report in enumerate(self.reports["Report"]):
			# df = pd.DataFrame(report)
			# for index, row in df.iterrows():
			for index, row in report.iterrows():
				for column in row.index:
					if "Autor" in str(column): # Goes through the authors columns
						if self.reports["Report"][pos][column][index] != " ":
							_, self.reports["Report"][pos].loc[index, column] = search_authors_list(self.authors_dict["Author"], str(self.reports["Report"][pos][column][index]))
							_, self.reports["Report"][pos].loc[index, column] = search_authors_list(egress_names, str(self.reports["Report"][pos][column][index]))
							_, self.reports["Report"][pos].loc[index, column] = search_authors_list(students_names, str(self.reports["Report"][pos][column][index]))
	
	def get_art_prof(self):
		for pos, report in enumerate(self.reports["Report"]):
			name_column = [self.reports["Author"][pos] for i in range(len(report))] # Generates a column with the name of the author for each article

			report_copy = report.copy() # A copy of the report
			report_copy.insert(loc=0, column='Nome', value=name_column) # Adds the name_column

			if pos == 0:
				self.art_prof = report_copy
			else:
				self.art_prof = pd.concat([self.art_prof, report_copy], ignore_index=True, sort=False) # Puts the reports together, in one dataframe
	
		# Replace "nan" values with " "
		for col in self.art_prof.columns:
			if "Autor" in col:
				for pos, i in enumerate(self.art_prof[col]):
					if str(i) == "NaN" or str(i) == "nan":
						self.art_prof.loc[pos, col] = " "


	def update_authors_dict(self):
		egress_names = []
		for egress in self.egress_list:
			egress_names.append(treat_exceptions(egress.name.strip())) # Gets the egress' name

		students_names = []
		for student in self.students_list:
			students_names.append(treat_exceptions(student.name.strip())) # Gets the student's name

		columns = []
		for year in quadrennium:
			if year not in columns:
				columns.append(year)
	
		# Looks for egress or students and marks them with a X in the "A/E" column
		for author in self.authors_dict["Author"]:
			if author in egress_names or author in students_names:
				self.authors_dict["A/E"].append("X")
			else:
				self.authors_dict["A/E"].append("")


			for col in columns:
				self.authors_dict[f"20{col}"].append("")

		result_df = self.art_prof.apply(lambda x: x.astype(str).str.lower()).drop_duplicates(subset="Título")
		publications = self.art_prof.loc[result_df.index]
		for index, row in publications.iterrows():
			for column in row.index:
				if "Autor" in str(column): # Goes through the authors columns
					for pos, author in enumerate(self.authors_dict["Author"]):
						if author == row[column]:
							year = row["Ano"]
							if "." in str(year):
								year = str(year).replace(".0", "")
								year = int(year)
							self.authors_dict[str(year)][pos] = "X"
					




	def get_indicators(self):
		all_publications = self.artppg.copy()

		indicators_2016 = Indicators(self.egress_list, self.students_list, all_publications, "CC 2016", general=True)
		gen_ind_2016, gen_ind_2016_journals, gen_ind_2016_proceedings = indicators_2016.get_indicators_2016()
		self.general_indicators_2016 = gen_ind_2016
		self.general_indicators_2016_journals = gen_ind_2016_journals
		self.general_indicators_2016_proceedings = gen_ind_2016_proceedings
		self.irestritos_2016 = indicators_2016.irestritos
		self.igerais_2016 = indicators_2016.igerais

		indicators_2019 = Indicators(self.egress_list, self.students_list, all_publications, "2019", general=True)
		gen_ind_2019, gen_ind_2019_journals, gen_ind_2019_proceedings = indicators_2019.get_indicators_2019()
		self.general_indicators_2019 = gen_ind_2019
		self.general_indicators_2019_journals = gen_ind_2019_journals
		self.general_indicators_2019_proceedings = gen_ind_2019_proceedings
		self.irestritos_2019 = indicators_2019.irestritos
		self.igerais_2019 = indicators_2019.igerais

		for report in self.reports["Report"]:
			indicators_2016 = Indicators(self.egress_list, self.students_list, report, "CC 2016")

			authors_ind_2016, authors_ind_2016_journals, authors_ind_2016_proceedings = indicators_2016.get_indicators_2016()
			self.authors_indicators_2016.append(authors_ind_2016)
			self.authors_indicators_2016_journals.append(authors_ind_2016_journals)
			self.authors_indicators_2016_proceedings.append(authors_ind_2016_proceedings)
			
			indicators_2019 = Indicators(self.egress_list, self.students_list, report, "2019")
			authors_ind_2019, authors_ind_2019_journals, authors_ind_2019_proceedings = indicators_2019.get_indicators_2019()
			self.authors_indicators_2019.append(authors_ind_2019)
			self.authors_indicators_2019_journals.append(authors_ind_2019_journals)
			self.authors_indicators_2019_proceedings.append(authors_ind_2019_proceedings)





	def analyze_journal_classifications(self, qualis_year):
		journals_a1_a4_list = [] # Journals A1-A4
		journals_a1_a4_SE = [] # Journals A1-A4 with students and/or egress
		journals_a1_b1_list = [] # Journals A1-B1
		journals_a1_b1_SE = [] # Journals A1-B1 with students and/or egress

		for pos, report in enumerate(self.reports["Report"]):
			# Separates by journal classifications 
			journals = report.loc[report["Tipo"] == "Periódico"] # All the publications in journals
			journals_a1 = journals.loc[journals[f"Qualis {qualis_year}"] == "A1"]
			journals_a2 = journals.loc[journals[f"Qualis {qualis_year}"] == "A2"]
			if qualis_year == "2019":
				journals_a3 = journals.loc[journals[f"Qualis {qualis_year}"] == "A3"]
				journals_a4 = journals.loc[journals[f"Qualis {qualis_year}"] == "A4"]
				journals_a1_a4 = pd.concat([journals_a1, journals_a2, journals_a3, journals_a4], ignore_index=True, sort=False)

				# Calculates the amount of articles A1-A4 with and without students/egress
				amount_journals_a1_a4 = len(journals_a1_a4.index)
				journals_a1_a4_list.append(amount_journals_a1_a4)
				indicators = Indicators(self.egress_list, self.students_list, journals_a1_a4, qualis_year)
				amount_journals_a1_a4_SE = indicators.get_SE(journals_a1_a4)
				journals_a1_a4_SE.append(amount_journals_a1_a4_SE)

				
			elif qualis_year == "CC 2016":
				journals_b1 = journals.loc[journals[f"Qualis {qualis_year}"] == "B1"]
				journals_a1_b1 = pd.concat([journals_a1, journals_a2, journals_b1], ignore_index=True, sort=False)

				# Calculates the amount of articles A1-B1 with and without students/egress
				amount_journals_a1_b1 = len(journals_a1_b1.index)
				journals_a1_b1_list.append(amount_journals_a1_b1)
				indicators = Indicators(self.egress_list, self.students_list, journals_a1_b1, qualis_year)
				amount_journals_a1_b1_SE = indicators.get_SE(journals_a1_b1)
				journals_a1_b1_SE.append(amount_journals_a1_b1_SE)

		if qualis_year == "2019":
			return (journals_a1_a4_list, journals_a1_a4_SE)
		elif qualis_year == "CC 2016":		
			return (journals_a1_b1_list, journals_a1_b1_SE)
			

		

	def analyze_journals(self):
		all_publications = self.artppg.copy()

		self.journals = all_publications.copy().loc[all_publications["Tipo"] == "Periódico"] # All the publications in journals

		self.journals.loc[:, 'Quantidade'] = self.journals["Nome de Publicação"].map(self.journals["Nome de Publicação"].value_counts()) # Calculates the number of times the journal appears and add that number to a column

		
		columns = ["Nome de Publicação", "ISSN/SIGLA", "Qualis CC 2016", "Qualis 2019", "Scopus 2019", "Quantidade"] # The columns we're gonna use

		drop_columns = []
		for column in self.journals.columns:
			if column not in columns:
				drop_columns.append(column)
		self.journals = self.journals.drop(columns=drop_columns)
		self.journals = self.journals.rename(columns={"ISSN/SIGLA": "ISSN"})
		self.journals = self.journals.drop_duplicates(subset="ISSN") # Drop all the duplicated journals

	def analyze_journal_metrics(self, qualis_year):
		journal_metrics = pd.DataFrame(columns=[f"Métrica {qualis_year}", "Qtd.", "Qtd. %"])
		if qualis_year == "2019":
			journal_metrics[f"Métrica {qualis_year}"] = ["Quantidade de periódicos diferentes", "Quantidade de periódicos A1-A4", "Quantidade de periódicos B1-B4", "Quantidade de periódicos Não Qualis"]
		elif qualis_year == "CC 2016":
			journal_metrics[f"Métrica {qualis_year}"] = ["Quantidade de periódicos diferentes", "Quantidade de periódicos A1-B1", "Quantidade de periódicos B2-B5", "Quantidade de periódicos Não Qualis"]

		amount = []
		amount_perc = []
		amount.append(len(self.journals.index))

		journals_a1 = self.journals.loc[self.journals[f"Qualis {qualis_year}"] == "A1"]
		journals_a2 = self.journals.loc[self.journals[f"Qualis {qualis_year}"] == "A2"]
		if qualis_year == "2019":
			journals_a3 = self.journals.loc[self.journals[f"Qualis {qualis_year}"] == "A3"]
			journals_a4 = self.journals.loc[self.journals[f"Qualis {qualis_year}"] == "A4"]
			journals_upperstrata = pd.concat([journals_a1, journals_a2, journals_a3, journals_a4], ignore_index=True, sort=False)
			amount.append(len(journals_upperstrata.index))

			journals_b1 = self.journals.loc[self.journals[f"Qualis {qualis_year}"] == "B1"]
			journals_b2 = self.journals.loc[self.journals[f"Qualis {qualis_year}"] == "B2"]
			journals_b3 = self.journals.loc[self.journals[f"Qualis {qualis_year}"] == "B3"]
			journals_b4 = self.journals.loc[self.journals[f"Qualis {qualis_year}"] == "B4"]
			journals_lowerstrata = pd.concat([journals_b1, journals_b2, journals_b3, journals_b4], ignore_index=True, sort=False)
			amount.append(len(journals_lowerstrata.index))
		elif qualis_year == "CC 2016":
			journals_b1 = self.journals.loc[self.journals[f"Qualis {qualis_year}"] == "B1"]
			journals_upperstrata = pd.concat([journals_a1, journals_a2, journals_b1], ignore_index=True, sort=False)
			amount.append(len(journals_upperstrata.index))

			journals_b2 = self.journals.loc[self.journals[f"Qualis {qualis_year}"] == "B2"]
			journals_b3 = self.journals.loc[self.journals[f"Qualis {qualis_year}"] == "B3"]
			journals_b4 = self.journals.loc[self.journals[f"Qualis {qualis_year}"] == "B4"]
			journals_b5 = self.journals.loc[self.journals[f"Qualis {qualis_year}"] == "B5"]
			journals_lowerstrata = pd.concat([journals_b2, journals_b3, journals_b4, journals_b5], ignore_index=True, sort=False)
			amount.append(len(journals_lowerstrata.index))

		others = self.journals.loc[((self.journals[f"Qualis {qualis_year}"] == "-") | (self.journals[f"Qualis {qualis_year}"] == "NP") | (self.journals[f"Qualis {qualis_year}"] == "C"))]
		amount.append(len(others.index))
		journal_metrics["Qtd."] = amount

		for i in journal_metrics["Qtd."]:
			amount_perc.append(f"{round(100/journal_metrics['Qtd.'][0] * i, 1)}%")
		
		journal_metrics["Qtd. %"] = amount_perc

		return journal_metrics


	def analyze_proceedings(self):
		all_publications = self.artppg.copy()
	
		self.proceedings = all_publications.loc[all_publications["Tipo"] == "Anais"]
		self.proceedings.loc[:, 'Quantidade'] = self.proceedings["Nome de Publicação"].map(self.proceedings["Nome de Publicação"].value_counts())
		columns = ["Nome de Publicação", "ISSN/SIGLA", "Qualis CC 2016", "Qualis 2019", "Scopus 2019", "Quantidade"]
		drop_columns = []
		for column in self.proceedings.columns:
			if column not in columns:
				drop_columns.append(column)
		self.proceedings = self.proceedings.drop(columns=drop_columns)
		self.proceedings = self.proceedings.rename(columns={"ISSN/SIGLA": "SIGLA"})
		self.proceedings = self.proceedings.drop_duplicates(subset="SIGLA")


	def analyze_proceedings_metrics(self, qualis_year):
		proceedings_metrics = pd.DataFrame(columns=[f"Métrica {qualis_year}", "Qtd.", "Qtd. %"])

		if qualis_year == "2019":
			proceedings_metrics[f"Métrica {qualis_year}"] = ["Quantidade de eventos diferentes", "Quantidade de eventos A1-A4", "Quantidade de eventos B1-B4", "Quantidade de eventos Não Qualis"]
		elif qualis_year == "CC 2016":
			proceedings_metrics[f"Métrica {qualis_year}"] = ["Quantidade de eventos diferentes", "Quantidade de eventos A1-B1", "Quantidade de eventos B2-B5", "Quantidade de eventos Não Qualis"]
		
		amount = []
		amount_perc = []
		amount.append(len(self.proceedings.index))

		proceedings_a1 = self.proceedings.loc[self.proceedings[f"Qualis {qualis_year}"] == "A1"]
		proceedings_a2 = self.proceedings.loc[self.proceedings[f"Qualis {qualis_year}"] == "A2"]
		if qualis_year == "2019":
			proceedings_a3 = self.proceedings.loc[self.proceedings[f"Qualis {qualis_year}"] == "A3"]
			proceedings_a4 = self.proceedings.loc[self.proceedings[f"Qualis {qualis_year}"] == "A4"]
			proceedings_a1_a4 = pd.concat([proceedings_a1, proceedings_a2, proceedings_a3, proceedings_a4], ignore_index=True, sort=False)
			amount.append(len(proceedings_a1_a4.index))

			proceedings_b1 = self.proceedings.loc[self.proceedings[f"Qualis {qualis_year}"] == "B1"]
			proceedings_b2 = self.proceedings.loc[self.proceedings[f"Qualis {qualis_year}"] == "B2"]
			proceedings_b3 = self.proceedings.loc[self.proceedings[f"Qualis {qualis_year}"] == "B3"]
			proceedings_b4 = self.proceedings.loc[self.proceedings[f"Qualis {qualis_year}"] == "B4"]
			proceedings_lowerstrata = pd.concat([proceedings_b1, proceedings_b2, proceedings_b3, proceedings_b4], ignore_index=True, sort=False)
			amount.append(len(proceedings_lowerstrata.index))

		elif qualis_year == "CC 2016":
			proceedings_b1 = self.proceedings.loc[self.proceedings[f"Qualis {qualis_year}"] == "B1"]
			proceedings_a1_a4 = pd.concat([proceedings_a1, proceedings_a2, proceedings_b1], ignore_index=True, sort=False)
			amount.append(len(proceedings_a1_a4.index))

			proceedings_b2 = self.proceedings.loc[self.proceedings[f"Qualis {qualis_year}"] == "B2"]
			proceedings_b3 = self.proceedings.loc[self.proceedings[f"Qualis {qualis_year}"] == "B3"]
			proceedings_b4 = self.proceedings.loc[self.proceedings[f"Qualis {qualis_year}"] == "B4"]
			proceedings_b5 = self.proceedings.loc[self.proceedings[f"Qualis {qualis_year}"] == "B5"]
			proceedings_lowerstrata = pd.concat([proceedings_b2, proceedings_b3, proceedings_b4, proceedings_b5], ignore_index=True, sort=False)
			amount.append(len(proceedings_lowerstrata.index))

		others = self.proceedings.loc[((self.proceedings[f"Qualis {qualis_year}"] == "-") | (self.proceedings[f"Qualis {qualis_year}"] == "NP") | (self.proceedings[f"Qualis {qualis_year}"] == "C"))]
		amount.append(len(others.index))

		proceedings_metrics["Qtd."] = amount

		for i in proceedings_metrics["Qtd."]:
			if i != 0:
				amount_perc.append(f"{round(100/proceedings_metrics['Qtd.'][0] * i, 1)}%") # proceedings_metrics['Qtd.'][0] holds the total amount of different journals
			else:
				amount_perc.append("0%")
			
		proceedings_metrics["Qtd. %"] = amount_perc

		return proceedings_metrics

	def get_artppg(self):
		self.artppg = self.art_prof.copy().drop(columns="Nome")
		result_df = self.artppg.apply(lambda x: x.astype(str).str.lower()).drop_duplicates(subset="Título")
		self.artppg = self.artppg.loc[result_df.index]
		# self.artppg = self.artppg.sort_values(by=['Título'], key= lambda col: col.str.lower())

		self.artppg = self.artppg.iloc[self.artppg['Título'].str.normalize('NFKD').argsort()]
		self.artppg['Temp'] = self.artppg['Título'].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')
		self.artppg = self.artppg.sort_values(by=['Temp'], ascending=True, key= lambda col: col.str.lower()).drop(columns=['Temp'])


		self.artppg = self.artppg.reset_index()

		for pos in range(self.artppg.shape[0]): # Check for titles that are the same but were written in different ways
			count = 1
			break_while = False

			if pos >= self.artppg.shape[0]:
				break
			while break_while == False:
				same_article = False
			
				if pos == self.artppg.shape[0]-1:
					break_while = True
				if break_while == False:
					similarity = jaro_distance(unidecode.unidecode(self.artppg['Título'][pos].lower()), unidecode.unidecode(self.artppg['Título'][pos + count].lower())) # Check for similarity
					year = self.artppg['Ano'][pos] == self.artppg['Ano'][pos + count] # Check if the year is the same
					journal = self.artppg['Nome de Publicação'][pos] == self.artppg['Nome de Publicação'][pos  + count] # Check if the journal is the same
					issn_initials = self.artppg['ISSN/SIGLA'][pos] == self.artppg['ISSN/SIGLA'][pos + count] # Check if the issn/initial is the same

					# Check if both articles have the same authors
					article_authors = []
					next_article_authors = []
					for col in self.artppg.columns:
						if "Autor" in col:
							if self.artppg[col][pos] != " ":
								article_authors.append(self.artppg[col][pos])
							if self.artppg[col][pos + count] != " ":
								next_article_authors.append(self.artppg[col][pos + count])

					same_authors = 0
					for author in article_authors:
						if author in next_article_authors:
							same_authors += 1

					if same_authors == len(article_authors) or same_authors == len(article_authors)-1:
						authors = True
					else:
						authors = False

					if similarity >= 0.80 and year == True and journal == True and issn_initials == True and authors == True: # Check if its the same article
						same_article = True
						self.artppg = self.artppg.drop([pos + count])
						self.artppg = self.artppg.reset_index(drop=True)


					if same_article == False: # If its not, verify the next one
						count += 1
					if same_article == False and count == 2: # If they're not the same, break the while loop
						break_while = True

		self.artppg = self.artppg.drop(columns=['index'])
		

	def get_scopus_citations(self):
		if REQUEST_SCOPUS_DATA == True:
			scopus_articles = {"Title":[], "Citations":[]}
			scopus = ScopusModified(SCOPUS_APIKEY)
			for pos, author_id in enumerate(self.professors["ID Scopus"]):
				if author_id != " " and author_id != "nan":
					try:
						author_id = int(str(author_id))
						search = scopus.search(f"AU-ID ({author_id})")
						docs_array = []
						for doc in search['scopus_id']: # Gets the documents
							docs_array.append(doc)
						
						# ============== TO RETRIEVE MORE DATA THAN THE LIMIT ====================
						# The limit is 25 by request

						done = 0
						not_done = 25
						citations_temp = []
						while not_done < len(docs_array) + 25: 
							citations_temp.append(scopus.retrieve_citation(scopus_id_array=docs_array[done:not_done], year_range=[int(f"20{quadrennium[0]}"), int(f"20{quadrennium[len(quadrennium)-1]}")])) # Retrieve the citations data
							done += 25
							not_done += 25
						# ========================================================================

						citations = citations_temp[0]
						for pos, citation in enumerate(citations_temp):
							if pos != 0:
								citations = citations.append(citation, ignore_index = True)
						for pos2, titulo in enumerate(search['title']):
							titulo = scopus_articles_exceptions(titulo)
							scopus_articles["Title"].append(titulo)
							scopus_articles["Citations"].append(citations["range_citation"][pos2])
					except Exception as err:
						print("Erro: ", err)
			citations = []
	
			for title in self.artppg["Título"]:
				pos = None
				for i, title2 in enumerate(scopus_articles["Title"]):
					if title.lower().strip() in title2 or title2 in title.lower().strip():
						pos = i
				if pos != None:
					citations.append(int(scopus_articles["Citations"][pos]))
				else:
					citations.append("")
					
		else:
			citations = []
			for title in self.artppg["Título"]:
				citations.append("")

		self.artppg.insert(8, 'Citações', citations)
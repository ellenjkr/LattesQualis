import pandas as pd
from autor import Author
from excel import ExcelFile
from individuos import Student, Egress
from verifica_autores import em_lista_autores, trata_exceçoes
from valores import ND, quadrennium
from PyscopusModified import ScopusModified
from pprint import pprint
from excecoes import excecoes_artigos_scopus

def calcula_AE(data_frame, lista_egressos, lista_alunos):
	egressos_nomes = []
	for egresso in lista_egressos:
		egressos_nomes.append(trata_exceçoes(egresso.name.strip()))
	alunos_nomes = []
	for aluno in lista_alunos:
		alunos_nomes.append(trata_exceçoes(aluno.name.strip()))

	AE_quantidade = 0
	for index, row in data_frame.iterrows():
		AE = False
		for coluna in row.index:
			if "Autor" in str(coluna):
				if data_frame[coluna][index] != "":
					for pos_egresso, egresso in enumerate(egressos_nomes):
						if data_frame[coluna][index] == egresso:
							if lista_egressos[pos_egresso].period[str(int(data_frame["Ano"][index]))[2:]] == True:
								AE = True

					for pos_aluno, aluno in enumerate(alunos_nomes):
						if data_frame[coluna][index] == aluno:
							if lista_alunos[pos_aluno].period[str(data_frame["Ano"][index])[2:]] == True:
								AE = True
		if AE == True:
			AE_quantidade += 1
	
	return AE_quantidade

def calcula_quantidade(data_frame, aux_porc, lista_egressos, lista_alunos):
	qtd_AE = calcula_AE(data_frame, lista_egressos, lista_alunos)
	qtd = len(data_frame.index)

	porc = f"{aux_porc * qtd:.2f}%"

	try:
		porc_AE = f"{100/qtd * qtd_AE:.2f}%"
	except ZeroDivisionError:
		porc_AE = "0%"


	return (qtd, qtd_AE, porc, porc_AE)

def get_indicadores(info, lista_egressos, lista_alunos, geral = False):
	data_frame = pd.DataFrame(info)
	porcentagens = []
	total_artigos = len(data_frame["Tipo"])
	if total_artigos != 0:
		aux_porc = 100/total_artigos
	else:
		aux_porc = 0
	porcentagens_AE = []

	periodicos = data_frame.loc[data_frame["Tipo"] == "Periódico"]
	periodicos, AE_periodicos, porc_periodicos, porc_AE_periodicos = calcula_quantidade(periodicos, aux_porc, lista_egressos, lista_alunos)
	
	anais = data_frame.loc[data_frame["Tipo"] == "Anais"]
	anais, AE_anais, porc_anais, porc_AE_anais = calcula_quantidade(anais, aux_porc, lista_egressos, lista_alunos)
	
	a1 = data_frame.loc[data_frame["Qualis 2019"] == "A1"]
	a1, AE_a1, porc_a1, porc_AE_a1 = calcula_quantidade(a1, aux_porc, lista_egressos, lista_alunos)

	a2 = data_frame.loc[data_frame["Qualis 2019"] == "A2"]
	a2, AE_a2, porc_a2, porc_AE_a2 = calcula_quantidade(a2, aux_porc, lista_egressos, lista_alunos)

	a3 = data_frame.loc[data_frame["Qualis 2019"] == "A3"]
	a3, AE_a3, porc_a3, porc_AE_a3 = calcula_quantidade(a3, aux_porc, lista_egressos, lista_alunos)

	a4 = data_frame.loc[data_frame["Qualis 2019"] == "A4"]
	a4, AE_a4, porc_a4, porc_AE_a4 = calcula_quantidade(a4, aux_porc, lista_egressos, lista_alunos)

	a1_a4 = a1 + a2 + a3 + a4
	AE_a1_a4 = AE_a1 + AE_a2 + AE_a3 + AE_a4
	porc_a1_a4 = f"{aux_porc * a1_a4:.2f}%"
	try:
		porc_AE_a1_a4 = f"{100/a1_a4 * AE_a1_a4:.2f}%"
	except ZeroDivisionError:
		porc_AE_a1_a4 = "0%"
	

	b1 = data_frame.loc[data_frame["Qualis 2019"] == "B1"]
	b1, AE_b1, porc_b1, porc_AE_b1 = calcula_quantidade(b1, aux_porc, lista_egressos, lista_alunos)

	b2 = data_frame.loc[data_frame["Qualis 2019"] == "B2"]
	b2, AE_b2, porc_b2, porc_AE_b2 = calcula_quantidade(b2, aux_porc, lista_egressos, lista_alunos)

	b3 = data_frame.loc[data_frame["Qualis 2019"] == "B3"]
	b3, AE_b3, porc_b3, porc_AE_b3 = calcula_quantidade(b3, aux_porc, lista_egressos, lista_alunos)

	b4 = data_frame.loc[data_frame["Qualis 2019"] == "B4"]
	b4, AE_b4, porc_b4, porc_AE_b4 = calcula_quantidade(b4, aux_porc, lista_egressos, lista_alunos)

	b1_b4 = b1 + b2 + b3 + b4
	AE_b1_b4 = AE_b1 + AE_b2 + AE_b3 + AE_b4
	porc_b1_b4 = f"{aux_porc * b1_b4:.2f}%"
	try:
		porc_AE_b1_b4 = f"{100/b1_b4 * AE_b1_b4:.2f}%"
	except ZeroDivisionError:
		porc_AE_b1_b4 = "0%"

	outros = data_frame.loc[((data_frame["Qualis 2019"] != "A1") & (data_frame["Qualis 2019"] != "A2") & (data_frame["Qualis 2019"] != "A3") & (data_frame["Qualis 2019"] != "A4"))]
	outros = outros.loc[((outros["Qualis 2019"] != "B1") & (outros["Qualis 2019"] != "B2") & (outros["Qualis 2019"] != "B3") & (outros["Qualis 2019"] != "B4"))]
	outros, AE_outros, porc_outros, porc_AE_outros = calcula_quantidade(outros, aux_porc, lista_egressos, lista_alunos)

	porcentagens.append(porc_periodicos)
	porcentagens.append(porc_anais)
	porcentagens.append(porc_a1_a4)
	porcentagens.append(porc_a1)
	porcentagens.append(porc_a2)
	porcentagens.append(porc_a3)
	porcentagens.append(porc_a4)
	porcentagens.append(porc_b1_b4)
	porcentagens.append(porc_b1)
	porcentagens.append(porc_b2)
	porcentagens.append(porc_b3)
	porcentagens.append(porc_b4)
	porcentagens.append(porc_outros)

	porcentagens_AE.append(porc_AE_periodicos)
	porcentagens_AE.append(porc_AE_anais)
	porcentagens_AE.append(porc_AE_a1_a4)
	porcentagens_AE.append(porc_AE_a1)
	porcentagens_AE.append(porc_AE_a2)
	porcentagens_AE.append(porc_AE_a3)
	porcentagens_AE.append(porc_AE_a4)
	porcentagens_AE.append(porc_AE_b1_b4)
	porcentagens_AE.append(porc_AE_b1)
	porcentagens_AE.append(porc_AE_b2)
	porcentagens_AE.append(porc_AE_b3)
	porcentagens_AE.append(porc_AE_b4)
	porcentagens_AE.append(porc_AE_outros)

	tipo_qualis = ["Periódicos", "Anais", "A1-A4", "A1", "A2", "A3", "A4", "B1-B4", "B1", "B2", "B3", "B4", "Outros"]
	tabela = {"Tipo/Qualis": tipo_qualis, "Quantidade": [], "Porcentagem": [], "Quantidade com alunos/egressos":[], "Porcentagem alunos/egressos":[]}

	tabela["Tipo/Qualis"].append(None)
	tabela["Tipo/Qualis"].append("Índice")
	tabela["Tipo/Qualis"].append("Irestrito")
	tabela["Tipo/Qualis"].append("Igeral")

	tabela["Quantidade"].append(periodicos)
	tabela["Quantidade"].append(anais)
	tabela["Quantidade"].append(a1_a4)
	tabela["Quantidade"].append(a1)
	tabela["Quantidade"].append(a2)
	tabela["Quantidade"].append(a3)
	tabela["Quantidade"].append(a4)
	tabela["Quantidade"].append(b1_b4)
	tabela["Quantidade"].append(b1)
	tabela["Quantidade"].append(b2)
	tabela["Quantidade"].append(b3)
	tabela["Quantidade"].append(b4)
	tabela["Quantidade"].append(outros)
	tabela["Quantidade"].append(None)

	Irestrito = a1 + (a2 * 0.875) + (a3 * 0.75) + (a4 * 0.625)
	if Irestrito != 0:
		Irestrito = round(Irestrito, 2)
		Irestrito_medio = round((Irestrito/ND), 2)
	else:
		Irestrito_medio = 0

	Igeral = Irestrito + (b1 * 0.5) + (b2 * 0.2) + (b3 * 0.1) + (b4 * 0.05)
	if Igeral != 0:
		Igeral = round(Igeral, 2)
		Igeral_medio = round((Igeral/ND), 2)
	else:
		Igeral_medio = 0
	tabela["Quantidade"].append("Acumulado")
	tabela["Quantidade"].append(Irestrito)
	tabela["Quantidade"].append(Igeral)

	tabela["Quantidade com alunos/egressos"].append(AE_periodicos)
	tabela["Quantidade com alunos/egressos"].append(AE_anais)
	tabela["Quantidade com alunos/egressos"].append(AE_a1_a4)
	tabela["Quantidade com alunos/egressos"].append(AE_a1)
	tabela["Quantidade com alunos/egressos"].append(AE_a2)
	tabela["Quantidade com alunos/egressos"].append(AE_a3)
	tabela["Quantidade com alunos/egressos"].append(AE_a4)
	tabela["Quantidade com alunos/egressos"].append(AE_b1_b4)
	tabela["Quantidade com alunos/egressos"].append(AE_b1)
	tabela["Quantidade com alunos/egressos"].append(AE_b2)
	tabela["Quantidade com alunos/egressos"].append(AE_b3)
	tabela["Quantidade com alunos/egressos"].append(AE_b4)
	tabela["Quantidade com alunos/egressos"].append(AE_outros)
	tabela["Quantidade com alunos/egressos"].append(None)
	tabela["Quantidade com alunos/egressos"].append(None)
	tabela["Quantidade com alunos/egressos"].append(None)
	tabela["Quantidade com alunos/egressos"].append(None)

	tabela["Porcentagem alunos/egressos"] = porcentagens_AE
	tabela["Porcentagem alunos/egressos"].append(None)
	tabela["Porcentagem alunos/egressos"].append(None)
	tabela["Porcentagem alunos/egressos"].append(None)
	tabela["Porcentagem alunos/egressos"].append(None)

	tabela["Porcentagem"] = porcentagens
	tabela["Porcentagem"].append(None)
	if geral:
		tabela["Porcentagem"].append("Média por docente")
		tabela["Porcentagem"].append(Irestrito_medio)
		tabela["Porcentagem"].append(Igeral_medio)
	else:
		tabela["Porcentagem"].append(None)
		tabela["Porcentagem"].append(None)
		tabela["Porcentagem"].append(None)
	
	return pd.DataFrame(tabela)

def read_files():
	# Read files - People
	try:
		professors = pd.read_csv("UNIVALI - PPGC - Professores.csv", sep=";", encoding='iso-8859-1')
	except:
		professors = pd.read_csv("UNIVALI - PPGC - Professores.csv", sep=";", encoding='utf-8')
	try:
		egress = pd.read_csv("planilha_egressos_lattes.CSV", sep=";", encoding='iso-8859-1')
	except:
		egress = pd.read_csv("planilha_egressos_lattes.CSV", sep=";", encoding='utf-8')
	try:
		students = pd.read_csv("Planilha - Levantamento alunos ativos.CSV", sep=";", encoding='iso-8859-1')
	except:
		students = pd.read_csv("Planilha - Levantamento alunos ativos.CSV", sep=";", encoding='utf-8')
	

	# Read files - Qualis
	try:
		qualis_cc2016_file = pd.read_csv("Qualis/QualisCC_2013_2016.csv", sep=";", encoding='iso-8859-1')
	except:
		qualis_cc2016_file = pd.read_csv("Qualis/QualisCC_2013_2016.csv", sep=";", encoding='utf-8')
	try:
		qualis_xx2020_file = pd.read_csv("Qualis/QualisXX_2020.csv", sep=";", encoding='iso-8859-1')
	except:
		qualis_xx2020_file = pd.read_csv("Qualis/QualisXX_2020.csv", sep=";", encoding='utf-8')
	try:
		qualis_cc2016_eventos = pd.read_csv("Qualis/QualisCC_eventos_2016.csv", sep=";", encoding='iso-8859-1')
	except:
		qualis_cc2016_eventos = pd.read_csv("Qualis/QualisCC_eventos_2016.csv", sep=";", encoding='utf-8')
	try:
		qualis_xx2020_eventos = pd.read_csv("Qualis/QualisXX_eventos_2020.csv", sep=";", encoding='iso-8859-1')
	except:
		qualis_xx2020_eventos = pd.read_csv("QualisXX_eventos_2020.csv", sep=";", encoding='utf-8')


	# Read file - Exceptions
	try:
		exceptions = pd.read_csv("excecoes.csv", sep=";", encoding='iso-8859-1')
	except:
		exceptions = pd.read_csv("excecoes.csv", sep=";", encoding='utf-8')

	return (professors, egress, students, qualis_cc2016_file, qualis_xx2020_file, qualis_cc2016_eventos, qualis_xx2020_eventos, exceptions)


class Data():
	def __init__(self, professors, egress, students, qualis_2016, qualis_2020, qualis_2016_events, qualis_2020_events, exceptions):
		super(Data, self).__init__()
		self.professors = professors
		self.egress = egress
		self.students = students
		self.qualis_2016 = qualis_2016
		self.qualis_2020 = qualis_2020
		self.qualis_2016_events = qualis_2016_events
		self.qualis_2020_events = qualis_2020_events
		self.exceptions = exceptions

		self.reports = {'Author':[], 'Report':[]} # Reports by author
		self.authors_dict = {"Author":[], "A/E":[]} # Dictionary of authors (Professors, Students and Egress)
		self.art_prof = pd.DataFrame() # Articles by professor
		self.authors_mean = [] # List with the "mean of authors by article" of each professor
		self.authors_indicators = [] # Indicators of each professor
		self.general_indicators = [] # Indicators for all professors together


	def treat_data(self):
		# Get the list of egress and students with their names and active-period
		egress = Egress(self.egress, quadrennium)
		self.egress_list = egress.get_egress_list()
		students = Student(self.students, quadrennium)
		self.students_list = students.get_students_list()

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
		period = {quadrennium[0]: False, quadrennium[1]: False, quadrennium[2]: False, quadrennium[3]: False}
		start = str(self.professors["Início do Vínculo"][pos])[8:]
		end = str(self.professors["Fim do Vínculo"][pos])

		if end == "-":
			end = quadrennium[3]
		else:
			end = str(self.professors["Fim do Vínculo"][pos])[8:]

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
				self.authors_dict["Author"] = author.lista_autores # Updates the authors list
				self.reports['Author'].append(professor) # Adds the professor to the list of reports
				self.reports['Report'].append(pd.DataFrame(author.info)) # Adds the professor's report to the list of reports
				self.authors_mean.append(author.get_media_autores()) # Adds the "mean of authors by article" to the list of means

	def treat_names(self): # Looks for convergence between names written in different ways and replaces for the right name
		egress_names = []
		for egress in self.egress_list:
			egress_names.append(trata_exceçoes(egress.name.strip()))

		students_names = []
		for student in self.students_list:
			students_names.append(trata_exceçoes(student.name.strip()))

		for pos, report in enumerate(self.reports["Report"]):
			# df = pd.DataFrame(report)
			# for index, row in df.iterrows():
			for index, row in report.iterrows():
				for column in row.index:
					if "Autor" in str(column): # Goes through the authors columns
						if self.reports["Report"][pos][column][index] != " ":
							_, self.reports["Report"][pos][column][index] = em_lista_autores(self.authors_dict["Author"], str(self.reports["Report"][pos][column][index]))
							_, self.reports["Report"][pos][column][index] = em_lista_autores(egress_names, str(self.reports["Report"][pos][column][index]))
							_, self.reports["Report"][pos][column][index] = em_lista_autores(students_names, str(self.reports["Report"][pos][column][index]))
	
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
			egress_names.append(trata_exceçoes(egress.name.strip())) # Gets the egress' name

		students_names = []
		for student in self.students_list:
			students_names.append(trata_exceçoes(student.name.strip())) # Gets the student's name

		# Looks for egress or students and marks them with a X in the "A/E" column
		for author in self.authors_dict["Author"]:
			if author in egress_names or author in students_names:
				self.authors_dict["A/E"].append("X")
			else:
				self.authors_dict["A/E"].append("")


	def get_indicators(self):
		for report in self.reports["Report"]:
			self.authors_indicators.append(get_indicadores(report, self.egress_list, self.students_list))
		self.general_indicators = get_indicadores(self.art_prof, self.egress_list, self.students_list, geral=True)


	def analyze_journal_classifications(self):
		self.journals_a1_a4 = [] # Journals A1-A4
		self.journals_a1_a4_ae = [] # Journals A1-A4 with students and/or egress

		for pos, report in enumerate(self.reports["Report"]):
			# Separates by journal classifications 
			journals = report.loc[report["Tipo"] == "Periódico"] # All the publications in journals
			journals_a1 = journals.loc[journals["Qualis 2019"] == "A1"]
			journals_a2 = journals.loc[journals["Qualis 2019"] == "A2"]
			journals_a3 = journals.loc[journals["Qualis 2019"] == "A3"]
			journals_a4 = journals.loc[journals["Qualis 2019"] == "A4"]
			journals_a1_a4 = pd.concat([journals_a1, journals_a2, journals_a3, journals_a4], ignore_index=True, sort=False)

			# Calculates the amount of articles A1-A4 with and without students/egress
			amount_journals_a1_a4 = len(journals_a1_a4.index)
			self.journals_a1_a4.append(amount_journals_a1_a4)
			amount_journals_a1_a4_ae = calcula_AE(journals_a1_a4, self.egress_list, self.students_list)
			self.journals_a1_a4_ae.append(amount_journals_a1_a4_ae)

	def analyze_journals(self):
		all_publications = self.art_prof.copy()
		all_publications = all_publications.drop_duplicates(subset="Título")

		self.journals = all_publications.loc[all_publications["Tipo"] == "Periódico"] # All the publications in journals
		self.journals.loc[:, 'Quantidade'] = self.journals["Nome de Publicação"].map(self.journals["Nome de Publicação"].value_counts()) # Calculates the number of times the journal appears and add that number to a column
		
		columns = ["Nome de Publicação", "ISSN/SIGLA", "Qualis CC 2016", "Qualis 2019", "Scopus 2019", "Quantidade"] # The columns we're gonna use

		drop_columns = []
		for column in self.journals.columns:
			if column not in columns:
				drop_columns.append(column)
		self.journals = self.journals.drop(columns=drop_columns)
		self.journals = self.journals.rename(columns={"ISSN/SIGLA": "ISSN"})
		self.journals = self.journals.drop_duplicates(subset="ISSN") # Drop all the duplicated journals

	def analyze_journal_metrics(self):
		self.journal_metrics = pd.DataFrame(columns=["Métrica", "Qtd.", "Qtd. %"])
		self.journal_metrics["Métrica"] = ["Quantidade de periódicos diferentes", "Quantidade de periódicos A1-A4", "Quantidade de periódicos B1-B4", "Quantidade de periódicos Não Qualis"]

		amount = []
		amount_perc = []
		amount.append(len(self.journals.index))

		journals_a1 = self.journals.loc[self.journals["Qualis 2019"] == "A1"]
		journals_a2 = self.journals.loc[self.journals["Qualis 2019"] == "A2"]
		journals_a3 = self.journals.loc[self.journals["Qualis 2019"] == "A3"]
		journals_a4 = self.journals.loc[self.journals["Qualis 2019"] == "A4"]
		journals_a1_a4 = pd.concat([journals_a1, journals_a2, journals_a3, journals_a4], ignore_index=True, sort=False)
		amount.append(len(journals_a1_a4.index))

		journals_b1 = self.journals.loc[self.journals["Qualis 2019"] == "B1"]
		journals_b2 = self.journals.loc[self.journals["Qualis 2019"] == "B2"]
		journals_b3 = self.journals.loc[self.journals["Qualis 2019"] == "B3"]
		journals_b4 = self.journals.loc[self.journals["Qualis 2019"] == "B4"]
		journals_b1_b4 = pd.concat([journals_b1, journals_b2, journals_b3, journals_b4], ignore_index=True, sort=False)
		amount.append(len(journals_b1_b4.index))

		others = self.journals.loc[((self.journals["Qualis 2019"] == "-") | (self.journals["Qualis 2019"] == "NP") | (self.journals["Qualis 2019"] == "C"))]
		amount.append(len(others.index))
		self.journal_metrics["Qtd."] = amount

		for i in self.journal_metrics["Qtd."]:
			amount_perc.append(f"{round(100/self.journal_metrics['Qtd.'][0] * i, 1)}%")
		
		self.journal_metrics["Qtd. %"] = amount_perc


	def analyze_proceedings(self):
		all_publications = self.art_prof.copy()
		all_publications = all_publications.drop_duplicates(subset="Título")

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


	def analyze_proceedings_metrics(self):
		self.proceedings_metrics = pd.DataFrame(columns=["Métrica", "Qtd.", "Qtd. %"])
		self.proceedings_metrics["Métrica"] = ["Quantidade de eventos diferentes", "Quantidade de eventos A1-A4", "Quantidade de eventos B1-B4", "Quantidade de eventos Não Qualis"]

		amount = []
		amount_perc = []
		amount.append(len(self.proceedings.index))

		proceedings_a1 = self.proceedings.loc[self.proceedings["Qualis 2019"] == "A1"]
		proceedings_a2 = self.proceedings.loc[self.proceedings["Qualis 2019"] == "A2"]
		proceedings_a3 = self.proceedings.loc[self.proceedings["Qualis 2019"] == "A3"]
		proceedings_a4 = self.proceedings.loc[self.proceedings["Qualis 2019"] == "A4"]
		proceedings_a1_a4 = pd.concat([proceedings_a1, proceedings_a2, proceedings_a3, proceedings_a4], ignore_index=True, sort=False)
		amount.append(len(proceedings_a1_a4.index))

		proceedings_b1 = self.proceedings.loc[self.proceedings["Qualis 2019"] == "B1"]
		proceedings_b2 = self.proceedings.loc[self.proceedings["Qualis 2019"] == "B2"]
		proceedings_b3 = self.proceedings.loc[self.proceedings["Qualis 2019"] == "B3"]
		proceedings_b4 = self.proceedings.loc[self.proceedings["Qualis 2019"] == "B4"]
		proceedings_b1_b4 = pd.concat([proceedings_b1, proceedings_b2, proceedings_b3, proceedings_b4], ignore_index=True, sort=False)
		amount.append(len(proceedings_b1_b4.index))

		others = self.proceedings.loc[((self.proceedings["Qualis 2019"] == "-") | (self.proceedings["Qualis 2019"] == "NP") | (self.proceedings["Qualis 2019"] == "C"))]
		amount.append(len(others.index))

		self.proceedings_metrics["Qtd."] = amount

		for i in self.proceedings_metrics["Qtd."]:
			amount_perc.append(f"{round(100/self.proceedings_metrics['Qtd.'][0] * i, 1)}%")
		
		self.proceedings_metrics["Qtd. %"] = amount_perc

	def get_artppg(self):
		self.artppg = self.art_prof.copy().drop(columns="Nome")

	def get_scopus_citations(self):
		# scopus_articles = {"Title":[], "Citations":[]}
		# scopus = ScopusModified('2f8a856ea2c32c265b4c5a9895e6900d')
		# for pos, author_id in enumerate(self.professors["ID Scopus"]):
		# 	try:
		# 		search = scopus.search(f"AU-ID ({author_id})")
		# 		docs_array = []
		# 		for doc in search['scopus_id']: # Gets the documents
		# 			docs_array.append(doc)
				
		# 		# ============== TO RETRIEVE MORE DATA THAN THE LIMIT ====================
		# 		# The limit is 25 by request

		# 		done = 0
		# 		not_done = 25
		# 		citations_temp = []
		# 		while not_done < len(docs_array) + 25: 
		# 			citations_temp.append(scopus.retrieve_citation(scopus_id_array=docs_array[done:not_done], year_range=[2017, 2020])) # Retrieve the citations data
		# 			done += 25
		# 			not_done += 25
		# 		# ========================================================================

		# 		citations = citations_temp[0]
		# 		for pos, citation in enumerate(citations_temp):
		# 			if pos != 0:
		# 				citations = citations.append(citation, ignore_index = True)
		# 		for pos2, titulo in enumerate(search['title']):
		# 			titulo = excecoes_artigos_scopus(titulo)
		# 			scopus_articles["Titulo"].append(titulo)
		# 			scopus_articles["Citações"].append(citations["range_citation"][pos2])
		# 	except:
		# 		pass
		citations = []
		for title in self.artppg["Título"]:
			citations.append("-")
			# pos = None
			# for i, title2 in enumerate(scopus_articles["Title"]):
			# 	if title.lower().strip() in title2 or title2 in title.lower().strip():
			# 		pos = i
			# if pos != None:
			# 	citations.append(str(scopus_articles["Citations"][pos]))
			# else:
			# 	citations.append("-")

		self.artppg.insert(8, 'Citações', citations)



if __name__ == '__main__':
	
	professors, egress, students, qualis_2016, qualis_2020, qualis_2016_events, qualis_2020_events, exceptions = read_files()

	data = Data(professors, egress, students, qualis_2016, qualis_2020, qualis_2016_events, qualis_2020_events, exceptions)
	data.treat_data()
	data.get_authors_reports()
	data.treat_names()
	data.get_art_prof()
	data.update_authors_dict()
	data.get_indicators()
	data.analyze_journal_classifications()
	data.analyze_journals()
	data.analyze_journal_metrics()
	data.analyze_proceedings()
	data.analyze_proceedings_metrics()
	data.get_artppg()
	data.get_scopus_citations()

	# excel = ExcelFile(relatorios, pd.DataFrame(dic_autores), art_prof_df, artppg, medias_autores, indicadores_autores, indicadores_geral, lista_egressos, lista_alunos, excecoes, per_a1_a4, per_a1_a4_ae, periodicos, anais, periodicos_metricas, anais_metricas)
	excel = ExcelFile(data.reports, pd.DataFrame(data.authors_dict), data.art_prof, data.artppg, data.authors_mean, data.authors_indicators, data.general_indicators, data.egress_list, data.students_list, data.exceptions, data.journals_a1_a4, data.journals_a1_a4_ae, data.journals, data.proceedings, data.journal_metrics, data.proceedings_metrics)

	excel.salva_arquivo()

	
	
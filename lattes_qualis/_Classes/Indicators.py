from _Funções_e_Valores.verify_authors import treat_exceptions
from _Funções_e_Valores.values import ND

import pandas as pd


class Indicators():
	def __init__(self, egress_list, students_list, info, qualis_year, general=False):
		super(Indicators, self).__init__()
		self.egress_list = egress_list
		self.students_list = students_list
		self.info = info
		self.qualis_year = qualis_year
		self.general = general


	def get_SE(self, data_frame): # Get the amount of publications that contains students or egress as authors
		# Get students and egress names
		egress_names = []
		for egress in self.egress_list:
			egress_names.append(treat_exceptions(egress.name.strip()))
		students_names = []
		for student in self.students_list:
			students_names.append(treat_exceptions(student.name.strip()))

		# Calculate the amount of students and egress who appear as authors
		amount_SE = 0
		for index, row in data_frame.iterrows():
			SE = False
			for column in row.index:
				if "Autor" in str(column):
					if data_frame[column][index] != "": # If the value isn't null
						# Verify if the author's name is on the egress list and if it's a valid publication year 
						for pos_egress, egress in enumerate(egress_names):
							if data_frame[column][index] == egress:
								if self.egress_list[pos_egress].period[str(int(data_frame["Ano"][index]))[2:4]] is True:
									SE = True
						# Verify if the author's name is on the students list and if it's a valid publication year 
						for pos_student, student in enumerate(students_names):
							if data_frame[column][index] == student:
								if self.students_list[pos_student].period[str(data_frame["Ano"][index])[2:4]] is True:
									SE = True
			# If there's an egress or a student as an author for that publication it increases the amount of SE
			if SE == True:
				amount_SE += 1
		
		return amount_SE

	def calculate_amount(self, data_frame, perc_aux): 
		amount_SE = self.get_SE(data_frame) # Get the amount of publications that contains students or egress as authors
		amount = len(data_frame.index) # Amount of publications

		perc = f"{perc_aux * amount:.2f}%" # Percentage of this type of publication 

		try:
			perc_SE = f"{100/amount * amount_SE:.2f}%" # Percentage with students or egress
		except ZeroDivisionError:
			perc_SE = "0%"


		return (amount, amount_SE, perc, perc_SE)

	def build_table_2016_general(self, journals, proceedings, a1_b1, a1, a2, b1, 
			b2_b5, b2, b3, b4, b5, others, Irestrito, Irestrito_journals, Irestrito_proceedings, 
			Igeral, Igeral_journals, Igeral_proceedings, SE_journals, SE_proceedings, SE_a1_b1, 
			SE_a1, SE_a2, SE_b1, SE_b2_b5, SE_b2, SE_b3, SE_b4, SE_b5, SE_others, percentages_SE, 
			percentages, Irestrito_medio, Irestrito_medio_journals, Irestrito_medio_proceedings, 
			Igeral_medio, Igeral_medio_journals, Igeral_medio_proceedings):
		type_qualis = ["Periódicos", "Anais", "A1-B1", "A1", "A2", "B1", "B2-B5", "B2", "B3", "B4", "B5", "Outros"]
		table = {f"Tipo/Qualis {self.qualis_year}": type_qualis, "Quantidade": [], "Porcentagem": [], 'Quantidade com alunos/egressos':[], "% Alunos/Egressos":[]}

		table[f"Tipo/Qualis {self.qualis_year}"].append(None)
		table[f"Tipo/Qualis {self.qualis_year}"].append("Índice")
		table[f"Tipo/Qualis {self.qualis_year}"].append("Irestrito")
		table[f"Tipo/Qualis {self.qualis_year}"].append("Igeral")
		table[f"Tipo/Qualis {self.qualis_year}"].append("Irestrito Periódicos")
		table[f"Tipo/Qualis {self.qualis_year}"].append("Igeral Periódicos")
		table[f"Tipo/Qualis {self.qualis_year}"].append("Irestrito Anais")
		table[f"Tipo/Qualis {self.qualis_year}"].append("Igeral Anais")

		table["Quantidade"].append(journals)
		table["Quantidade"].append(proceedings)
		table["Quantidade"].append(a1_b1)
		table["Quantidade"].append(a1)
		table["Quantidade"].append(a2)
		table["Quantidade"].append(b1)
		table["Quantidade"].append(b2_b5)
		table["Quantidade"].append(b2)
		table["Quantidade"].append(b3)
		table["Quantidade"].append(b4)
		table["Quantidade"].append(b5)
		table["Quantidade"].append(others)
		table["Quantidade"].append(None)
		table["Quantidade"].append("Acumulado")
		table["Quantidade"].append(Irestrito)
		table["Quantidade"].append(Igeral)
		table["Quantidade"].append(Irestrito_journals)
		table["Quantidade"].append(Igeral_journals)
		table["Quantidade"].append(Irestrito_proceedings)
		table["Quantidade"].append(Igeral_proceedings)

		table['Quantidade com alunos/egressos'].append(SE_journals)
		table['Quantidade com alunos/egressos'].append(SE_proceedings)
		table['Quantidade com alunos/egressos'].append(SE_a1_b1)
		table['Quantidade com alunos/egressos'].append(SE_a1)
		table['Quantidade com alunos/egressos'].append(SE_a2)
		table['Quantidade com alunos/egressos'].append(SE_b1)
		table['Quantidade com alunos/egressos'].append(SE_b2_b5)
		table['Quantidade com alunos/egressos'].append(SE_b2)
		table['Quantidade com alunos/egressos'].append(SE_b3)
		table['Quantidade com alunos/egressos'].append(SE_b4)
		table['Quantidade com alunos/egressos'].append(SE_b5)
		table['Quantidade com alunos/egressos'].append(SE_others)
		table['Quantidade com alunos/egressos'].append(None)
		table['Quantidade com alunos/egressos'].append(None)
		table['Quantidade com alunos/egressos'].append(None)
		table['Quantidade com alunos/egressos'].append(None)
		table['Quantidade com alunos/egressos'].append(None)
		table['Quantidade com alunos/egressos'].append(None)
		table['Quantidade com alunos/egressos'].append(None)
		table['Quantidade com alunos/egressos'].append(None)

		table["% Alunos/Egressos"] = percentages_SE
		table["% Alunos/Egressos"].append(None)
		table["% Alunos/Egressos"].append(None)
		table["% Alunos/Egressos"].append(None)
		table["% Alunos/Egressos"].append(None)
		table["% Alunos/Egressos"].append(None)
		table["% Alunos/Egressos"].append(None)
		table["% Alunos/Egressos"].append(None)
		table["% Alunos/Egressos"].append(None)

		table["Porcentagem"] = percentages
		table["Porcentagem"].append(None)
		if self.general:
			table["Porcentagem"].append("Média por docente")
			table["Porcentagem"].append(Irestrito_medio)
			table["Porcentagem"].append(Igeral_medio)
			table["Porcentagem"].append(Irestrito_medio_journals)
			table["Porcentagem"].append(Igeral_medio_journals)
			table["Porcentagem"].append(Irestrito_medio_proceedings)
			table["Porcentagem"].append(Igeral_medio_proceedings)
		else:
			table["Porcentagem"].append(None)
			table["Porcentagem"].append(None)
			table["Porcentagem"].append(None)
			table["Porcentagem"].append(None)
			table["Porcentagem"].append(None)
			table["Porcentagem"].append(None)
			table["Porcentagem"].append(None)

		return table

	# Proceedings and Journals separated
	def build_table_2016_separated(self, a1_b1, a1, a2, b1, b2_b5, b2, b3, b4, b5, others, 
		Irestrito, Igeral, SE_a1_b1, SE_a1, SE_a2, SE_b1, SE_b2_b5, SE_b2, SE_b3, SE_b4, 
		SE_b5, SE_others, percentages_SE, percentages, Irestrito_medio, Igeral_medio):
		type_qualis = ["A1-B1", "A1", "A2", "B1", "B2-B5", "B2", "B3", "B4", "B5", "Outros"]
		table = {f"Tipo/Qualis {self.qualis_year}": type_qualis, "Quantidade": [], "Porcentagem": [], 'Quantidade com alunos/egressos':[], "% Alunos/Egressos":[]}

		table[f"Tipo/Qualis {self.qualis_year}"].append(None)
		table[f"Tipo/Qualis {self.qualis_year}"].append("Índice")
		table[f"Tipo/Qualis {self.qualis_year}"].append("Irestrito")
		table[f"Tipo/Qualis {self.qualis_year}"].append("Igeral")


		table["Quantidade"].append(a1_b1)
		table["Quantidade"].append(a1)
		table["Quantidade"].append(a2)
		table["Quantidade"].append(b1)
		table["Quantidade"].append(b2_b5)
		table["Quantidade"].append(b2)
		table["Quantidade"].append(b3)
		table["Quantidade"].append(b4)
		table["Quantidade"].append(b5)
		table["Quantidade"].append(others)
		table["Quantidade"].append(None)
		table["Quantidade"].append("Acumulado")
		table["Quantidade"].append(Irestrito)
		table["Quantidade"].append(Igeral)

		table['Quantidade com alunos/egressos'].append(SE_a1_b1)
		table['Quantidade com alunos/egressos'].append(SE_a1)
		table['Quantidade com alunos/egressos'].append(SE_a2)
		table['Quantidade com alunos/egressos'].append(SE_b1)
		table['Quantidade com alunos/egressos'].append(SE_b2_b5)
		table['Quantidade com alunos/egressos'].append(SE_b2)
		table['Quantidade com alunos/egressos'].append(SE_b3)
		table['Quantidade com alunos/egressos'].append(SE_b4)
		table['Quantidade com alunos/egressos'].append(SE_b5)
		table['Quantidade com alunos/egressos'].append(SE_others)
		table['Quantidade com alunos/egressos'].append(None)
		table['Quantidade com alunos/egressos'].append(None)
		table['Quantidade com alunos/egressos'].append(None)
		table['Quantidade com alunos/egressos'].append(None)

		table["% Alunos/Egressos"] = percentages_SE
		table["% Alunos/Egressos"].append(None)
		table["% Alunos/Egressos"].append(None)
		table["% Alunos/Egressos"].append(None)
		table["% Alunos/Egressos"].append(None)


		table["Porcentagem"] = percentages
		table["Porcentagem"].append(None)
		if self.general:
			table["Porcentagem"].append("Média por docente")
			table["Porcentagem"].append(Irestrito_medio)
			table["Porcentagem"].append(Igeral_medio)

		else:
			table["Porcentagem"].append(None)
			table["Porcentagem"].append(None)
			table["Porcentagem"].append(None)

		return table

	def build_table_2019_general(self, journals, proceedings, a1_a4, a1, a2, a3, a4, 
			b1_b4, b1, b2, b3, b4, others, Irestrito, Igeral, Irestrito_journals, Igeral_journals, 
			Irestrito_proceedings, Igeral_proceedings, SE_journals, SE_proceedings, SE_a1_a4, SE_a1, 
			SE_a2, SE_a3, SE_a4, SE_b1_b4, SE_b1, SE_b2, SE_b3, SE_b4, SE_others, percentages_SE, 
			percentages, Irestrito_medio, Igeral_medio, Irestrito_medio_journals, Igeral_medio_journals, 
			Irestrito_medio_proceedings, Igeral_medio_proceedings):
		# Build table
		type_qualis = ["Periódicos", "Anais", "A1-A4", "A1", "A2", "A3", "A4", "B1-B4", "B1", "B2", "B3", "B4", "Outros"]
		table = {f"Tipo/Qualis {self.qualis_year}": type_qualis, "Quantidade": [], "Porcentagem": [], 'Quantidade com alunos/egressos':[], "% Alunos/Egressos":[]}

		table[f"Tipo/Qualis {self.qualis_year}"].append(None)
		table[f"Tipo/Qualis {self.qualis_year}"].append("Índice")
		table[f"Tipo/Qualis {self.qualis_year}"].append("Irestrito")
		table[f"Tipo/Qualis {self.qualis_year}"].append("Igeral")
		table[f"Tipo/Qualis {self.qualis_year}"].append("Irestrito Periódicos")
		table[f"Tipo/Qualis {self.qualis_year}"].append("Igeral Periódicos")
		table[f"Tipo/Qualis {self.qualis_year}"].append("Irestrito Anais")
		table[f"Tipo/Qualis {self.qualis_year}"].append("Igeral Anais")

		table["Quantidade"].append(journals)
		table["Quantidade"].append(proceedings)
		table["Quantidade"].append(a1_a4)
		table["Quantidade"].append(a1)
		table["Quantidade"].append(a2)
		table["Quantidade"].append(a3)
		table["Quantidade"].append(a4)
		table["Quantidade"].append(b1_b4)
		table["Quantidade"].append(b1)
		table["Quantidade"].append(b2)
		table["Quantidade"].append(b3)
		table["Quantidade"].append(b4)
		table["Quantidade"].append(others)
		table["Quantidade"].append(None)
		table["Quantidade"].append("Acumulado")
		table["Quantidade"].append(Irestrito)
		table["Quantidade"].append(Igeral)
		table["Quantidade"].append(Irestrito_journals)
		table["Quantidade"].append(Igeral_journals)
		table["Quantidade"].append(Irestrito_proceedings)
		table["Quantidade"].append(Igeral_proceedings)

		table['Quantidade com alunos/egressos'].append(SE_journals)
		table['Quantidade com alunos/egressos'].append(SE_proceedings)
		table['Quantidade com alunos/egressos'].append(SE_a1_a4)
		table['Quantidade com alunos/egressos'].append(SE_a1)
		table['Quantidade com alunos/egressos'].append(SE_a2)
		table['Quantidade com alunos/egressos'].append(SE_a3)
		table['Quantidade com alunos/egressos'].append(SE_a4)
		table['Quantidade com alunos/egressos'].append(SE_b1_b4)
		table['Quantidade com alunos/egressos'].append(SE_b1)
		table['Quantidade com alunos/egressos'].append(SE_b2)
		table['Quantidade com alunos/egressos'].append(SE_b3)
		table['Quantidade com alunos/egressos'].append(SE_b4)
		table['Quantidade com alunos/egressos'].append(SE_others)
		table['Quantidade com alunos/egressos'].append(None)
		table['Quantidade com alunos/egressos'].append(None)
		table['Quantidade com alunos/egressos'].append(None)
		table['Quantidade com alunos/egressos'].append(None)
		table['Quantidade com alunos/egressos'].append(None)
		table['Quantidade com alunos/egressos'].append(None)
		table['Quantidade com alunos/egressos'].append(None)
		table['Quantidade com alunos/egressos'].append(None)

		table["% Alunos/Egressos"] = percentages_SE
		table["% Alunos/Egressos"].append(None)
		table["% Alunos/Egressos"].append(None)
		table["% Alunos/Egressos"].append(None)
		table["% Alunos/Egressos"].append(None)
		table["% Alunos/Egressos"].append(None)
		table["% Alunos/Egressos"].append(None)
		table["% Alunos/Egressos"].append(None)
		table["% Alunos/Egressos"].append(None)

		table["Porcentagem"] = percentages
		table["Porcentagem"].append(None)
		if self.general:
			table["Porcentagem"].append("Média por docente")
			table["Porcentagem"].append(Irestrito_medio)
			table["Porcentagem"].append(Igeral_medio)
			table["Porcentagem"].append(Irestrito_medio_journals)
			table["Porcentagem"].append(Igeral_medio_journals)
			table["Porcentagem"].append(Irestrito_medio_proceedings)
			table["Porcentagem"].append(Igeral_medio_proceedings)
		else:
			table["Porcentagem"].append(None)
			table["Porcentagem"].append(None)
			table["Porcentagem"].append(None)
			table["Porcentagem"].append(None)
			table["Porcentagem"].append(None)
			table["Porcentagem"].append(None)
			table["Porcentagem"].append(None)

		return table


	def build_table_2019_separated(self, a1_a4, a1, a2, a3, a4, b1_b4, b1, b2, b3, b4, others, 
		Irestrito, Igeral, SE_a1_a4, SE_a1, SE_a2, SE_a3, SE_a4, SE_b1_b4, SE_b1, SE_b2, SE_b3, SE_b4, 
		SE_others, percentages_SE, percentages, Irestrito_medio, Igeral_medio):
		# Build table
		type_qualis = ["A1-A4", "A1", "A2", "A3", "A4", "B1-B4", "B1", "B2", "B3", "B4", "Outros"]
		table = {f"Tipo/Qualis {self.qualis_year}": type_qualis, "Quantidade": [], "Porcentagem": [], 'Quantidade com alunos/egressos':[], "% Alunos/Egressos":[]}

		table[f"Tipo/Qualis {self.qualis_year}"].append(None)
		table[f"Tipo/Qualis {self.qualis_year}"].append("Índice")
		table[f"Tipo/Qualis {self.qualis_year}"].append("Irestrito")
		table[f"Tipo/Qualis {self.qualis_year}"].append("Igeral")

		table["Quantidade"].append(a1_a4)
		table["Quantidade"].append(a1)
		table["Quantidade"].append(a2)
		table["Quantidade"].append(a3)
		table["Quantidade"].append(a4)
		table["Quantidade"].append(b1_b4)
		table["Quantidade"].append(b1)
		table["Quantidade"].append(b2)
		table["Quantidade"].append(b3)
		table["Quantidade"].append(b4)
		table["Quantidade"].append(others)
		table["Quantidade"].append(None)
		table["Quantidade"].append("Acumulado")
		table["Quantidade"].append(Irestrito)
		table["Quantidade"].append(Igeral)

		table['Quantidade com alunos/egressos'].append(SE_a1_a4)
		table['Quantidade com alunos/egressos'].append(SE_a1)
		table['Quantidade com alunos/egressos'].append(SE_a2)
		table['Quantidade com alunos/egressos'].append(SE_a3)
		table['Quantidade com alunos/egressos'].append(SE_a4)
		table['Quantidade com alunos/egressos'].append(SE_b1_b4)
		table['Quantidade com alunos/egressos'].append(SE_b1)
		table['Quantidade com alunos/egressos'].append(SE_b2)
		table['Quantidade com alunos/egressos'].append(SE_b3)
		table['Quantidade com alunos/egressos'].append(SE_b4)
		table['Quantidade com alunos/egressos'].append(SE_others)
		table['Quantidade com alunos/egressos'].append(None)
		table['Quantidade com alunos/egressos'].append(None)
		table['Quantidade com alunos/egressos'].append(None)
		table['Quantidade com alunos/egressos'].append(None)

		table["% Alunos/Egressos"] = percentages_SE
		table["% Alunos/Egressos"].append(None)
		table["% Alunos/Egressos"].append(None)
		table["% Alunos/Egressos"].append(None)
		table["% Alunos/Egressos"].append(None)

		table["Porcentagem"] = percentages
		table["Porcentagem"].append(None)
		if self.general:
			table["Porcentagem"].append("Média por docente")
			table["Porcentagem"].append(Irestrito_medio)
			table["Porcentagem"].append(Igeral_medio)
		else:
			table["Porcentagem"].append(None)
			table["Porcentagem"].append(None)
			table["Porcentagem"].append(None)

		return table

	def get_irestrito_igeral_2016(self, a1, a2, b1, b2, b3, b4, b5):
		Irestrito = (a1 + a2*0.85 + b1*0.7)
		if Irestrito != 0:
			Irestrito = round(Irestrito, 2)

		Igeral = (a1 + a2*0.85 + b1*0.7 + b2*0.5 + b3*0.2 + b4*0.1 + b5*0.05)
		if Igeral != 0:
			Igeral = round(Igeral, 2)

		return (Irestrito, Igeral)

	def get_irestrito_igeral_2019(self, a1, a2, a3, a4, b1, b2, b3, b4):
		Irestrito = a1 + (a2 * 0.875) + (a3 * 0.75) + (a4 * 0.625)
		if Irestrito != 0:
			Irestrito = round(Irestrito, 2)

		Igeral = Irestrito + (b1 * 0.5) + (b2 * 0.2) + (b3 * 0.1) + (b4 * 0.05)
		if Igeral != 0:
			Igeral = round(Igeral, 2)

		return (Irestrito, Igeral)


	def apply_3x1_2016(self, a1_journals, a2_journals, b1_journals, b2_journals, b3_journals, b4_journals, b5_journals, 
		a1_proceedings, a2_proceedings, b1_proceedings, b2_proceedings, b3_proceedings, b4_proceedings, b5_proceedings):
		slots = {'EA1':a1_journals*3, 'EA2':a2_journals*3, 'EB1':b1_journals*3, 'EB2':b2_journals*3, 
		'EB3':b3_journals*3, 'EB4':b4_journals*3, 'EB5':b5_journals*3}
		events_qualis = {'EA1':a1_proceedings, 'EA2':a2_proceedings, 'EB1':b1_proceedings, 'EB2':b2_proceedings, 
		'EB3':b3_proceedings, 'EB4':b4_proceedings, 'EB5':b5_proceedings}
		
		remainder = 0
		for key in slots.keys():
			slots[key] += remainder
			remainder = 0
			if events_qualis[key] >= slots[key]:
				events_qualis[key] = slots[key]
			else:
				remainder += slots[key] - events_qualis[key]

		a1_total = a1_journals + events_qualis['EA1']
		a2_total = a2_journals + events_qualis['EA2']
		b1_total = b1_journals + events_qualis['EB1']
		b2_total = b2_journals + events_qualis['EB2']
		b3_total = b3_journals + events_qualis['EB3']
		b4_total = b4_journals + events_qualis['EB4']
		b5_total = b5_journals + events_qualis['EB5']

		Irestrito_3x1_proceedings, Igeral_3x1_proceedings = self.get_irestrito_igeral_2016(events_qualis['EA1'], events_qualis['EA2'], events_qualis['EB1'], events_qualis['EB2'], events_qualis['EB3'], events_qualis['EB4'], events_qualis['EB5'])
		Irestrito_3x1_total, Igeral_3x1_total = self.get_irestrito_igeral_2016(a1_total, a2_total, b1_total, b2_total, b3_total, b4_total, b5_total)

		return (Irestrito_3x1_proceedings, Igeral_3x1_proceedings, Irestrito_3x1_total, Igeral_3x1_total)

	def apply_3x1_2019(self, a1_journals, a2_journals, a3_journals, a4_journals, b1_journals, b2_journals, b3_journals, b4_journals, 
		a1_proceedings, a2_proceedings, a3_proceedings, a4_proceedings, b1_proceedings, b2_proceedings, b3_proceedings, b4_proceedings):
		slots = {'EA1':a1_journals*3, 'EA2':a2_journals*3, 'EA3':a3_journals*3, 'EA4':a4_journals*3, 
		'EB1':b1_journals*3, 'EB2':b2_journals*3, 'EB3':b3_journals*3, 'EB4':b4_journals*3}
		events_qualis = {'EA1':a1_proceedings, 'EA2':a2_proceedings, 'EA3':a3_proceedings, 'EA4':a4_proceedings, 
		'EB1':b1_proceedings, 'EB2':b2_proceedings, 'EB3':b3_proceedings, 'EB4':b4_proceedings}
		
		remainder = 0
		for key in slots.keys():
			slots[key] += remainder
			remainder = 0
			if events_qualis[key] >= slots[key]:
				events_qualis[key] = slots[key]
			else:
				remainder += slots[key] - events_qualis[key]

		a1_total = a1_journals + events_qualis['EA1']
		a2_total = a2_journals + events_qualis['EA2']
		a3_total = a3_journals + events_qualis['EA3']
		a4_total = a4_journals + events_qualis['EA4']
		b1_total = b1_journals + events_qualis['EB1']
		b2_total = b2_journals + events_qualis['EB2']
		b3_total = b3_journals + events_qualis['EB3']
		b4_total = b4_journals + events_qualis['EB4']

		Irestrito_3x1_proceedings, Igeral_3x1_proceedings = self.get_irestrito_igeral_2019(events_qualis['EA1'], events_qualis['EA2'], events_qualis['EA3'], events_qualis['EA4'], events_qualis['EB1'], events_qualis['EB2'], events_qualis['EB3'], events_qualis['EB4'])
		Irestrito_3x1_total, Igeral_3x1_total = self.get_irestrito_igeral_2019(a1_total, a2_total, a3_total, a4_total, b1_total, b2_total, b3_total, b4_total)

		return (Irestrito_3x1_proceedings, Igeral_3x1_proceedings, Irestrito_3x1_total, Igeral_3x1_total)


	def get_irestritos(self, Irestrito, Irestrito_journals, Irestrito_proceedings, Irestrito_3x1_proceedings, Irestrito_3x1_total):
		self.irestritos = {'Total com trava':None, 'Total sem trava':None, 'Anais com trava':None, 'Anais sem trava':None, 'Periódicos':None}
		self.irestritos['Total com trava'] = Irestrito_3x1_total
		self.irestritos['Total sem trava'] = Irestrito
		self.irestritos['Anais com trava'] = Irestrito_3x1_proceedings
		self.irestritos['Anais sem trava'] = Irestrito_proceedings
		self.irestritos['Periódicos'] = Irestrito_journals


	def get_igerais(self, Igeral, Igeral_journals, Igeral_proceedings, Igeral_3x1_proceedings, Igeral_3x1_total):
		self.igerais = {'Total com trava':None, 'Total sem trava':None, 'Anais com trava':None, 'Anais sem trava':None, 'Periódicos':None}
		self.igerais['Total com trava'] = Igeral_3x1_total
		self.igerais['Total sem trava'] = Igeral
		self.igerais['Anais com trava'] = Igeral_3x1_proceedings
		self.igerais['Anais sem trava'] = Igeral_proceedings
		self.igerais['Periódicos'] = Igeral_journals
		
	def get_indicators_2016(self): 
		data_frame = pd.DataFrame(self.info)

		# Get total of publications that are not books or chapters
		total_articles = 0
		for i in data_frame["Tipo"]:
			if i != "Livros" and i != "Capítulos":
				total_articles += 1
		if total_articles != 0:
			perc_aux = 100/total_articles
		else:
			perc_aux = 0

		journals_df = data_frame.loc[data_frame["Tipo"] == "Periódico"] # Get all publications on journals
		journals, SE_journals, perc_journals, perc_SE_journals = self.calculate_amount(journals_df, perc_aux) # Perform calculations 
		# (amount of journals, amount of journals with students or egress as authors, percentage of publications on journals, percentage of publications on journals with students or egress as authors)
		if journals != 0:
			perc_aux_journals = 100/journals
		else:
			perc_aux_journals = 0


		proceedings_df = data_frame.loc[data_frame["Tipo"] == "Anais"] # Get all publications on events
		proceedings, SE_proceedings, perc_proceedings, perc_SE_proceedings = self.calculate_amount(proceedings_df, perc_aux) # Perform calculations  
		if proceedings != 0:
			perc_aux_proceedings = 100/proceedings
		else:
			perc_aux_proceedings = 0

		# ==========================================================================================================

		a1 = data_frame.loc[data_frame[f"Qualis {self.qualis_year}"] == "A1"] # Get all publications with "A1" Qualis
		a1, SE_a1, perc_a1, perc_SE_a1 = self.calculate_amount(a1, perc_aux) # Perform calculations 

		a1_journals = journals_df.loc[journals_df[f"Qualis {self.qualis_year}"] == "A1"] # Get all journals with "A1" Qualis
		a1_journals, SE_a1_journals, perc_a1_journals, perc_SE_a1_journals = self.calculate_amount(a1_journals, perc_aux_journals) # Perform calculations 

		a1_proceedings = proceedings_df.loc[proceedings_df[f"Qualis {self.qualis_year}"] == "A1"] # Get all proceedings with "A1" Qualis
		a1_proceedings, SE_a1_proceedings, perc_a1_proceedings, perc_SE_a1_proceedings = self.calculate_amount(a1_proceedings, perc_aux_proceedings) # Perform calculations 

		# ==========================================================================================================
		a2 = data_frame.loc[data_frame[f"Qualis {self.qualis_year}"] == "A2"] # Get all publications with "A2" Qualis
		a2, SE_a2, perc_a2, perc_SE_a2 = self.calculate_amount(a2, perc_aux) # Perform calculations 

		a2_journals = journals_df.loc[journals_df[f"Qualis {self.qualis_year}"] == "A2"] # Get all journals with "A2" Qualis
		a2_journals, SE_a2_journals, perc_a2_journals, perc_SE_a2_journals = self.calculate_amount(a2_journals, perc_aux_journals) # Perform calculations 

		a2_proceedings = proceedings_df.loc[proceedings_df[f"Qualis {self.qualis_year}"] == "A2"] # Get all proceedings with "A2" Qualis
		a2_proceedings, SE_a2_proceedings, perc_a2_proceedings, perc_SE_a2_proceedings = self.calculate_amount(a2_proceedings, perc_aux_proceedings) # Perform calculations 

		# ==========================================================================================================

		b1 = data_frame.loc[data_frame[f"Qualis {self.qualis_year}"] == "B1"] # Get all publications with "B1" Qualis
		b1, SE_b1, perc_b1, perc_SE_b1 = self.calculate_amount(b1, perc_aux) # Perform calculations 
		
		b1_journals = journals_df.loc[journals_df[f"Qualis {self.qualis_year}"] == "B1"] # Get all journals with "B1" Qualis
		b1_journals, SE_b1_journals, perc_b1_journals, perc_SE_b1_journals = self.calculate_amount(b1_journals, perc_aux_journals) # Perform calculations 

		b1_proceedings = proceedings_df.loc[proceedings_df[f"Qualis {self.qualis_year}"] == "B1"] # Get all proceedings with "B1" Qualis
		b1_proceedings, SE_b1_proceedings, perc_b1_proceedings, perc_SE_b1_proceedings = self.calculate_amount(b1_proceedings, perc_aux_proceedings) # Perform calculations 

		# ==========================================================================================================

		b2 = data_frame.loc[data_frame[f"Qualis {self.qualis_year}"] == "B2"] # Get all publications with "B2" Qualis
		b2, SE_b2, perc_b2, perc_SE_b2 = self.calculate_amount(b2, perc_aux) # Perform calculations 
		
		b2_journals = journals_df.loc[journals_df[f"Qualis {self.qualis_year}"] == "B2"] # Get all journals with "B2" Qualis
		b2_journals, SE_b2_journals, perc_b2_journals, perc_SE_b2_journals = self.calculate_amount(b2_journals, perc_aux_journals) # Perform calculations 

		b2_proceedings = proceedings_df.loc[proceedings_df[f"Qualis {self.qualis_year}"] == "B2"] # Get all proceedings with "B2" Qualis
		b2_proceedings, SE_b2_proceedings, perc_b2_proceedings, perc_SE_b2_proceedings = self.calculate_amount(b2_proceedings, perc_aux_proceedings) # Perform calculations 

		# ==========================================================================================================

		b3 = data_frame.loc[data_frame[f"Qualis {self.qualis_year}"] == "B3"] # Get all publications with "B3" Qualis
		b3, SE_b3, perc_b3, perc_SE_b3 = self.calculate_amount(b3, perc_aux) # Perform calculations 
		
		b3_journals = journals_df.loc[journals_df[f"Qualis {self.qualis_year}"] == "B3"] # Get all journals with "B3" Qualis
		b3_journals, SE_b3_journals, perc_b3_journals, perc_SE_b3_journals = self.calculate_amount(b3_journals, perc_aux_journals) # Perform calculations 

		b3_proceedings = proceedings_df.loc[proceedings_df[f"Qualis {self.qualis_year}"] == "B3"] # Get all proceedings with "B3" Qualis
		b3_proceedings, SE_b3_proceedings, perc_b3_proceedings, perc_SE_b3_proceedings = self.calculate_amount(b3_proceedings, perc_aux_proceedings) # Perform calculations 

		# ==========================================================================================================

		b4 = data_frame.loc[data_frame[f"Qualis {self.qualis_year}"] == "B4"] # Get all publications with "B4" Qualis
		b4, SE_b4, perc_b4, perc_SE_b4 = self.calculate_amount(b4, perc_aux) # Perform calculations 
		
		b4_journals = journals_df.loc[journals_df[f"Qualis {self.qualis_year}"] == "B4"] # Get all journals with "B4" Qualis
		b4_journals, SE_b4_journals, perc_b4_journals, perc_SE_b4_journals = self.calculate_amount(b4_journals, perc_aux_journals) # Perform calculations 

		b4_proceedings = proceedings_df.loc[proceedings_df[f"Qualis {self.qualis_year}"] == "B4"] # Get all proceedings with "B4" Qualis
		b4_proceedings, SE_b4_proceedings, perc_b4_proceedings, perc_SE_b4_proceedings = self.calculate_amount(b4_proceedings, perc_aux_proceedings) # Perform calculations 

		# ==========================================================================================================
		
		b5 = data_frame.loc[data_frame[f"Qualis {self.qualis_year}"] == "B5"] # Get all publications with "B4" Qualis
		b5, SE_b5, perc_b5, perc_SE_b5 = self.calculate_amount(b5, perc_aux) # Perform calculations 
		
		b5_journals = journals_df.loc[journals_df[f"Qualis {self.qualis_year}"] == "B5"] # Get all journals with "B5" Qualis
		b5_journals, SE_b5_journals, perc_b5_journals, perc_SE_b5_journals = self.calculate_amount(b5_journals, perc_aux_journals) # Perform calculations 

		b5_proceedings = proceedings_df.loc[proceedings_df[f"Qualis {self.qualis_year}"] == "B5"] # Get all proceedings with "B5" Qualis
		b5_proceedings, SE_b5_proceedings, perc_b5_proceedings, perc_SE_b5_proceedings = self.calculate_amount(b5_proceedings, perc_aux_proceedings) # Perform calculations 

		# ==========================================================================================================

		# A1-B1 (all merged)
		a1_b1 = a1 + a2 + b1
		SE_a1_b1 = SE_a1 + SE_a2 + SE_b1
		perc_a1_b1 = f"{perc_aux * a1_b1:.2f}%"
		try:
			perc_SE_a1_b1 = f"{100/a1_b1 * SE_a1_b1:.2f}%"
		except ZeroDivisionError:
			perc_SE_a1_b1 = "0%"

		# A1-B1 (all merged) - Journals
		a1_b1_journals = a1_journals + a2_journals + b1_journals
		SE_a1_b1_journals = SE_a1_journals + SE_a2_journals + SE_b1_journals
		perc_a1_b1_journals = f"{perc_aux_journals * a1_b1_journals:.2f}%"
		try:
			perc_SE_a1_b1_journals = f"{100/a1_b1_journals * SE_a1_b1_journals:.2f}%"
		except ZeroDivisionError:
			perc_SE_a1_b1_journals = "0%"

		# A1-B1 (all merged) - Proceedings
		a1_b1_proceedings = a1_proceedings + a2_proceedings + b1_proceedings
		SE_a1_b1_proceedings = SE_a1_proceedings + SE_a2_proceedings + SE_b1_proceedings
		perc_a1_b1_proceedings = f"{perc_aux_proceedings * a1_b1_proceedings:.2f}%"
		try:
			perc_SE_a1_b1_proceedings = f"{100/a1_b1_proceedings * SE_a1_b1_proceedings:.2f}%"
		except ZeroDivisionError:
			perc_SE_a1_b1_proceedings = "0%"

		# ==========================================================================================================

		# B2-B5 (all merged)
		b2_b5 = b2 + b3 + b4 + b5
		SE_b2_b5 = SE_b2 + SE_b3 + SE_b4 + SE_b5
		perc_b2_b5 = f"{perc_aux * b2_b5:.2f}%"
		try:
			perc_SE_b2_b5 = f"{100/b2_b5 * SE_b2_b5:.2f}%"
		except ZeroDivisionError:
			perc_SE_b2_b5 = "0%"

		# B2-B5 (all merged) - Journals
		b2_b5_journals = b2_journals + b3_journals + b4_journals + b5_journals
		SE_b2_b5_journals = SE_b2_journals + SE_b3_journals + SE_b4_journals + SE_b5_journals
		perc_b2_b5_journals = f"{perc_aux_journals * b2_b5_journals:.2f}%"
		try:
			perc_SE_b2_b5_journals = f"{100/b2_b5_journals * SE_b2_b5_journals:.2f}%"
		except ZeroDivisionError:
			perc_SE_b2_b5_journals = "0%"

		# B2-B5 (all merged) - Proceedings
		b2_b5_proceedings = b2_proceedings + b3_proceedings + b4_proceedings + b5_proceedings
		SE_b2_b5_proceedings = SE_b2_proceedings + SE_b3_proceedings + SE_b4_proceedings + SE_b5_proceedings
		perc_b2_b5_proceedings = f"{perc_aux_proceedings * b2_b5_proceedings:.2f}%"
		try:
			perc_SE_b2_b5_proceedings = f"{100/b2_b5_proceedings * SE_b2_b5_proceedings:.2f}%"
		except ZeroDivisionError:
			perc_SE_b2_b5_proceedings = "0%"

		# ==========================================================================================================

		# Other - Not in A1-B1 or B2-B5
		others = data_frame.loc[((data_frame[f"Qualis {self.qualis_year}"] != "A1") & (data_frame[f"Qualis {self.qualis_year}"] != "A2") & (data_frame[f"Qualis {self.qualis_year}"] != "A3") & (data_frame[f"Qualis {self.qualis_year}"] != "A4") & (data_frame["Tipo"] != "Livros") & (data_frame["Tipo"] != "Capítulos"))]
		others = others.loc[((others[f"Qualis {self.qualis_year}"] != "B1") & (others[f"Qualis {self.qualis_year}"] != "B2") & (others[f"Qualis {self.qualis_year}"] != "B3") & (others[f"Qualis {self.qualis_year}"] != "B4")  & (others[f"Qualis {self.qualis_year}"] != "B5"))]
		others, SE_others, perc_others, perc_SE_others = self.calculate_amount(others, perc_aux) # Perform calculations 

		# Other - Not in A1-B1 or B2-B5 - Journals
		others_journals = journals_df.loc[((journals_df[f"Qualis {self.qualis_year}"] != "A1") & (journals_df[f"Qualis {self.qualis_year}"] != "A2") & (journals_df[f"Qualis {self.qualis_year}"] != "A3") & (journals_df[f"Qualis {self.qualis_year}"] != "A4") & (journals_df["Tipo"] != "Livros") & (journals_df["Tipo"] != "Capítulos"))]
		others_journals = others_journals.loc[((others_journals[f"Qualis {self.qualis_year}"] != "B1") & (others_journals[f"Qualis {self.qualis_year}"] != "B2") & (others_journals[f"Qualis {self.qualis_year}"] != "B3") & (others_journals[f"Qualis {self.qualis_year}"] != "B4")  & (others_journals[f"Qualis {self.qualis_year}"] != "B5"))]
		others_journals, SE_others_journals, perc_others_journals, perc_SE_others_journals = self.calculate_amount(others_journals, perc_aux_journals) # Perform calculations 
		
		# Other - Not in A1-B1 or B2-B5 - Proceedings
		others_proceedings = proceedings_df.loc[((proceedings_df[f"Qualis {self.qualis_year}"] != "A1") & (proceedings_df[f"Qualis {self.qualis_year}"] != "A2") & (proceedings_df[f"Qualis {self.qualis_year}"] != "A3") & (proceedings_df[f"Qualis {self.qualis_year}"] != "A4") & (proceedings_df["Tipo"] != "Livros") & (proceedings_df["Tipo"] != "Capítulos"))]
		others_proceedings = others_proceedings.loc[((others_proceedings[f"Qualis {self.qualis_year}"] != "B1") & (others_proceedings[f"Qualis {self.qualis_year}"] != "B2") & (others_proceedings[f"Qualis {self.qualis_year}"] != "B3") & (others_proceedings[f"Qualis {self.qualis_year}"] != "B4")  & (others_proceedings[f"Qualis {self.qualis_year}"] != "B5"))]
		others_proceedings, SE_others_proceedings, perc_others_proceedings, perc_SE_others_proceedings = self.calculate_amount(others_proceedings, perc_aux_proceedings) # Perform calculations 

		# ==========================================================================================================

		percentages = [perc_journals, perc_proceedings, perc_a1_b1, perc_a1, perc_a2, perc_b1, perc_b2_b5, perc_b2, perc_b3, perc_b4, perc_b5, perc_others]
		percentages_SE = [perc_SE_journals, perc_SE_proceedings, perc_SE_a1_b1, perc_SE_a1, perc_SE_a2, perc_SE_b1, perc_SE_b2_b5, perc_SE_b2, perc_SE_b3, perc_SE_b4, perc_SE_b5, perc_SE_others]

		percentages_journals = [perc_a1_b1_journals, perc_a1_journals, perc_a2_journals, perc_b1_journals, perc_b2_b5_journals, perc_b2_journals, perc_b3_journals, perc_b4_journals, perc_b5_journals, perc_others_journals]
		percentages_SE_journals = [perc_SE_a1_b1_journals, perc_SE_a1_journals, perc_SE_a2_journals, perc_SE_b1_journals, perc_SE_b2_b5_journals, perc_SE_b2_journals, perc_SE_b3_journals, perc_SE_b4_journals, perc_SE_b5_journals, perc_SE_others_journals]
		
		percentages_proceedings = [perc_a1_b1_proceedings, perc_a1_proceedings, perc_a2_proceedings, perc_b1_proceedings, perc_b2_b5_proceedings, perc_b2_proceedings, perc_b3_proceedings, perc_b4_proceedings, perc_b5_proceedings, perc_others_proceedings]
		percentages_SE_proceedings = [perc_SE_a1_b1_proceedings, perc_SE_a1_proceedings, perc_SE_a2_proceedings, perc_SE_b1_proceedings, perc_SE_b2_b5_proceedings, perc_SE_b2_proceedings, perc_SE_b3_proceedings, perc_SE_b4_proceedings, perc_SE_b5_proceedings, perc_SE_others_proceedings]

		# ==========================================================================================================


		Irestrito, Igeral = self.get_irestrito_igeral_2016(a1, a2, b1, b2, b3, b4, b5)
		if Irestrito != 0:
			Irestrito_medio = round((Irestrito/ND), 2)
		else:
		 	Irestrito_medio = 0
		if Igeral != 0:
			Igeral_medio = round((Igeral/ND), 2)
		else:
			Igeral_medio = 0

		Irestrito_journals, Igeral_journals = self.get_irestrito_igeral_2016(a1_journals, a2_journals, b1_journals, b2_journals, b3_journals, b4_journals, b5_journals)
		if Irestrito_journals != 0:
			Irestrito_medio_journals = round((Irestrito_journals/ND), 2)
		else:
			Irestrito_medio_journals = 0
		if Igeral_journals != 0:
			Igeral_medio_journals = round((Igeral_journals/ND), 2)
		else:
			Igeral_medio_journals = 0

		Irestrito_proceedings, Igeral_proceedings = self.get_irestrito_igeral_2016(a1_proceedings, a2_proceedings, b1_proceedings, b2_proceedings, b3_proceedings, b4_proceedings, b5_proceedings)
		if Irestrito_proceedings != 0:
			Irestrito_medio_proceedings = round((Irestrito_proceedings/ND), 2)
		else:
			Irestrito_medio_proceedings = 0
		if Igeral_proceedings != 0:
			Igeral_medio_proceedings = round((Igeral_proceedings/ND), 2)
		else:
			Igeral_medio_proceedings = 0

		# ==========================================================================================================

		table_general = self.build_table_2016_general(journals, proceedings, a1_b1, a1, a2, b1, 
			b2_b5, b2, b3, b4, b5, others, Irestrito, Irestrito_journals, Irestrito_proceedings, 
			Igeral, Igeral_journals, Igeral_proceedings, SE_journals, SE_proceedings, SE_a1_b1, 
			SE_a1, SE_a2, SE_b1, SE_b2_b5, SE_b2, SE_b3, SE_b4, SE_b5, SE_others, percentages_SE, 
			percentages, Irestrito_medio, Irestrito_medio_journals, Irestrito_medio_proceedings, 
			Igeral_medio, Igeral_medio_journals, Igeral_medio_proceedings)

		table_journals = self.build_table_2016_separated(a1_b1_journals, a1_journals, a2_journals, b1_journals, 
			b2_b5_journals, b2_journals, b3_journals, b4_journals, b5_journals, others_journals, Irestrito_journals, 
			Igeral_journals, SE_a1_b1_journals, SE_a1_journals, SE_a2_journals, SE_b1_journals, SE_b2_b5_journals, 
			SE_b2_journals, SE_b3_journals, SE_b4_journals, SE_b5_journals, SE_others_journals, percentages_SE_journals, 
			percentages_journals, Irestrito_medio_journals, Igeral_medio_journals)

		table_proceedings = self.build_table_2016_separated(a1_b1_proceedings, a1_proceedings, a2_proceedings, b1_proceedings, 
			b2_b5_proceedings, b2_proceedings, b3_proceedings, b4_proceedings, b5_proceedings, others_proceedings, Irestrito_proceedings, 
			Igeral_proceedings, SE_a1_b1_proceedings, SE_a1_proceedings, SE_a2_proceedings, SE_b1_proceedings, SE_b2_b5_proceedings, 
			SE_b2_proceedings, SE_b3_proceedings, SE_b4_proceedings, SE_b5_proceedings, SE_others_proceedings, percentages_SE_proceedings, 
			percentages_proceedings, Irestrito_medio_proceedings, Igeral_medio_proceedings)
		

		if self.general == True:
			Irestrito_3x1_proceedings, Igeral_3x1_proceedings, Irestrito_3x1_total, Igeral_3x1_total = self.apply_3x1_2016(a1_journals, a2_journals, 
				b1_journals, b2_journals, b3_journals, b4_journals, b5_journals, a1_proceedings, a2_proceedings, 
				b1_proceedings, b2_proceedings, b3_proceedings, b4_proceedings, b5_proceedings)

			self.get_irestritos(Irestrito, Irestrito_journals, Irestrito_proceedings, Irestrito_3x1_proceedings, Irestrito_3x1_total)
			self.get_igerais(Igeral, Igeral_journals, Igeral_proceedings, Igeral_3x1_proceedings, Igeral_3x1_total)

		return (pd.DataFrame(table_general), pd.DataFrame(table_journals), pd.DataFrame(table_proceedings))

	def get_indicators_2019(self): 
		data_frame = pd.DataFrame(self.info)

		# Get total of publications that are not books or chapters
		total_articles = 0
		for i in data_frame["Tipo"]:
			if i != "Livros" and i != "Capítulos":
				total_articles += 1
		if total_articles != 0:
			perc_aux = 100/total_articles
		else:
			perc_aux = 0

		journals_df = data_frame.loc[data_frame["Tipo"] == "Periódico"] # Get all publications on journals
		journals, SE_journals, perc_journals, perc_SE_journals = self.calculate_amount(journals_df, perc_aux) # Perform calculations 
		# (amount of journals, amount of journals with students or egress as authors, percentage of publications on journals, percentage of publications on journals with students or egress as authors)
		if journals != 0:
			perc_aux_journals = 100/journals
		else:
			perc_aux_journals = 0


		proceedings_df = data_frame.loc[data_frame["Tipo"] == "Anais"] # Get all publications on events
		proceedings, SE_proceedings, perc_proceedings, perc_SE_proceedings = self.calculate_amount(proceedings_df, perc_aux) # Perform calculations  
		if proceedings != 0:
			perc_aux_proceedings = 100/proceedings
		else:
			perc_aux_proceedings = 0
		
		# ==========================================================================================================

		a1 = data_frame.loc[data_frame[f"Qualis {self.qualis_year}"] == "A1"] # Get all publications with "A1" Qualis
		a1, SE_a1, perc_a1, perc_SE_a1 = self.calculate_amount(a1, perc_aux) # Perform calculations 

		a1_journals = journals_df.loc[journals_df[f"Qualis {self.qualis_year}"] == "A1"] # Get all journals with "A1" Qualis
		a1_journals, SE_a1_journals, perc_a1_journals, perc_SE_a1_journals = self.calculate_amount(a1_journals, perc_aux_journals) # Perform calculations 

		a1_proceedings = proceedings_df.loc[proceedings_df[f"Qualis {self.qualis_year}"] == "A1"] # Get all proceedings with "A1" Qualis
		a1_proceedings, SE_a1_proceedings, perc_a1_proceedings, perc_SE_a1_proceedings = self.calculate_amount(a1_proceedings, perc_aux_proceedings) # Perform calculations 

		# ==========================================================================================================

		a2 = data_frame.loc[data_frame[f"Qualis {self.qualis_year}"] == "A2"] # Get all publications with "A2" Qualis
		a2, SE_a2, perc_a2, perc_SE_a2 = self.calculate_amount(a2, perc_aux) # Perform calculations 

		a2_journals = journals_df.loc[journals_df[f"Qualis {self.qualis_year}"] == "A2"] # Get all journals with "A2" Qualis
		a2_journals, SE_a2_journals, perc_a2_journals, perc_SE_a2_journals = self.calculate_amount(a2_journals, perc_aux_journals) # Perform calculations 

		a2_proceedings = proceedings_df.loc[proceedings_df[f"Qualis {self.qualis_year}"] == "A2"] # Get all proceedings with "A2" Qualis
		a2_proceedings, SE_a2_proceedings, perc_a2_proceedings, perc_SE_a2_proceedings = self.calculate_amount(a2_proceedings, perc_aux_proceedings) # Perform calculations 

		# ==========================================================================================================

		a3 = data_frame.loc[data_frame[f"Qualis {self.qualis_year}"] == "A3"] # Get all publications with "A3" Qualis
		a3, SE_a3, perc_a3, perc_SE_a3 = self.calculate_amount(a3, perc_aux) # Perform calculations 

		a3_journals = journals_df.loc[journals_df[f"Qualis {self.qualis_year}"] == "A3"] # Get all journals with "A3" Qualis
		a3_journals, SE_a3_journals, perc_a3_journals, perc_SE_a3_journals = self.calculate_amount(a3_journals, perc_aux_journals) # Perform calculations 

		a3_proceedings = proceedings_df.loc[proceedings_df[f"Qualis {self.qualis_year}"] == "A3"] # Get all proceedings with "A3" Qualis
		a3_proceedings, SE_a3_proceedings, perc_a3_proceedings, perc_SE_a3_proceedings = self.calculate_amount(a3_proceedings, perc_aux_proceedings) # Perform calculations 

		# ==========================================================================================================

		a4 = data_frame.loc[data_frame[f"Qualis {self.qualis_year}"] == "A4"] # Get all publications with "A4" Qualis
		a4, SE_a4, perc_a4, perc_SE_a4 = self.calculate_amount(a4, perc_aux) # Perform calculations 

		a4_journals = journals_df.loc[journals_df[f"Qualis {self.qualis_year}"] == "A4"] # Get all journals with "A4" Qualis
		a4_journals, SE_a4_journals, perc_a4_journals, perc_SE_a4_journals = self.calculate_amount(a4_journals, perc_aux_journals) # Perform calculations 

		a4_proceedings = proceedings_df.loc[proceedings_df[f"Qualis {self.qualis_year}"] == "A4"] # Get all proceedings with "A4" Qualis
		a4_proceedings, SE_a4_proceedings, perc_a4_proceedings, perc_SE_a4_proceedings = self.calculate_amount(a4_proceedings, perc_aux_proceedings) # Perform calculations 

		# ==========================================================================================================

		b1 = data_frame.loc[data_frame[f"Qualis {self.qualis_year}"] == "B1"] # Get all publications with "B1" Qualis
		b1, SE_b1, perc_b1, perc_SE_b1 = self.calculate_amount(b1, perc_aux) # Perform calculations 
		
		b1_journals = journals_df.loc[journals_df[f"Qualis {self.qualis_year}"] == "B1"] # Get all journals with "B1" Qualis
		b1_journals, SE_b1_journals, perc_b1_journals, perc_SE_b1_journals = self.calculate_amount(b1_journals, perc_aux_journals) # Perform calculations 

		b1_proceedings = proceedings_df.loc[proceedings_df[f"Qualis {self.qualis_year}"] == "B1"] # Get all proceedings with "B1" Qualis
		b1_proceedings, SE_b1_proceedings, perc_b1_proceedings, perc_SE_b1_proceedings = self.calculate_amount(b1_proceedings, perc_aux_proceedings) # Perform calculations 

		# ==========================================================================================================

		b2 = data_frame.loc[data_frame[f"Qualis {self.qualis_year}"] == "B2"] # Get all publications with "B2" Qualis
		b2, SE_b2, perc_b2, perc_SE_b2 = self.calculate_amount(b2, perc_aux) # Perform calculations 
		
		b2_journals = journals_df.loc[journals_df[f"Qualis {self.qualis_year}"] == "B2"] # Get all journals with "B2" Qualis
		b2_journals, SE_b2_journals, perc_b2_journals, perc_SE_b2_journals = self.calculate_amount(b2_journals, perc_aux_journals) # Perform calculations 

		b2_proceedings = proceedings_df.loc[proceedings_df[f"Qualis {self.qualis_year}"] == "B2"] # Get all proceedings with "B2" Qualis
		b2_proceedings, SE_b2_proceedings, perc_b2_proceedings, perc_SE_b2_proceedings = self.calculate_amount(b2_proceedings, perc_aux_proceedings) # Perform calculations 

		# ==========================================================================================================

		b3 = data_frame.loc[data_frame[f"Qualis {self.qualis_year}"] == "B3"] # Get all publications with "B3" Qualis
		b3, SE_b3, perc_b3, perc_SE_b3 = self.calculate_amount(b3, perc_aux) # Perform calculations 
		
		b3_journals = journals_df.loc[journals_df[f"Qualis {self.qualis_year}"] == "B3"] # Get all journals with "B3" Qualis
		b3_journals, SE_b3_journals, perc_b3_journals, perc_SE_b3_journals = self.calculate_amount(b3_journals, perc_aux_journals) # Perform calculations 

		b3_proceedings = proceedings_df.loc[proceedings_df[f"Qualis {self.qualis_year}"] == "B3"] # Get all proceedings with "B3" Qualis
		b3_proceedings, SE_b3_proceedings, perc_b3_proceedings, perc_SE_b3_proceedings = self.calculate_amount(b3_proceedings, perc_aux_proceedings) # Perform calculations 

		# ==========================================================================================================

		b4 = data_frame.loc[data_frame[f"Qualis {self.qualis_year}"] == "B4"] # Get all publications with "B4" Qualis
		b4, SE_b4, perc_b4, perc_SE_b4 = self.calculate_amount(b4, perc_aux) # Perform calculations 
		
		b4_journals = journals_df.loc[journals_df[f"Qualis {self.qualis_year}"] == "B4"] # Get all journals with "B4" Qualis
		b4_journals, SE_b4_journals, perc_b4_journals, perc_SE_b4_journals = self.calculate_amount(b4_journals, perc_aux_journals) # Perform calculations 

		b4_proceedings = proceedings_df.loc[proceedings_df[f"Qualis {self.qualis_year}"] == "B4"] # Get all proceedings with "B4" Qualis
		b4_proceedings, SE_b4_proceedings, perc_b4_proceedings, perc_SE_b4_proceedings = self.calculate_amount(b4_proceedings, perc_aux_proceedings) # Perform calculations 

		# ==========================================================================================================
		
		# A1-A4 (all merged)
		a1_a4 = a1 + a2 + a3 + a4
		SE_a1_a4 = SE_a1 + SE_a2 + SE_a3 + SE_a4
		perc_a1_a4 = f"{perc_aux * a1_a4:.2f}%"
		try:
			perc_SE_a1_a4 = f"{100/a1_a4 * SE_a1_a4:.2f}%"
		except ZeroDivisionError:
			perc_SE_a1_a4 = "0%"

		# A1-A4 (all merged) - Journals
		a1_a4_journals = a1_journals + a2_journals + a3_journals + a4_journals
		SE_a1_a4_journals = SE_a1_journals + SE_a2_journals + SE_a3_journals + SE_a4_journals
		perc_a1_a4_journals = f"{perc_aux_journals * a1_a4_journals:.2f}%"
		try:
			perc_SE_a1_a4_journals = f"{100/a1_a4_journals * SE_a1_a4_journals:.2f}%"
		except ZeroDivisionError:
			perc_SE_a1_a4_journals = "0%"

		# A1-A4 (all merged) - Proceedings
		a1_a4_proceedings = a1_proceedings + a2_proceedings + a3_proceedings + a4_proceedings
		SE_a1_a4_proceedings = SE_a1_proceedings + SE_a2_proceedings + SE_a3_proceedings + SE_a4_proceedings
		perc_a1_a4_proceedings = f"{perc_aux_proceedings * a1_a4_proceedings:.2f}%"
		try:
			perc_SE_a1_a4_proceedings = f"{100/a1_a4_proceedings * SE_a1_a4_proceedings:.2f}%"
		except ZeroDivisionError:
			perc_SE_a1_a4_proceedings = "0%"
		
		# ==========================================================================================================

		# B1-B4 (all merged)
		b1_b4 = b1 + b2 + b3 + b4
		SE_b1_b4 = SE_b1 + SE_b2 + SE_b3 + SE_b4
		perc_b1_b4 = f"{perc_aux * b1_b4:.2f}%"
		try:
			perc_SE_b1_b4 = f"{100/b1_b4 * SE_b1_b4:.2f}%"
		except ZeroDivisionError:
			perc_SE_b1_b4 = "0%"

		# B1-B4 (all merged) - Journals
		b1_b4_journals = b1_journals + b2_journals + b3_journals + b4_journals
		SE_b1_b4_journals = SE_b1_journals + SE_b2_journals + SE_b3_journals + SE_b4_journals
		perc_b1_b4_journals = f"{perc_aux_journals * b1_b4_journals:.2f}%"
		try:
			perc_SE_b1_b4_journals = f"{100/b1_b4_journals * SE_b1_b4_journals:.2f}%"
		except ZeroDivisionError:
			perc_SE_b1_b4_journals = "0%"

		# B1-B4 (all merged) - Proceedings
		b1_b4_proceedings = b1_proceedings + b2_proceedings + b3_proceedings + b4_proceedings
		SE_b1_b4_proceedings = SE_b1_proceedings + SE_b2_proceedings + SE_b3_proceedings + SE_b4_proceedings
		perc_b1_b4_proceedings = f"{perc_aux_proceedings * b1_b4_proceedings:.2f}%"
		try:
			perc_SE_b1_b4_proceedings = f"{100/b1_b4_proceedings * SE_b1_b4_proceedings:.2f}%"
		except ZeroDivisionError:
			perc_SE_b1_b4_proceedings = "0%"

		# ==========================================================================================================

		# Other - Not in A1-A4 or B1-B4
		others = data_frame.loc[((data_frame[f"Qualis {self.qualis_year}"] != "A1") & (data_frame[f"Qualis {self.qualis_year}"] != "A2") & (data_frame[f"Qualis {self.qualis_year}"] != "A3") & (data_frame[f"Qualis {self.qualis_year}"] != "A4") & (data_frame["Tipo"] != "Livros") & (data_frame["Tipo"] != "Capítulos"))]
		others = others.loc[((others[f"Qualis {self.qualis_year}"] != "B1") & (others[f"Qualis {self.qualis_year}"] != "B2") & (others[f"Qualis {self.qualis_year}"] != "B3") & (others[f"Qualis {self.qualis_year}"] != "B4")  & (others[f"Qualis {self.qualis_year}"] != "B5"))]
		others, SE_others, perc_others, perc_SE_others = self.calculate_amount(others, perc_aux) # Perform calculations

		# Other - Not in A1-A4 or B1-B4 - Journals
		others_journals = journals_df.loc[((journals_df[f"Qualis {self.qualis_year}"] != "A1") & (journals_df[f"Qualis {self.qualis_year}"] != "A2") & (journals_df[f"Qualis {self.qualis_year}"] != "A3") & (journals_df[f"Qualis {self.qualis_year}"] != "A4") & (journals_df["Tipo"] != "Livros") & (journals_df["Tipo"] != "Capítulos"))]
		others_journals = others_journals.loc[((others_journals[f"Qualis {self.qualis_year}"] != "B1") & (others_journals[f"Qualis {self.qualis_year}"] != "B2") & (others_journals[f"Qualis {self.qualis_year}"] != "B3") & (others_journals[f"Qualis {self.qualis_year}"] != "B4")  & (others_journals[f"Qualis {self.qualis_year}"] != "B5"))]
		others_journals, SE_others_journals, perc_others_journals, perc_SE_others_journals = self.calculate_amount(others_journals, perc_aux_journals) # Perform calculations 
		
		# Other - Not in A1-A4 or B1-B4 - Proceedings
		others_proceedings = proceedings_df.loc[((proceedings_df[f"Qualis {self.qualis_year}"] != "A1") & (proceedings_df[f"Qualis {self.qualis_year}"] != "A2") & (proceedings_df[f"Qualis {self.qualis_year}"] != "A3") & (proceedings_df[f"Qualis {self.qualis_year}"] != "A4") & (proceedings_df["Tipo"] != "Livros") & (proceedings_df["Tipo"] != "Capítulos"))]
		others_proceedings = others_proceedings.loc[((others_proceedings[f"Qualis {self.qualis_year}"] != "B1") & (others_proceedings[f"Qualis {self.qualis_year}"] != "B2") & (others_proceedings[f"Qualis {self.qualis_year}"] != "B3") & (others_proceedings[f"Qualis {self.qualis_year}"] != "B4")  & (others_proceedings[f"Qualis {self.qualis_year}"] != "B5"))]
		others_proceedings, SE_others_proceedings, perc_others_proceedings, perc_SE_others_proceedings = self.calculate_amount(others_proceedings, perc_aux_proceedings) # Perform calculations 
 		
 		# ==========================================================================================================

		percentages = [perc_journals, perc_proceedings, perc_a1_a4, perc_a1, perc_a2, perc_a3, perc_a4, perc_b1_b4, perc_b1, perc_b2, perc_b3, perc_b4, perc_others]
		percentages_SE = [perc_SE_journals, perc_SE_proceedings, perc_SE_a1_a4, perc_SE_a1, perc_SE_a2, perc_SE_a3, perc_SE_a4, perc_SE_b1_b4, perc_SE_b1, perc_SE_b2, perc_SE_b3, perc_SE_b4, perc_SE_others]

		percentages_journals = [perc_a1_a4_journals, perc_a1_journals, perc_a2_journals, perc_a3_journals, perc_a4_journals, perc_b1_b4_journals, perc_b1_journals, perc_b2_journals, perc_b3_journals, perc_b4_journals, perc_others_journals]
		percentages_SE_journals = [perc_SE_a1_a4_journals, perc_SE_a1_journals, perc_SE_a2_journals, perc_SE_a3_journals, perc_SE_a4_journals, perc_SE_b1_b4_journals, perc_SE_b1_journals, perc_SE_b2_journals, perc_SE_b3_journals, perc_SE_b4_journals, perc_SE_others_journals]
		
		percentages_proceedings = [perc_a1_a4_proceedings, perc_a1_proceedings, perc_a2_proceedings, perc_a3_proceedings, perc_a4_proceedings, perc_b1_b4_proceedings, perc_b1_proceedings, perc_b2_proceedings, perc_b3_proceedings, perc_b4_proceedings, perc_others_proceedings]
		percentages_SE_proceedings = [perc_SE_a1_a4_proceedings, perc_SE_a1_proceedings, perc_SE_a2_proceedings, perc_SE_a3_proceedings, perc_SE_a4_proceedings, perc_SE_b1_b4_proceedings, perc_SE_b1_proceedings, perc_SE_b2_proceedings, perc_SE_b3_proceedings, perc_SE_b4_proceedings, perc_SE_others_proceedings]

		# ==========================================================================================================

		# Calculate Irestrito and Igeral

		Irestrito, Igeral = self.get_irestrito_igeral_2019(a1, a2, a3, a4, b1, b2, b3, b4)
		if Irestrito != 0:
			Irestrito_medio = round((Irestrito/ND), 2)
		else:
			Irestrito_medio = 0
		if Igeral != 0:
			Igeral_medio = round((Igeral/ND), 2)
		else:
			Igeral_medio = 0


		Irestrito_journals, Igeral_journals = self.get_irestrito_igeral_2019(a1_journals, a2_journals, a3_journals, a4_journals, b1_journals, b2_journals, b3_journals, b4_journals)
		if Irestrito_journals != 0:
			Irestrito_medio_journals = round((Irestrito_journals/ND), 2)
		else:
			Irestrito_medio_journals = 0
		if Igeral_journals != 0:
			Igeral_medio_journals = round((Igeral_journals/ND), 2)
		else:
			Igeral_medio_journals = 0
		

		Irestrito_proceedings, Igeral_proceedings = self.get_irestrito_igeral_2019(a1_proceedings, a2_proceedings, a3_proceedings, a4_proceedings, b1_proceedings, b2_proceedings, b3_proceedings, b4_proceedings)
		if Irestrito_proceedings != 0:
			Irestrito_medio_proceedings = round((Irestrito_proceedings/ND), 2)
		else:
			Irestrito_medio_proceedings = 0
		if Igeral_proceedings != 0:
			Igeral_medio_proceedings = round((Igeral_proceedings/ND), 2)
		else:
			Igeral_medio_proceedings = 0

		# ==========================================================================================================

		table_general = self.build_table_2019_general(journals, proceedings, a1_a4, a1, a2, a3, a4, 
			b1_b4, b1, b2, b3, b4, others, Irestrito, Igeral, Irestrito_journals, Igeral_journals, 
			Irestrito_proceedings, Igeral_proceedings, SE_journals, SE_proceedings, SE_a1_a4, SE_a1, 
			SE_a2, SE_a3, SE_a4, SE_b1_b4, SE_b1, SE_b2, SE_b3, SE_b4, SE_others, percentages_SE, 
			percentages, Irestrito_medio, Igeral_medio, Irestrito_medio_journals, Igeral_medio_journals, 
			Irestrito_medio_proceedings, Igeral_medio_proceedings)

		table_journals = self.build_table_2019_separated(a1_a4_journals, a1_journals, a2_journals, a3_journals, a4_journals, 
			b1_b4_journals, b1_journals, b2_journals, b3_journals, b4_journals, others_journals, Irestrito_journals, 
			Igeral_journals, SE_a1_a4_journals, SE_a1_journals, SE_a2_journals, SE_a3_journals, SE_a4_journals, 
			SE_b1_b4_journals, SE_b1_journals, SE_b2_journals, SE_b3_journals, SE_b4_journals, SE_others_journals, 
			percentages_SE_journals, percentages_journals, Irestrito_medio_journals, Igeral_medio_journals)

		table_proceedings = self.build_table_2019_separated(a1_a4_proceedings, a1_proceedings, a2_proceedings, a3_proceedings, a4_proceedings, 
			b1_b4_proceedings, b1_proceedings, b2_proceedings, b3_proceedings, b4_proceedings, others_proceedings, Irestrito_proceedings, 
			Igeral_proceedings, SE_a1_a4_proceedings, SE_a1_proceedings, SE_a2_proceedings, SE_a3_proceedings, SE_a4_proceedings, 
			SE_b1_b4_proceedings, SE_b1_proceedings, SE_b2_proceedings, SE_b3_proceedings, SE_b4_proceedings, SE_others_proceedings, 
			percentages_SE_proceedings, percentages_proceedings, Irestrito_medio_proceedings, Igeral_medio_proceedings)
		
		if self.general == True:
			Irestrito_3x1_proceedings, Igeral_3x1_proceedings, Irestrito_3x1_total, Igeral_3x1_total = self.apply_3x1_2019(a1_journals, a2_journals, a3_journals, a4_journals, 
				b1_journals, b2_journals, b3_journals, b4_journals, a1_proceedings, a2_proceedings, a3_proceedings, a4_proceedings,
				b1_proceedings, b2_proceedings, b3_proceedings, b4_proceedings)
			self.get_irestritos(Irestrito, Irestrito_journals, Irestrito_proceedings, Irestrito_3x1_proceedings, Irestrito_3x1_total)
			self.get_igerais(Igeral, Igeral_journals, Igeral_proceedings, Igeral_3x1_proceedings, Igeral_3x1_total)

		return (pd.DataFrame(table_general), pd.DataFrame(table_journals), pd.DataFrame(table_proceedings))


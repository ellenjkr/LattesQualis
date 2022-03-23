from _Classes.Data import Data
from _Classes.Excel import ExcelFile
from _Funções_e_Valores.values import FILES_DIRECTORY, FILE, HAS_EVENTS

import pandas as pd


def read_files():
	# Read files - People
	try:
		professors = pd.read_csv(f"{FILES_DIRECTORY}/Professores.csv", sep=";", encoding='utf-8')
	except:
		professors = pd.read_csv(f"{FILES_DIRECTORY}/Professores.csv", sep=";", encoding='iso-8859-1')
	try:
		egress = pd.read_csv(f"{FILES_DIRECTORY}/Egressos.CSV", sep=";", encoding='iso-8859-1')
	except:
		egress = pd.read_csv(f"{FILES_DIRECTORY}/Egressos.CSV", sep=";", encoding='utf-8')

	if FILE == "UNIVALI 2013-2016":
		try:
			students = pd.read_csv(f"{FILES_DIRECTORY}/Egressos.CSV", sep=";", encoding='iso-8859-1')
		except:
			students = pd.read_csv(f"{FILES_DIRECTORY}/Egressos.CSV", sep=";", encoding='utf-8')
	else:
		try:
			students = pd.read_csv(f"{FILES_DIRECTORY}/Alunos.CSV", sep=";", encoding='iso-8859-1')
		except:
			students = pd.read_csv(f"{FILES_DIRECTORY}/Alunos.CSV", sep=";", encoding='utf-8')
	

	# Read files - Qualis
	try:
		qualis_cc2016_file = pd.read_csv(f"{FILES_DIRECTORY}/Qualis/QualisCC_2013_2016.csv", sep=";", encoding='iso-8859-1')
	except:
		qualis_cc2016_file = pd.read_csv(f"{FILES_DIRECTORY}/Qualis/QualisCC_2013_2016.csv", sep=";", encoding='utf-8')
	try:
		qualis_xx2020_file = pd.read_csv(f"{FILES_DIRECTORY}/Qualis/QualisXX_2020.csv", sep=";", encoding='iso-8859-1')
	except:
		qualis_xx2020_file = pd.read_csv(f"{FILES_DIRECTORY}/Qualis/QualisXX_2020.csv", sep=";", encoding='utf-8')
	

	if HAS_EVENTS == True:
		try:
			qualis_cc2016_eventos = pd.read_csv(f"{FILES_DIRECTORY}/Qualis/QualisCC_eventos_2016.csv", sep=";", encoding='iso-8859-1')
		except:
			qualis_cc2016_eventos = pd.read_csv(f"{FILES_DIRECTORY}/Qualis/QualisCC_eventos_2016.csv", sep=";", encoding='utf-8')
		try:
			qualis_xx2020_eventos = pd.read_csv(f"{FILES_DIRECTORY}/Qualis/QualisXX_eventos_2020.csv", sep=";", encoding='iso-8859-1')
		except:
			qualis_xx2020_eventos = pd.read_csv(f"{FILES_DIRECTORY}/QualisXX_eventos_2020.csv", sep=";", encoding='utf-8')
	else:
		qualis_cc2016_eventos = None 
		qualis_xx2020_eventos = None

	return (professors, egress, students, qualis_cc2016_file, qualis_xx2020_file, qualis_cc2016_eventos, qualis_xx2020_eventos)


if __name__ == '__main__':
	# pd.options.mode.chained_assignment = 'raise'

	professors, egress, students, qualis_2016, qualis_2020, qualis_2016_events, qualis_2020_events = read_files()

	data = Data(professors, egress, students, qualis_2016, qualis_2020, qualis_2016_events, qualis_2020_events)
	data.treat_data()
	data.get_authors_reports()
	data.treat_names()
	data.get_art_prof()
	data.update_authors_dict()
	data.get_artppg()
	data.get_indicators()

	data.journals_upperstrata_2019, data.journals_upperstrata_SE_2019 = data.analyze_journal_classifications("2019")
	data.journals_upperstrata_2016, data.journals_upperstrata_SE_2016 = data.analyze_journal_classifications("CC 2016")

	data.analyze_journals()

	data.journal_metrics_2019 = data.analyze_journal_metrics("2019")
	data.journal_metrics_2016 = data.analyze_journal_metrics("CC 2016")

	data.analyze_proceedings()

	data.proceedings_metrics_2019 = data.analyze_proceedings_metrics("2019")
	data.proceedings_metrics_2016 = data.analyze_proceedings_metrics("CC 2016")

	data.get_scopus_citations()

	excel = ExcelFile(data)
	excel.save_file()

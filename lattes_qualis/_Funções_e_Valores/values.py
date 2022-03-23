# Choose the file

# FILE = "BRUNO ARAUJO CC"
# FILE = "BRUNO ARAUJO FARMACIA"
FILE = "ANDRE 2022"
# FILE = "UNIVALI 2017-2020"
# FILE = "UNIVALI 2020"
# FILE = "UNIVALI 2013-2016"
# FILE = "UFSC 2017-2020"
# FILE = "TURISMO E HOTELARIA 2017-2020"
# FILE = "ODONTO 2017-2020"
# FILE = "EGRESSOS 2017-2020"

#-------------------------------------
# Choose if scopus data should be retrieved

REQUEST_SCOPUS_DATA = False
# REQUEST_SCOPUS_DATA = True

# =========================================================

if FILE == "BRUNO ARAUJO CC":
	EGRESS = False # If the entry data are egress
	FILES_DIRECTORY = "Arquivos BRUNO ARAUJO CC"
	ND = 12.1 
	quadrennium = ["17", "18", "19", "20", "21"] 
	FULL_PERIOD_AUTHORS = True # True if we assume the authors are active for the whole period
	HAS_EVENTS = True
	EXCEL_FILE_NAME = "coleta_bruno_araujo_CC.xlsx" 

	# GRAPH:
	Y_LIMITS = {"Irestrito": 30, "Igeral": 30, "Periódicos": 30, "Periódicos com alunos/egressos": 30, "Anais": 30, "Anais com alunos/egressos": 30, 
				"A1-A4": 30, "A1-A4 com alunos/egressos": 30, "A1-B1": 30, "A1-B1 com alunos/egressos": 30,
				"B1-B4": 30, "B1-B4 com alunos/egressos": 30, "B2-B5": 30, "B2-B5 com alunos/egressos": 30,
				 "Periódicos A1-A4": 30, "Periódicos A1-A4 com alunos/egressos": 30, "Periódicos A1-B1": 30, "Periódicos A1-B1 com alunos/egressos": 30}
	Y_LIMITS_PROCEEDINGS = 30 
	Y_LIMITS_JOURNALS = 30 

elif FILE == "BRUNO ARAUJO FARMACIA":
	EGRESS = False # If the entry data are egress
	FILES_DIRECTORY = "Arquivos BRUNO ARAUJO FARMACIA"
	ND = 12.1 
	quadrennium = ["17", "18", "19", "20", "21"] 
	FULL_PERIOD_AUTHORS = True # True if we assume the authors are active for the whole period
	HAS_EVENTS = False
	EXCEL_FILE_NAME = "coleta_bruno_araujo_farmacia.xlsx" 

	# GRAPH:
	Y_LIMITS = {"Irestrito": 30, "Igeral": 30, "Periódicos": 30, "Periódicos com alunos/egressos": 30, "Anais": 30, "Anais com alunos/egressos": 30, 
				"A1-A4": 30, "A1-A4 com alunos/egressos": 30, "A1-B1": 30, "A1-B1 com alunos/egressos": 30,
				"B1-B4": 30, "B1-B4 com alunos/egressos": 30, "B2-B5": 30, "B2-B5 com alunos/egressos": 30,
				 "Periódicos A1-A4": 30, "Periódicos A1-A4 com alunos/egressos": 30, "Periódicos A1-B1": 30, "Periódicos A1-B1 com alunos/egressos": 30}
	Y_LIMITS_PROCEEDINGS = 30 
	Y_LIMITS_JOURNALS = 30 

elif FILE == "ANDRE 2022":
	EGRESS = False # If the entry data are egress
	FILES_DIRECTORY = "Arquivos ANDRE 2022"
	ND = 12.1 
	quadrennium = ["18", "19", "20", "21"] 
	FULL_PERIOD_AUTHORS = True # True if we assume the authors are active for the whole period
	HAS_EVENTS = True
	EXCEL_FILE_NAME = "coleta_univali_2018_2021.xlsx" 

	# GRAPH:
	Y_LIMITS = {"Irestrito": 30, "Igeral": 30, "Periódicos": 30, "Periódicos com alunos/egressos": 30, "Anais": 30, "Anais com alunos/egressos": 30, 
				"A1-A4": 30, "A1-A4 com alunos/egressos": 30, "A1-B1": 30, "A1-B1 com alunos/egressos": 30,
				"B1-B4": 30, "B1-B4 com alunos/egressos": 30, "B2-B5": 30, "B2-B5 com alunos/egressos": 30,
				 "Periódicos A1-A4": 30, "Periódicos A1-A4 com alunos/egressos": 30, "Periódicos A1-B1": 30, "Periódicos A1-B1 com alunos/egressos": 30}
	Y_LIMITS_PROCEEDINGS = 30 
	Y_LIMITS_JOURNALS = 30 

elif FILE == "UNIVALI 2017-2020":
	EGRESS = False # If the entry data are egress
	FILES_DIRECTORY = "Arquivos UNIVALI 2017-2020"
	ND = 12.1 
	quadrennium = ["17", "18", "19", "20"] 
	FULL_PERIOD_AUTHORS = False # True if we assume the authors are active for the whole period
	HAS_EVENTS = True
	EXCEL_FILE_NAME = "coleta_univali_ppgc_2017_2020.xlsx" 

	# GRAPH:
	Y_LIMITS = {"Irestrito": 30, "Igeral": 30, "Periódicos": 30, "Periódicos com alunos/egressos": 30, "Anais": 30, "Anais com alunos/egressos": 30, 
				"A1-A4": 30, "A1-A4 com alunos/egressos": 30, "A1-B1": 30, "A1-B1 com alunos/egressos": 30,
				"B1-B4": 30, "B1-B4 com alunos/egressos": 30, "B2-B5": 30, "B2-B5 com alunos/egressos": 30,
				 "Periódicos A1-A4": 30, "Periódicos A1-A4 com alunos/egressos": 30, "Periódicos A1-B1": 30, "Periódicos A1-B1 com alunos/egressos": 30}
	Y_LIMITS_PROCEEDINGS = 30 
	Y_LIMITS_JOURNALS = 30 


elif FILE == "UNIVALI 2020":
	EGRESS = False
	FILES_DIRECTORY = "Arquivos UNIVALI 2020"
	ND = 12.1 
	quadrennium = ["20", "20", "20", "20"] 
	FULL_PERIOD_AUTHORS = False
	HAS_EVENTS = True
	EXCEL_FILE_NAME = "coleta_univali_ppgc_2020.xlsx" 

	# GRAPH:
	Y_LIMITS = {"Irestrito": 30, "Igeral": 30, "Periódicos": 30, "Periódicos com alunos/egressos": 30, "Anais": 30, "Anais com alunos/egressos": 30, 
				"A1-A4": 30, "A1-A4 com alunos/egressos": 30, "A1-B1": 30, "A1-B1 com alunos/egressos": 30,
				"B1-B4": 30, "B1-B4 com alunos/egressos": 30, "B2-B5": 30, "B2-B5 com alunos/egressos": 30,
				 "Periódicos A1-A4": 30, "Periódicos A1-A4 com alunos/egressos": 30, "Periódicos A1-B1": 30, "Periódicos A1-B1 com alunos/egressos": 30}
	Y_LIMITS_PROCEEDINGS = 30 
	Y_LIMITS_JOURNALS = 30 


elif FILE == "UNIVALI 2013-2016":
	EGRESS = False
	FILES_DIRECTORY = "Arquivos UNIVALI 2013-2016"
	ND = 9.8 
	quadrennium = ["13", "14", "15", "16"]
	FULL_PERIOD_AUTHORS = False
	HAS_EVENTS = True
	EXCEL_FILE_NAME = "coleta_univali_ppgc_2013_2016.xlsx"

	# GRAPH:
	Y_LIMITS = {"Irestrito": 30, "Igeral": 30, "Periódicos": 30, "Periódicos com alunos/egressos": 30, "Anais": 30, "Anais com alunos/egressos": 30, 
				"A1-A4": 30, "A1-A4 com alunos/egressos": 30, "A1-B1": 30, "A1-B1 com alunos/egressos": 30,
				"B1-B4": 30, "B1-B4 com alunos/egressos": 30, "B2-B5": 30, "B2-B5 com alunos/egressos": 30,
				 "Periódicos A1-A4": 30, "Periódicos A1-A4 com alunos/egressos": 30, "Periódicos A1-B1": 30, "Periódicos A1-B1 com alunos/egressos": 30}
	Y_LIMITS_PROCEEDINGS = 30 
	Y_LIMITS_JOURNALS = 30 

elif FILE == "UFSC 2017-2020":
	EGRESS = False
	FILES_DIRECTORY = "Arquivos UFSC 2017-2020"
	ND = 23.4
	quadrennium = ["17", "18", "19", "20"]
	FULL_PERIOD_AUTHORS = False
	HAS_EVENTS = True
	EXCEL_FILE_NAME = "coleta_ufsc_ppgcc_2017_2020.xlsx"

	# GRAPH:
	Y_LIMITS = {"Irestrito": 30, "Igeral": 30, "Periódicos": 30, "Periódicos com alunos/egressos": 30, "Anais": 40, "Anais com alunos/egressos": 40, 
				"A1-A4": 35, "A1-A4 com alunos/egressos": 35, "A1-B1": 35, "A1-B1 com alunos/egressos": 35,
				"B1-B4": 40, "B1-B4 com alunos/egressos": 40, "B2-B5": 40, "B2-B5 com alunos/egressos": 40,
				 "Periódicos A1-A4": 20, "Periódicos A1-A4 com alunos/egressos": 20, "Periódicos A1-B1": 20, "Periódicos A1-B1 com alunos/egressos": 20}
	Y_LIMITS_PROCEEDINGS = 15 
	Y_LIMITS_JOURNALS = 15 

elif FILE == "TURISMO E HOTELARIA 2017-2020":
	EGRESS = False
	FILES_DIRECTORY = "Arquivos TURISMO E HOTELARIA 2017-2020"
	ND = 12.1 
	quadrennium = ["17", "18", "19", "20"] 
	FULL_PERIOD_AUTHORS = True
	HAS_EVENTS = False
	EXCEL_FILE_NAME = "coleta_turismo_hotelaria_2017_2020.xlsx" 

	# GRAPH:
	Y_LIMITS = {"Irestrito": 30, "Igeral": 30, "Periódicos": 30, "Periódicos com alunos/egressos": 30, "Anais": 0, "Anais com alunos/egressos": 0, 
				"A1-A4": 30, "A1-A4 com alunos/egressos": 30, "A1-B1": 30, "A1-B1 com alunos/egressos": 30,
				"B1-B4": 30, "B1-B4 com alunos/egressos": 30, "B2-B5": 30, "B2-B5 com alunos/egressos": 30,
				 "Periódicos A1-A4": 30, "Periódicos A1-A4 com alunos/egressos": 30, "Periódicos A1-B1": 30, "Periódicos A1-B1 com alunos/egressos": 30}
	Y_LIMITS_PROCEEDINGS = 30 
	Y_LIMITS_JOURNALS = 30 

elif FILE == "ODONTO 2017-2020":
	EGRESS = False
	FILES_DIRECTORY = "Arquivos ODONTO 2017-2020"
	ND = 11
	quadrennium = ["17", "18", "19", "20"] 
	FULL_PERIOD_AUTHORS = True
	HAS_EVENTS = False
	EXCEL_FILE_NAME = "coleta_odonto_2017_2020.xlsx" 

	# GRAPH:
	Y_LIMITS = {"Irestrito": 35, "Igeral": 35, "Periódicos": 45, "Periódicos com alunos/egressos": 45, "Anais": 0, "Anais com alunos/egressos": 0, 
				"A1-A4": 40, "A1-A4 com alunos/egressos": 40, "A1-B1": 40, "A1-B1 com alunos/egressos": 40,
				"B1-B4": 15, "B1-B4 com alunos/egressos": 15, "B2-B5": 15, "B2-B5 com alunos/egressos": 15,
				 "Periódicos A1-A4": 45, "Periódicos A1-A4 com alunos/egressos": 45, "Periódicos A1-B1": 45, "Periódicos A1-B1 com alunos/egressos": 45}
	Y_LIMITS_PROCEEDINGS = 30 
	Y_LIMITS_JOURNALS = 30 

elif FILE == "EGRESSOS 2017-2020":
	EGRESS = True
	FILES_DIRECTORY = "Arquivos EGRESSOS 2017-2020"
	ND = 120
	quadrennium = ["17", "18", "19", "20"] 
	FULL_PERIOD_AUTHORS = False # True if we assume the authors are active for the whole period
	HAS_EVENTS = True
	EXCEL_FILE_NAME = "coleta_egressos_ppgc_2017_2020.xlsx" 

	# GRAPH:
	Y_LIMITS = {"Irestrito": 35, "Igeral": 35, "Periódicos": 45, "Periódicos com alunos/egressos": 45, "Anais": 0, "Anais com alunos/egressos": 0, 
				"A1-A4": 40, "A1-A4 com alunos/egressos": 40, "A1-B1": 40, "A1-B1 com alunos/egressos": 40,
				"B1-B4": 15, "B1-B4 com alunos/egressos": 15, "B2-B5": 15, "B2-B5 com alunos/egressos": 15,
				 "Periódicos A1-A4": 45, "Periódicos A1-A4 com alunos/egressos": 45, "Periódicos A1-B1": 45, "Periódicos A1-B1 com alunos/egressos": 45}
	Y_LIMITS_PROCEEDINGS = 30 
	Y_LIMITS_JOURNALS = 30 
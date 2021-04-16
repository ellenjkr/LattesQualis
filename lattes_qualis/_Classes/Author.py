import xml.etree.ElementTree as ET
import pandas as pd
import os
import requests
from requests.exceptions import HTTPError
import json

from _Funções_e_Valores.verify_authors import treat_commas, search_professors_list, search_authors_list, treat_exceptions
from _Funções_e_Valores._exceptions import event_exceptions, initials_exceptions, issn_exceptions, article_exceptions, presentation_exceptions
from _Funções_e_Valores.values import quadrennium, FILES_DIRECTORY, HAS_EVENTS, REQUEST_SCOPUS_DATA


class Quartis(): # Get journal quartile
	def __init__(self, issn, api_key): # Enter with the scopus api and the issn value
		super(Quartis, self).__init__()
		self.issn = issn
		self.api_key = api_key

	def search_percentil(self):
		if self.issn != None:
			self.issn = self.issn.replace("-", "")
			self.issn = self.issn.replace(".0", "")
		percentil = None
		log = ''
		link_scopus = ''
		insttoken = os.environ.get('INSTTOKEN')
		headers = {'X-ELS-Insttoken': insttoken, 'X-ELS-APIKey': self.api_key}
		uri = "https://api.elsevier.com/content/serial/title?issn=" + self.issn + "&view=citescore"
		response = requests.get(uri, headers=headers)
		try:
			json_data = json.loads(response.text)

			link_scopus = json_data['serial-metadata-response']['entry'][0]['link'][0]['@href']
			try:
				percentil = json_data['serial-metadata-response']['entry'][0]['citeScoreYearInfoList']['citeScoreYearInfo'][1]['citeScoreInformationList'][0]['citeScoreInfo'][0]['citeScoreSubjectRank'][0]['percentile']
			except:
				log = 'sem valor de percentil'

		except HTTPError as http_err:
			log += 'HTTP error occurred: ' + str(http_err) + ' - Status_code: ' + str(response.status_code)
		except Exception as err:
			log += 'Other error occurred: ' + str(err) + ' - Status_code: ' + str(response.status_code)

		if percentil == '':
			percentil = None

		return percentil, link_scopus, str(log)

	def get_quartis(self):
		per, link, log = self.search_percentil()
		
		if per == None:
			return "-"
		else:
			if int(per) >= 75:
				quarti = "Q1"
			elif int(per) >= 50:
				quarti = "Q2"
			elif int(per) >= 25:
				quarti = "Q3"
			else:
				quarti = "Q4"

			return quarti


class Author():
	def __init__(self, name, period, qualis_cc2016_file, qualis_xx2020_file, qualis_cc2016_eventos, qualis_xx2020_eventos, professors, authors_list):
		super(Author, self).__init__()
		self.name = name
		self.period = period

		self.qualis_cc2016_file = qualis_cc2016_file
		self.qualis_xx2020_file = qualis_xx2020_file
		self.qualis_cc2016_eventos = qualis_cc2016_eventos
		self.qualis_xx2020_eventos = qualis_xx2020_eventos

		self.professors = professors
		self.authors_list = authors_list
			

		self.exceptions = {'Nome Trabalho':[], 'Nome Evento Cadastrado':[], 'Nome Evento Canônico':[]} # Events exceptions
		self.type_dict = {"ARTIGO-PUBLICADO": "Periódico", "TRABALHO-EM-EVENTOS": "Anais", 'LIVRO-PUBLICADO-OU-ORGANIZADO': 'Livros', 'CAPITULO-DE-LIVRO-PUBLICADO': 'Capítulos'}
		self.info = {"Ano":[], "Tipo":[], "Título":[], "Nome de Publicação":[], "ISSN/SIGLA":[], "Qualis CC 2016":[], "Qualis 2019":[], "Scopus 2019":[], "A/E":[]}
		self.suffixes  = ['Jr.', 'Jr', 'Filho', 'Neto']

		self.authors_amount = 0
		
		self.myroot = self.get_XML_file()
		self.fill_info()

	def get_XML_file(self):
		mytree = ET.parse(f"{FILES_DIRECTORY}/Curriculos/{self.name}.xml") # Open author's resume
		return mytree.getroot()

	def add_authors(self, pub): # Get all the authors of a publication
		authors = []
		for i in pub:
			if 'NOME-COMPLETO-DO-AUTOR' in i.attrib.keys(): # Search for authors
				self.authors_amount += 1 # Increases the total number of authors
				author = i.attrib['NOME-COMPLETO-DO-AUTOR'] 
				author = author.title()
				
				author = treat_commas(author)
				author = search_professors_list(self.professors, author)

				# Finds out if the author is already on the authors list (searches for similarities)
				# If it's not on it, it's added to the list
				self.authors_list, author = search_authors_list(self.authors_list, author)


				authors.append(author)
	

		# Define columns names
		for pos2, author in enumerate(authors):
			if f"{pos2+1}º Autor" not in self.info:
				self.info[f"{pos2+1}º Autor"] = []
				for i in range(len(self.info["Título"])-1):
					self.info[f"{pos2+1}º Autor"].append(" ")

		author_keys = []
		for key in self.info.keys():
			if "º Autor" in key:
				author_keys.append(key)
		for pos3, key in enumerate(author_keys):
			if pos3 <= (len(authors)-1):
				self.info[key].append(authors[pos3])
			else:
				self.info[key].append(" ")


	def add_article_data(self, pub, year):
		self.info["Ano"].append(year)
		
		title = pub[0].attrib['TITULO-DO-ARTIGO']
		title = article_exceptions(title)
		self.info["Título"].append(title)

		journal= pub[1].attrib['TITULO-DO-PERIODICO-OU-REVISTA'].upper()
		issn = pub[1].attrib['ISSN']


		if REQUEST_SCOPUS_DATA == True:
			quartis = Quartis(issn, '2f8a856ea2c32c265b4c5a9895e6900d')
			self.info["Scopus 2019"].append(quartis.get_quartis())
		else:
			self.info["Scopus 2019"].append("-")

		qualis_cc2016 = self.qualis_cc2016_file.loc[self.qualis_cc2016_file['ISSN'] == issn]
		try:
			qualis_cc2016 = qualis_cc2016.reset_index()
			qualis_cc2016 = qualis_cc2016["Estrato"][0]
		except:
			issn = issn_exceptions(journal, issn)
			qualis_cc2016 = self.qualis_cc2016_file.loc[self.qualis_cc2016_file['ISSN'] == issn]
			try:
				qualis_cc2016 = qualis_cc2016.reset_index()
				qualis_cc2016 = qualis_cc2016['Estrato'][0]
			except:
				qualis_cc2016 = "-"

		self.info["Qualis CC 2016"].append(qualis_cc2016)

		qualis_cc2020 = self.qualis_xx2020_file.loc[self.qualis_xx2020_file['ISSN'] == issn]
		try:
			qualis_cc2020 = qualis_cc2020.reset_index()
			qualis_cc2020 = qualis_cc2020["Estrato"][0]
		except:
			issn = issn_exceptions(journal, issn)
			qualis_cc2020 = self.qualis_xx2020_file.loc[self.qualis_xx2020_file['ISSN'] == issn]
			try:
				qualis_cc2020 = qualis_cc2020.reset_index()
				qualis_cc2020 = qualis_cc2020['Estrato'][0]
			except:
				qualis_cc2020 = "-"

		self.info["Qualis 2019"].append(qualis_cc2020)

		if qualis_cc2020 == "-" and qualis_cc2016 =="-":
			self.info["Nome de Publicação"].append("*" + journal)
		else:
			self.info["Nome de Publicação"].append(journal)
		
		self.info["ISSN/SIGLA"].append(issn[:4] + "-" +issn[4:])

	def add_event_data(self, pub, year):
		self.info["Scopus 2019"].append("-")
		self.info["Ano"].append(year)

		title = pub[0].attrib['TITULO-DO-TRABALHO']
		title = presentation_exceptions(title)
		self.info["Título"].append(title)
		
		event_name = pub[1].attrib['NOME-DO-EVENTO']
		proceedings_title = pub[1].attrib['TITULO-DOS-ANAIS-OU-PROCEEDINGS']

		
		if len(event_name) > int(len(proceedings_title)/3):
			name = event_name
		else:
			name = proceedings_title

		name, event_name, self.exceptions = event_exceptions(name, event_name, pub[0].attrib['TITULO-DO-TRABALHO'], self.exceptions)
		name = "*" + name
		event_name = "*" + event_name
		
		initials = initials_exceptions(name)

		qualis_cc2016 = "-"
		qualis_2020 = "-"

		for pos, default_name in enumerate(self.qualis_cc2016_eventos['Nome Padrão']):
			if default_name != "nan":
				if default_name.lower() in name.lower():
					initials = self.qualis_cc2016_eventos['SIGLA'][pos]
					name = default_name
					qualis_cc2016 = self.qualis_cc2016_eventos['Qualis 2016'][pos]
					break
				# elif default_name.lower() in proceedings_title.lower():
				# 	initials = self.qualis_cc2016_eventos['SIGLA'][pos]
				# 	name = default_name
				# 	qualis_cc2016 = self.qualis_cc2016_eventos['Qualis 2016'][pos]
				# 	break
		self.info["Qualis CC 2016"].append(qualis_cc2016)


		for pos, default_name in enumerate(self.qualis_xx2020_eventos['Nome Padrão']):
			if default_name != "nan":
				if default_name.lower() in name.lower():
					initials = self.qualis_xx2020_eventos['SIGLA'][pos]
					name = default_name
					qualis_2020 = self.qualis_xx2020_eventos['Qualis 2020'][pos]
					break
				# elif default_name.lower() in proceedings_title.lower():
				# 	initials = self.qualis_xx2020_eventos['SIGLA'][pos]
				# 	name = default_name
				# 	qualis_2020 = self.qualis_xx2020_eventos['Qualis 2020'][pos]
				# 	break

		self.info["Qualis 2019"].append(qualis_2020)

		# self.info["Qualis Eng. IV 2016"].append("-")

		name = name.title()
		self.info["Nome de Publicação"].append(name.upper())
		self.info["ISSN/SIGLA"].append(initials)


	def add_book_data(self, pub, year):
		self.info["Ano"].append(year)
		
		title = pub[0].attrib['TITULO-DO-LIVRO']
		self.info["Título"].append(title)
		self.info["Nome de Publicação"].append(title)

		self.info["Scopus 2019"].append("-")
		self.info["Qualis CC 2016"].append("-")
		self.info["Qualis 2019"].append("-")
		
		isbn = pub[1].attrib['ISBN']
		self.info["ISSN/SIGLA"].append(isbn)


	def add_chapter_data(self, pub, year):
		self.info["Ano"].append(year)
		
		title = pub[0].attrib['TITULO-DO-CAPITULO-DO-LIVRO']
		self.info["Título"].append(title)

		publication_name = pub[1].attrib['TITULO-DO-LIVRO']
		self.info["Nome de Publicação"].append(publication_name)

		self.info["Scopus 2019"].append("-")
		self.info["Qualis CC 2016"].append("-")
		self.info["Qualis 2019"].append("-")
		
		isbn = pub[1].attrib['ISBN']
		self.info["ISSN/SIGLA"].append(isbn)


	def fill_info(self):
		publications_list = []
		for i in self.myroot[1]:
			if i.tag == 'LIVROS-E-CAPITULOS': # If it's a chapter or a book
				for j in i:
					publications_list.append(j) # Add chapters and books to the list
			elif i.tag == "ARTIGOS-PUBLICADOS": # If it's an article 
				publications_list.append(i) # Add the publications to the list
			elif i.tag == "TRABALHOS-EM-EVENTOS" and HAS_EVENTS == True: # If it's an event
				publications_list.append(i) # Add the publications to the list

		for publications in publications_list: 
			for pub in publications: # For each publication
				if pub.tag == "TRABALHO-EM-EVENTOS": # Events
					year = int(pub[0].attrib['ANO-DO-TRABALHO']) # Get year
				elif pub.tag == "ARTIGO-PUBLICADO": # Articles 
					try:
						year = int(pub[0].attrib['ANO-DO-ARTIGO']) # Get year
					except:
						print(pub[0].attrib['ANO-DO-ARTIGO'])
				elif pub.tag == 'LIVRO-PUBLICADO-OU-ORGANIZADO':# Book
					year = int(pub[0].attrib['ANO']) # Get year
				else: # Chapter
					year = int(pub[0].attrib['ANO']) # Get year

				first_year = int(quadrennium[0]) + 2000 # First year of the quadrennium
				last_year = int(quadrennium[3]) + 2000 # Last year of the quadrennium

				if year >= first_year and year <= last_year: # If the year is in the quadrennium
					if self.period[str(year)[2:]] == True: # If the publication year is valid for that author
						if pub.tag == "TRABALHO-EM-EVENTOS": # Event
							if pub[0].attrib['NATUREZA'] == 'COMPLETO': # Complete works only
								self.info["Tipo"].append(self.type_dict[pub.tag]) # Get type
								self.info["A/E"].append("") # "Contém Alunos/Egressos" Default = empty
								self.add_event_data(pub, year) # Add all the presentation info
								self.add_authors(pub) # Add all the authors
						elif pub.tag == "ARTIGO-PUBLICADO": # Article
							self.info["Tipo"].append(self.type_dict[pub.tag])
							self.info["A/E"].append("")
							self.add_article_data(pub, year)
							self.add_authors(pub)

						elif pub.tag == 'LIVRO-PUBLICADO-OU-ORGANIZADO': # Book
							self.info["Tipo"].append(self.type_dict[pub.tag])
							self.info["A/E"].append("")
							self.add_book_data(pub, year)
							self.add_authors(pub)
						else: # Chapter
							self.info["Tipo"].append(self.type_dict[pub.tag])
							self.info["A/E"].append("")
							self.add_chapter_data(pub, year)
							self.add_authors(pub)

	def get_authors_average(self): # Average number of authors per article 
		try:
			average = f"Média de autores/artigo = {self.authors_amount/len(pd.DataFrame(self.info)):.2f}"
		except ZeroDivisionError:
			average = ""
		return average

	def get_indicators(self):
		data_frame = pd.DataFrame(self.info) # Convert data into a dataframe
		total_articles = len(data_frame["Tipo"]) # Get the total number of articles
		
		# ==========================================================

		# Count amount of each type
		journals = 0 
		proceedings = 0
		types = data_frame["Tipo"].value_counts()
		for i in types.index:
			if i == "Periódico":
				journals = types[i]
			elif i == "Anais":
				proceedings = types[i]

		# ==========================================================

		# Count amount of each qualis
		grouping  = data_frame["Qualis 2019"].value_counts().sort_index()

		others = 0
		a1_a4 = 0
		b1_b4 = 0
		qualis = {}
		for i in grouping .index:
			if i in "A1A2A3A4": 
				a1_a4 += grouping [i]
			elif i in "B1B2B3B4":
				b1_b4 += grouping [i]
			if i not in "A1A2A3A4B1B2B3B4":
				others += grouping [i]
			else:
				qualis[i]= grouping [i]

		# ==========================================================

		# Calculate percentages
		percentages = []
		percentages.append((100/total_articles * journals).round(2))
		percentages.append((100/total_articles * proceedings).round(2))
		percentages.append((100/total_articles * a1_a4).round(2))
		percentages.append((100/total_articles * b1_b4).round(2))
		for key in qualis.keys():
			percentages.append((100/total_articles * qualis[key]).round(2))
		percentages.append((100/total_arttotal_articlesigos * others).round(2))

		# ==========================================================

		# Build table
		type_qualis = ["Periódicos", "Anais", "A1-A4", "B1-B4", "A1", "A2", "A3", "A4", "B1", "B2", "B3", "B4", "Outros"]
		table = {"Tipo/Qualis": type_qualis, "Quantidade": [], "Porcentagem": []}
		table["Quantidade"].append(journals)
		table["Quantidade"].append(proceedings)
		table["Quantidade"].append(a1_a4)
		table["Quantidade"].append(b1_b4)
		for key in qualis.keys():
			table["Quantidade"].append(qualis[key])
		table["Quantidade"].append(others)

		for perc in percentages:
			table["Porcentagem"].append(f"{perc}%")

		# ==========================================================

		return pd.DataFrame(table)
import xml.etree.ElementTree as ET
import pandas as pd
from verifica_autores import trata_virgulas, em_lista_professores, em_lista_autores, trata_exceçoes
from excecoes import excecoes_evento, excecoes_sigla, excecoes_issn, excecoes_artigos, excecoes_apresentacoes
from requests.exceptions import HTTPError
import os
import requests
import json

class Quartis():
	def __init__(self, issn, api_key):
		super(Quartis, self).__init__()
		self.issn = issn
		self.api_key = api_key

	def buscaPercentil(self):
		if self.issn != None:
			self.issn = self.issn.replace("-", "")
			self.issn = self.issn.replace(".0", "")
		percentil = None
		log = ''
		link_scopus = ''
		try:
			insttoken = os.environ.get('INSTTOKEN')
			headers = {'X-ELS-Insttoken': insttoken, 'X-ELS-APIKey': self.api_key}
			uri = "https://api.elsevier.com/content/serial/title?issn=" + self.issn + "&view=citescore"
			response = requests.get(uri, headers=headers)
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
		per, link, log = self.buscaPercentil()
		
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
	def __init__(self, nome, periodo, qualis_cc2016_file, qualis_xx2020_file, qualis_cc2016_eventos, qualis_xx2020_eventos, professores, lista_autores):
		super(Author, self).__init__()
		self.nome = nome
		self.periodo = periodo
		self.qualis_cc2016_file = qualis_cc2016_file
		self.qualis_xx2020_file = qualis_xx2020_file

		self.qualis_cc2016_eventos = qualis_cc2016_eventos
		self.qualis_xx2020_eventos = qualis_xx2020_eventos

		self.professores = professores
		self.lista_autores = lista_autores
		
		self.dic_tipo = {"ARTIGO-PUBLICADO": "Periódico", "TRABALHO-EM-EVENTOS": "Anais"}
		self.info = {"Ano":[], "Tipo":[], "Título":[], "Nome de Publicação":[], "ISSN/SIGLA":[], "Qualis CC 2016":[], "Qualis 2019":[], "Scopus 2019":[], "A/E":[]}
		# self.info = {"Ano":[], "Tipo":[], "Título":[], "Nome de Publicação":[], "ISSN":[], "Qualis Eng. IV 2016":[], "Qualis CC 2016":[], "Qualis 2019":[]}
		self.sufixos = ['Jr.', 'Jr', 'Filho', 'Neto']
		# self.lista_autores = []
		self.qtd_autores = 0
		
		self.myroot = self.get_XML_file()
		self.fill_info()

	def get_XML_file(self):
		mytree = ET.parse(f"Curriculos/{self.nome}.xml")
		return mytree.getroot()

	def add_authors(self, pub):
		autores = []
		for i in pub:
			if 'NOME-COMPLETO-DO-AUTOR' in i.attrib.keys():
				self.qtd_autores += 1
				autor = i.attrib['NOME-COMPLETO-DO-AUTOR'] 
				autor = autor.title()
				
				autor = trata_virgulas(autor)
				autor = em_lista_professores(self.professores, autor)
				self.lista_autores, autor = em_lista_autores(self.lista_autores, autor)

				autores.append(autor)
		
		for pos2, autor in enumerate(autores):
			if f"{pos2+1}º Autor" not in self.info:
				self.info[f"{pos2+1}º Autor"] = []
				for i in range(len(self.info["Título"])-1):
					self.info[f"{pos2+1}º Autor"].append(" ")

		autor_keys = []
		for key in self.info.keys():
			if "º Autor" in key:
				autor_keys.append(key)
		for pos3, key in enumerate(autor_keys):
			if pos3 <= (len(autores)-1):
				self.info[key].append(autores[pos3])
			else:
				self.info[key].append(" ")


	def add_data_artigo(self, pub, ano):
		self.info["Ano"].append(ano)
		
		titulo = pub[0].attrib['TITULO-DO-ARTIGO']
		titulo = excecoes_artigos(titulo)
		self.info["Título"].append(titulo)
		periodico = pub[1].attrib['TITULO-DO-PERIODICO-OU-REVISTA'].upper()
		
		issn = pub[1].attrib['ISSN']

		quartis = Quartis(issn, '2f8a856ea2c32c265b4c5a9895e6900d')
		# self.info["Scopus 2019"].append(quartis.get_quartis())
		self.info["Scopus 2019"].append("-")

		qualis_cc2016 = self.qualis_cc2016_file.loc[self.qualis_cc2016_file['ISSN'] == issn]
		try:
			qualis_cc2016 = qualis_cc2016.reset_index()
			qualis_cc2016 = qualis_cc2016["Estrato"][0]
		except:
			issn = excecoes_issn(periodico, issn)
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
			issn = excecoes_issn(periodico, issn)
			qualis_cc2020 = self.qualis_xx2020_file.loc[self.qualis_xx2020_file['ISSN'] == issn]
			try:
				qualis_cc2020 = qualis_cc2020.reset_index()
				qualis_cc2020 = qualis_cc2020['Estrato'][0]
			except:
				qualis_cc2020 = "-"

		self.info["Qualis 2019"].append(qualis_cc2020)

		if qualis_cc2020 == "-" and qualis_cc2016 =="-":
			self.info["Nome de Publicação"].append("*"+periodico)
		else:
			self.info["Nome de Publicação"].append(periodico)
		
		self.info["ISSN/SIGLA"].append(issn[:4] + "-" +issn[4:])

	def add_data_evento(self, pub, ano):
		self.info["Scopus 2019"].append("-")
		self.info["Ano"].append(ano)

		titulo = pub[0].attrib['TITULO-DO-TRABALHO']
		titulo = excecoes_apresentacoes(titulo)
		self.info["Título"].append(titulo)
		
		nome_evento = pub[1].attrib['NOME-DO-EVENTO']
		titulo_anais = pub[1].attrib['TITULO-DOS-ANAIS-OU-PROCEEDINGS']

		if len(nome_evento) > len(titulo_anais):
			nome = nome_evento
		else:
			nome = titulo_anais

		nome, nome_evento = excecoes_evento(nome, nome_evento, pub[0].attrib['TITULO-DO-TRABALHO'])
		nome = "*" + nome
		nome_evento = "*" + nome_evento

		sigla = excecoes_sigla(nome)

		qualis_cc2016 = "-"
		qualis_2020 = "-"

		for pos, nome_padrao in enumerate(self.qualis_cc2016_eventos['Nome Padrão']):
			if nome_padrao != "nan":
				if nome_padrao.lower() in nome_evento.lower():
					sigla = self.qualis_cc2016_eventos['SIGLA'][pos]
					nome = nome_padrao
					qualis_cc2016 = self.qualis_cc2016_eventos['Qualis 2016'][pos]
					break
				elif nome_padrao.lower() in titulo_anais.lower():
					sigla = self.qualis_cc2016_eventos['SIGLA'][pos]
					nome = nome_padrao
					qualis_cc2016 = self.qualis_cc2016_eventos['Qualis 2016'][pos]
					break
		self.info["Qualis CC 2016"].append(qualis_cc2016)


		for pos, nome_padrao in enumerate(self.qualis_xx2020_eventos['Nome Padrão']):
			if nome_padrao != "nan":
				if nome_padrao.lower() in nome_evento.lower():
					sigla = self.qualis_xx2020_eventos['SIGLA'][pos]
					nome = nome_padrao
					qualis_2020 = self.qualis_xx2020_eventos['Qualis 2020'][pos]
					break
				elif nome_padrao.lower() in titulo_anais.lower():
					sigla = self.qualis_xx2020_eventos['SIGLA'][pos]
					nome = nome_padrao
					qualis_2020 = self.qualis_xx2020_eventos['Qualis 2020'][pos]
					break

		self.info["Qualis 2019"].append(qualis_2020)

		# self.info["Qualis Eng. IV 2016"].append("-")

		nome = nome.title()
		self.info["Nome de Publicação"].append(nome.upper())
		self.info["ISSN/SIGLA"].append(sigla)


	def fill_info(self):
		publications_list = []
		for i in self.myroot[1]:
			if i.tag == "ARTIGOS-PUBLICADOS" or i.tag == "TRABALHOS-EM-EVENTOS":
				publications_list.append(i)
		print(self.nome, len(publications_list[0]))
		for publications in publications_list:
			if "aluizio" in self.nome.lower():
				print(len(publications))
			for pub in publications:
				if pub.tag == "TRABALHO-EM-EVENTOS":
					ano = int(pub[0].attrib['ANO-DO-TRABALHO'])
				else:
					ano = int(pub[0].attrib['ANO-DO-ARTIGO'])
				if ano >= 2017 and ano <= 2020:
					# print(self.nome, periodo)
					if self.periodo[str(ano)[2:]] == True:
						if pub.tag == "TRABALHO-EM-EVENTOS":
							if pub[0].attrib['NATUREZA'] == 'COMPLETO':
								self.info["Tipo"].append(self.dic_tipo[pub.tag])
								self.info["A/E"].append("")
								self.add_data_evento(pub, ano)
								self.add_authors(pub)
						else:
							self.info["Tipo"].append(self.dic_tipo[pub.tag])
							self.info["A/E"].append("")
							self.add_data_artigo(pub, ano)
							self.add_authors(pub)

	def get_media_autores(self):
		try:
			media = f"Média de autores/artigo = {self.qtd_autores/len(pd.DataFrame(self.info)):.2f}"
		except ZeroDivisionError:
			media = ""
		return media

	def get_indicadores(self):
		data_frame = pd.DataFrame(self.info)
		total_artigos = len(data_frame["Tipo"])
		

		periodicos = 0
		anais = 0
		tipos = data_frame["Tipo"].value_counts()
		for i in tipos.index:
			if i == "Periódico":
				periodicos = tipos[i]
			elif i == "Anais":
				anais = tipos[i]

		agrupamento = data_frame["Qualis 2019"].value_counts().sort_index()

		outros = 0
		a1_a4 = 0
		b1_b4 = 0
		qualis = {}
		for i in agrupamento.index:
			if i in "A1A2A3A4":
				a1_a4 += agrupamento[i]
			elif i in "B1B2B3B4":
				b1_b4 += agrupamento[i]
			if i not in "A1A2A3A4B1B2B3B4":
				outros += agrupamento[i]
			else:
				qualis[i]= agrupamento[i]

		porcentagens = []
		porcentagens.append((100/total_artigos * periodicos).round(2))
		porcentagens.append((100/total_artigos * anais).round(2))
		porcentagens.append((100/total_artigos * a1_a4).round(2))
		porcentagens.append((100/total_artigos * b1_b4).round(2))
		for key in qualis.keys():
			porcentagens.append((100/total_artigos * qualis[key]).round(2))
		porcentagens.append((100/total_artigos * outros).round(2))

		tipo_qualis = ["Periódicos", "Anais", "A1-A4", "B1-B4", "A1", "A2", "A3", "A4", "B1", "B2", "B3", "B4", "Outros"]
		tabela = {"Tipo/Qualis": tipo_qualis, "Quantidade": [], "Porcentagem": []}
		tabela["Quantidade"].append(periodicos)
		tabela["Quantidade"].append(anais)
		tabela["Quantidade"].append(a1_a4)
		tabela["Quantidade"].append(b1_b4)
		for key in qualis.keys():
			tabela["Quantidade"].append(qualis[key])
		tabela["Quantidade"].append(outros)

		for perc in porcentagens:
			tabela["Porcentagem"].append(f"{perc}%")

		return pd.DataFrame(tabela)
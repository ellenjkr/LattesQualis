import pandas as pd

def excecoes_artigos_scopus(titulo):
	excecoes = pd.read_csv('Exceções/excecoes_artigos_scopus.CSV', sep=';', encoding='utf-8')
	for pos, artigo in enumerate(excecoes['Título no Scopus']):
		titulo = titulo.replace(";", ",")
		if artigo.upper() in titulo.upper():
			titulo = str(excecoes['Título no Lattes'][pos])
			break
	
	return titulo.lower()


def excecoes_artigos(titulo):
	excecoes = pd.read_csv('Exceções/excecoes_artigos.CSV', sep=';', encoding='utf-8')
	for pos, artigo in enumerate(excecoes['Título Cadastrado']):
		titulo = titulo.replace(";", ",")
		if titulo.upper() == artigo.upper():
			titulo = str(excecoes['Título Canônico'][pos])
			break

	return titulo


def excecoes_apresentacoes(titulo):
	excecoes = pd.read_csv('Exceções/excecoes_apresentacoes.CSV', sep=';', encoding='utf-8')
	for pos, apresentacao in enumerate(excecoes['Título Cadastrado']):
		titulo = titulo.replace(";", ",")
		if titulo.upper() == apresentacao.upper():
			titulo = str(excecoes['Título Canônico'][pos])
			break

	return titulo


def excecoes_issn(nome, issn):
	excecoes = pd.read_csv('Exceções/excecoes_issn.CSV', sep=';', encoding='utf-8')
	for pos, evento in enumerate(excecoes['Nome Evento']):
		nome = nome.replace(";", ",")
		if nome.upper() == evento.upper():
			issn = str(excecoes['ISSN'][pos])
			break
	return issn


def excecoes_evento(nome, nome_evento, titulo_trabalho):
	excecoes = pd.read_csv('Exceções/excecoes_eventos.CSV', sep=';', encoding='utf-8')
	for pos, evento_cadastrado in enumerate(excecoes['Nome Evento Cadastrado']):
		nome = nome.replace(";", ",")
		if nome.upper() == evento_cadastrado.upper():
			nome = excecoes['Nome Evento Canônico'][pos]
			nome_evento = nome
			break
	
	return (nome, nome_evento)


def excecoes_sigla(nome):
	sigla = " "
	nome = nome.replace("*", "")
	excecoes = pd.read_csv('Exceções/excecoes_siglas.CSV', sep=';', encoding='utf-8')
	for pos, evento in enumerate(excecoes['Nome Evento']):
		nome = nome.replace(";", ",")
		if nome.upper() == evento.upper():
			sigla = excecoes['Sigla'][pos]
			break

	return sigla
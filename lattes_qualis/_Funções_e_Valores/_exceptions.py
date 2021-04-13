import pandas as pd

# Search for a match and replace the word with it's right name

def scopus_articles_exceptions(title):
	exceptions = pd.read_csv('Exceções/excecoes_artigos_scopus.CSV', sep=';', encoding='utf-8')
	for pos, article in enumerate(exceptions['Título no Scopus']):
		title = title.replace(";", ",")
		if article.upper() in title.upper():
			title = str(exceptions['Título no Lattes'][pos])
			break
	
	return title.lower()


def article_exceptions(title):
	exceptions = pd.read_csv('Exceções/excecoes_artigos.CSV', sep=';', encoding='utf-8')
	for pos, article in enumerate(exceptions['Título Cadastrado']):
		title = title.replace(";", ",")
		if title.upper() == article.upper():
			title = str(exceptions['Título Canônico'][pos])
			break

	return title


def presentation_exceptions(title):
	exceptions = pd.read_csv('Exceções/excecoes_apresentacoes.CSV', sep=';', encoding='utf-8')
	for pos, presentation in enumerate(exceptions['Título Cadastrado']):
		title = title.replace(";", ",")
		if title.upper() == presentation.upper():
			title = str(exceptions['Título Canônico'][pos])
			break

	return title


def issn_exceptions(name, issn):
	exceptions = pd.read_csv('Exceções/excecoes_issn.CSV', sep=';', encoding='utf-8')
	for pos, event in enumerate(exceptions['Nome Evento']):
		name= name.replace(";", ",")
		if name.upper() == event.upper():
			issn = str(exceptions['ISSN'][pos])
			break
	return issn


def event_exceptions(name, event_name, titulo_trabalho, exceptions_dict):
	exceptions = pd.read_csv('Exceções/excecoes_eventos.CSV', sep=';', encoding='utf-8')
	for pos, event_registered in enumerate(exceptions['Nome Evento Cadastrado']):
		name= name.replace(";", ",")
		if name.upper() == event_registered.upper():
			exceptions_dict['Nome Trabalho'].append(titulo_trabalho)
			exceptions_dict['Nome Evento Cadastrado'].append(name)
			exceptions_dict['Nome Evento Canônico'].append(exceptions['Nome Evento Canônico'][pos])

			name= exceptions['Nome Evento Canônico'][pos]
			event_name = name
			break
	
	return (name, event_name, exceptions_dict)


def initials_exceptions(name):
	initials = " "
	name= name.replace("*", "")
	exceptions = pd.read_csv('Exceções/excecoes_siglas.CSV', sep=';', encoding='utf-8')
	for pos, event in enumerate(exceptions['Nome Evento']):
		name= name.replace(";", ",")
		if name.upper() == event.upper():
			initials = exceptions['Sigla'][pos]
			break

	return initials
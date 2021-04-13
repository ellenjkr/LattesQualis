import unidecode

def trata_virgulas(autor):
	if "," in autor and autor[-1] != ",":
		autor_array = autor.split(", ")
		sobrenome = autor_array[0]
		autor = autor_array[1] + " " + sobrenome

	return autor


def trata_preposicoes(autor):
	nome = autor
	nome = nome.split(" ")
	autor = ""
	dic_preposicoes = {"De": "de", "Da": "da", "Das": "das", "Do": "do", "Dos": "dos"}
	for pos, palavra in enumerate(nome):
		if palavra in dic_preposicoes:
			palavra = dic_preposicoes[palavra]
		if pos == 0:
			autor += palavra
		else:
			autor += " " + palavra

	return autor


def trata_exceçoes(autor):
	dic_excecoes = {"cornélio celso de brasil camargo": "C. Celso de Brasil Camargo", 
					"c.f.r. geyer": "Cláudio Fernando Resin Geyer",
					"c.o. rolim": "Carlos Oberdan Rolim",
					"christiane heeman": "Christiane Heemann",
					"claudia zanbom": "Cláudia Neli de Souza Zambon",
					"jorge m. sa da silva": "Jorge Sa Silva",
					"raimundo celeste ghizoni theive": "Raimundo Celeste Ghizoni Teive",
					"rudimar luís scaranto dazze": "Rudimar Luís Scaranto Dazzi",
					"angelica karize viecelli": "Karize Viecelli",
					"angélica karize viecelli": "Karize Viecelli", 
					"jéferson fernandes da silva": "Jeferson Fernandes da Silva"}

	nome = autor.lower()

	if nome in dic_excecoes:
		autor = dic_excecoes[nome]

	return autor


def em_lista_professores(professores, autor):
	for professor in professores["Nome"]:
		if str(professor) != 'nan':
			professor_temp = professor.replace("-", " ")
			professor_array = unidecode.unidecode(professor_temp).lower().split(" ")
			autor_temp = autor.replace("-", " ")
			autor_array = unidecode.unidecode(autor_temp).lower().split(" ")
			iguais = False
			cont_iguais = 0
			if (professor_array[0] == autor_array[0]) or ((len(professor_array[0]) == 1 or (len(professor_array[0]) == 2 and professor_array[0][1] ==".")) and autor_array[0][0] == professor_array[0][0]) or ((len(autor_array[0]) == 1 or (len(autor_array[0]) == 2 and autor_array[0][1] == ".")) and professor_array[0][0] == autor_array[0][0]):
				if len(autor) < len(professor):
					for num in range(1, len(autor_array)):
						if autor_array[num] in professor_array:
							cont_iguais +=1
						elif len(autor_array[num]) == 2 and autor_array[num][1] == ".":
							for palavra in professor_array[1:]:
								if autor_array[num][0] == palavra[0]:
									cont_iguais +=1
						elif len(autor_array[num]) == 1:
							for palavra in professor_array[1:]:
								if autor_array[num] == palavra[0]:
									cont_iguais +=1
					if cont_iguais >= len(autor_array)-1:
						iguais = True
				else:
					for num in range(1, len(professor_array)):
						if professor_array[num] in autor_array:
							cont_iguais +=1
						elif len(professor_array[num]) == 2 and professor_array[num][1] == ".":
							for palavra in autor_array[1:]:
								if professor_array[num][0] == palavra[0]:
									cont_iguais +=1
						elif len(professor_array[num]) == 1:
							for palavra in autor_array[1:]:
								if professor_array[num] == palavra[0]:
									cont_iguais +=1

					if cont_iguais >= len(professor_array)-1:
						iguais = True

			if iguais == True:
				autor = professor
				break

	autor = trata_preposicoes(autor)
	autor = trata_exceçoes(autor)
	return autor

def em_lista_autores(lista_autores, autor):
	tem = False
	qtd = 0

	removeu = False
	lista = autor.split(" ")
	for pos, palavra in enumerate(lista):
		if lista.count(palavra) > 1 and len(palavra) > 3:
			if removeu == False:
				lista.pop(pos)
				removeu = True
	if removeu == True:
		autor = lista[0]
		for palavra in lista[1:]:
			autor += " " + palavra

	autor = trata_preposicoes(autor)
	autor = trata_exceçoes(autor)

	for posicao, nome in enumerate(lista_autores):
		nome_temp = nome.replace("-", " ")
		nome_array = unidecode.unidecode(nome_temp).lower().split(" ")
		autor_temp = autor.replace("-", " ")
		autor_array = unidecode.unidecode(autor_temp).lower().split(" ")
		iguais = False
		cont_iguais = 0
		if (nome_array[0] == autor_array[0]) or ((len(nome_array[0]) == 1 or (len(nome_array[0]) == 2 and nome_array[0][1] ==".")) and autor_array[0][0] == nome_array[0][0]) or ((len(autor_array[0]) == 1 or (len(autor_array[0]) == 2 and autor_array[0][1] == ".")) and nome_array[0][0] == autor_array[0][0]):
			if len(autor) < len(nome):
				for num in range(1, len(autor_array)):
					if autor_array[num] in nome_array:
						cont_iguais +=1
					elif len(autor_array[num]) == 2 and autor_array[num][1] == ".":
						for palavra in nome_array[1:]:
							if autor_array[num][0] == palavra[0]:
								cont_iguais +=1
					elif len(autor_array[num]) == 1:
						for palavra in nome_array[1:]:
							if autor_array[num] == palavra[0]:
								cont_iguais +=1
				if cont_iguais >= len(autor_array)-1:
					iguais = True
			else:
				for num in range(1, len(nome_array)):
					if nome_array[num] in autor_array:
						cont_iguais +=1
					elif len(nome_array[num]) == 2 and nome_array[num][1] == ".":
						for palavra in autor_array[1:]:
							if nome_array[num][0] == palavra[0]:
								cont_iguais +=1
					elif len(nome_array[num]) == 1:
						for palavra in autor_array[1:]:
							if nome_array[num] == palavra[0]:
								cont_iguais +=1

				if cont_iguais >= len(nome_array)-1:
					iguais = True

		if iguais == True:

			if len(autor) > len(nome):
				if qtd == 0:
					lista_autores[posicao] = autor
				else:
					del lista_autores[posicao]
			elif len(autor) == len(nome) and "-" in autor:
				if qtd == 0:
					lista_autores[posicao] = autor
				else:
					del lista_autores[posicao]
			else:
				autor = nome
			qtd += 1 # Para se tiver mais de um compativel, os demais vao ser removidos
			tem = True
			# break

	
	if tem == False:
		lista_autores.append(autor)

	return (lista_autores, autor)
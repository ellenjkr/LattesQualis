import unidecode

def treat_commas(author):
	if "," in author and author[-1] != ",": # If the name was registered with a comma
		author_array = author.split(", ") 
		last_name = author_array[0]
		author = author_array[1] + " " + last_name

	return author


def treat_prepositions(author): # All the prepositions must begin with a lowercase letter
	name = author
	name = name.split(" ") 
	author = ""
	prepositions_dict = {"De": "de", "Da": "da", "Das": "das", "Do": "do", "Dos": "dos"}
	for pos, word in enumerate(name):
		if word in prepositions_dict:
			word = prepositions_dict[word]
		if pos == 0:
			author += word
		else:
			author += " " + word

	return author


def treat_exceptions(author): # Names that are exceptions
	exceptions_dict = {"cornélio celso de brasil camargo": "C. Celso de Brasil Camargo", 
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

	name = author.lower()

	if name in exceptions_dict:
		author = exceptions_dict[name]

	return author


def search_professors_list(professors, author):
	for professor in professors["Nome"]:
		if str(professor) != 'nan': # If it's not null

			# ======================================================

			# Remove accents, lowercase, split words
			professor_temp = professor.replace("-", " ")
			professor_array = unidecode.unidecode(professor_temp).lower().split(" ")
			author_temp = author.replace("-", " ")
			author_array = unidecode.unidecode(author_temp).lower().split(" ")

			# ======================================================

			# Verifies if the author's name is on the list of professors (searches for similarities)
			equals = False 
			count_equals = 0 

			# If professor first name equals author first name, or 
			# professor first name begins with one letter or with two letters, the first being ".", and professor's name begins with the same letter as the author's name
			# vice versa 
			if (professor_array[0] == author_array[0]) or ((len(professor_array[0]) == 1 or (len(professor_array[0]) == 2 and professor_array[0][1] ==".")) and author_array[0][0] == professor_array[0][0]) or ((len(author_array[0]) == 1 or (len(author_array[0]) == 2 and author_array[0][1] == ".")) and professor_array[0][0] == author_array[0][0]):
				if len(author) < len(professor): 
					# Count the amount of equal words
					for num in range(1, len(author_array)):
						if author_array[num] in professor_array:
							count_equals +=1
						elif len(author_array[num]) == 2 and author_array[num][1] == ".":
							for word in professor_array[1:]:
								if author_array[num][0] == word[0]:
									count_equals +=1
						elif len(author_array[num]) == 1:
							for word in professor_array[1:]:
								if author_array[num] == word[0]:
									count_equals +=1
					if count_equals >= len(author_array)-1:
						equals = True
				else:
					for num in range(1, len(professor_array)):
						if professor_array[num] in author_array:
							count_equals +=1
						elif len(professor_array[num]) == 2 and professor_array[num][1] == ".":
							for word in author_array[1:]:
								if professor_array[num][0] == word[0]:
									count_equals +=1
						elif len(professor_array[num]) == 1:
							for word in author_array[1:]:
								if professor_array[num] == word[0]:
									count_equals +=1

					if count_equals >= len(professor_array)-1:
						equals = True

			if equals == True:
				author = professor
				break

	author = treat_prepositions(author)
	author = treat_exceptions(author)
	return author

def search_authors_list(authors_list, author):
	found = False
	amount = 0

	removed = False
	_list = author.split(" ")
	for pos, word in enumerate(_list):
		if _list.count(word) > 1 and len(word) > 3:
			if removed == False:
				_list.pop(pos)
				removed = True
	if removed == True:
		author = _list[0]
		for word in _list[1:]:
			author += " " + word

	author = treat_prepositions(author)
	author = treat_exceptions(author)

	for position, name in enumerate(authors_list):

		# ========================================================================

		# Remove accents, lowercase, split words
		name_temp = name.replace("-", " ")
		name_array = unidecode.unidecode(name_temp).lower().split(" ")
		author_temp = author.replace("-", " ")
		author_array = unidecode.unidecode(author_temp).lower().split(" ")

		# ========================================================================

		# Almost the same as search_professors_list
		equals = False
		count_equals = 0
		if (name_array[0] == author_array[0]) or ((len(name_array[0]) == 1 or (len(name_array[0]) == 2 and name_array[0][1] ==".")) and author_array[0][0] == name_array[0][0]) or ((len(author_array[0]) == 1 or (len(author_array[0]) == 2 and author_array[0][1] == ".")) and name_array[0][0] == author_array[0][0]):
			if len(author) < len(name):
				for num in range(1, len(author_array)):
					if author_array[num] in name_array:
						count_equals +=1
					elif len(author_array[num]) == 2 and author_array[num][1] == ".":
						for word in name_array[1:]:
							if author_array[num][0] == word[0]:
								count_equals +=1
					elif len(author_array[num]) == 1:
						for word in name_array[1:]:
							if author_array[num] == word[0]:
								count_equals +=1
				if count_equals >= len(author_array)-1:
					equals = True
			else:
				for num in range(1, len(name_array)):
					if name_array[num] in author_array:
						count_equals +=1
					elif len(name_array[num]) == 2 and name_array[num][1] == ".":
						for word in author_array[1:]:
							if name_array[num][0] == word[0]:
								count_equals +=1
					elif len(name_array[num]) == 1:
						for word in author_array[1:]:
							if name_array[num] == word[0]:
								count_equals +=1

				if count_equals >= len(name_array)-1:
					equals = True

		# ========================================================================

		# Remove repeated names 

		if equals == True:

			# The biggest name is the one that stays on the list
			if len(author) > len(name): 
				if amount == 0:
					authors_list[position] = author
				else:
					del authors_list[position]
			elif len(author) == len(name) and "-" in author:
				if amount == 0:
					authors_list[position] = author
				else:
					del authors_list[position]
			else:
				author = name
			amount += 1 # Increases the number of repetitions. If there's more than one match, the others will be removed
			found = True
			# break

		# ========================================================================
		
	if found == False:
		authors_list.append(author)

	return (authors_list, author)
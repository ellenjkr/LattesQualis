from _Funções_e_Valores.values import FILE


class Students_and_Egress(): # Class for students and egress that holds their name, active-period and egress year
	def __init__(self, name, period, egress_year):
		super(Students_and_Egress, self).__init__()
		self.name = name
		self.period = period
		self.egress_year = egress_year


class Student(): 
	def __init__(self, students, quadrennium):
		super(Student, self).__init__()
		self.students = students
		self.quadrennium = quadrennium

	def get_students_list(self):
		students_list = []

		if FILE == "UNIVALI 2013-2016":
			students_list = []
			for pos, student in enumerate(self.students["Aluno"]): # Iterates through the students
				if str(student) != "nan":
					period = {self.quadrennium[0]: False, self.quadrennium[1]: False, self.quadrennium[2]: False, self.quadrennium[3]: False}
					if str(self.students["Ingresso"][pos]) != "nan":
						ingress_year = int(str(self.students["Ingresso"][pos])[7:])
						if str(ingress_year) in period: # If the ingress year it's in the quadrennium
							period[str(ingress_year)] = True # Sets the ingress year as true

						egress_year = str(self.students["Defesa"][pos])
						if egress_year != '' and egress_year != "nan":
							egress_year = int(str(int(self.students["Egresso"][pos]))[2:])
							if egress_year < int(self.quadrennium[3]):
								limit_year = egress_year
							else:
								limit_year = int(self.quadrennium[3]) # The last year of the quadrennium
						for i in range(1, limit_year+1):
							if str(ingress_year + i) in period:
								period[str(ingress_year + i)] = True # Set the all the years after the ingress year and before the limit year as true

						students_list.append(Students_and_Egress(student, period, egress_year))

		else:
			for pos, student in enumerate(self.students["Aluno"]): # Iterates through the students
				if str(student) != "nan":
					period = {}
					for year in self.quadrennium:
						period[year] = False
					if str(self.students["Ingresso"][pos]) != "nan":
						ingress_year = int(str(self.students["Ingresso"][pos])[7:])
						if str(ingress_year) in period: # If the ingress year it's in the quadrennium
							period[str(ingress_year)] = True # Sets the ingress year as true

						limit_year = int(self.quadrennium[3]) # The last year of the quadrennium
						for i in range(1, limit_year+1):
							if str(ingress_year + i) in period:
								period[str(ingress_year + i)] = True # Set the all the years after the ingress year and before the limit year as true

						egress_year = str(self.students["Defesa"][pos])
						if egress_year != '' and egress_year != "nan":
							egress_year = int(egress_year[7:])
							if str(egress_year) in period: # If the egress year it's in the quadrennium
								period[str(egress_year)] = True # Sets the egress year as true 
							for i in range(1, 6):
								if str(egress_year + i) in period:
									period[str(egress_year + i)] = True # Sets the 5 years after the egress year as true

						students_list.append(Students_and_Egress(student, period, egress_year))
		return students_list


class Egress():
	def __init__(self, egress, quadrennium):
		super(Egress, self).__init__()
		self.egress = egress
		self.quadrennium = quadrennium
		
	def get_egress_list(self):
		egress_list = []
		for pos, student in enumerate(self.egress["Aluno"]):
			if str(student) != "nan":
				period = {}
				for year in self.quadrennium:
					period[year] = False
				if str(self.egress["Egresso"][pos]) != "nan":
					egress_year = int(str(int(self.egress["Egresso"][pos]))[2:])
					if egress_year >= (int(self.quadrennium[0])-5): # Only the ones after the (first year of the quaddrenium - 5)
						if str(egress_year) in period: # If the egress year it's in the quadrennium
							period[str(egress_year)] = True # Sets the egress year as true
						for i in range(1, 6):
							if str(egress_year + i) in period:
								period[str(egress_year + i)] = True # Sets the 5 years after the egress year as true

						ingress_year = str(self.egress["Ingresso"][pos]).split("-")[2]
						if ingress_year in self.quadrennium: # If the ingress year it's in the quadrennium
							for i in range(self.quadrennium.index(ingress_year), len(self.quadrennium)):
								period[self.quadrennium[i]] = True # Sets all the years after the ingress year as true

						egress_list.append(Students_and_Egress(student, period, egress_year))

		return egress_list
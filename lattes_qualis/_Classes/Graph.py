import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
import matplotlib.ticker as mticker

import matplotlib
import pandas as pd
from openpyxl.drawing.image import Image
import PIL
import openpyxl
import os

from _Funções_e_Valores.values import ND, Y_LIMITS, Y_LIMITS_PROCEEDINGS, Y_LIMITS_JOURNALS, HAS_EVENTS

# tabela = {f"Tipo/Qualis {self.qualis_year}": tipo_qualis, "Quantidade": [], "Porcentagem": [], "Quantidade com alunos/egressos":[], "Porcentagem alunos/egressos":[]}
class Graphs():
	def __init__(self, indicators, per_upperstrata, per_upperstrata_ae, authors_list, qualis_year, temp_folder):
		super(Graphs, self).__init__()
		self.indicators = indicators 
		self.per_upperstrata = pd.DataFrame(columns=["Nome", "Data", "Porcentagem", "Porcentagem Acumulada"])
		self.per_upperstrata["Data"] = per_upperstrata
		self.per_upperstrata["Nome"] = authors_list
		self.per_upperstrata_ae = pd.DataFrame(columns=["Nome", "Data", "Porcentagem", "Porcentagem Acumulada"])
		self.per_upperstrata_ae["Data"] = per_upperstrata_ae
		self.per_upperstrata_ae["Nome"] = authors_list
		self.qualis_year = qualis_year
		self.temp_folder = temp_folder

		self.dict = self.fill_dict()
		self.images = []
		self.build_graph()


	def fill_dict(self):
		# Fill a dictionary with all the data

		self.indicators["Quantidade com alunos/egressos"] = self.indicators["Quantidade com alunos/egressos"].astype("int", errors="ignore", copy=False)
		dic = {}
		dic["Irestrito"] = self.indicators.loc[self.indicators[f"Tipo/Qualis {self.qualis_year}"] == "Irestrito"].reset_index(drop=True)
		dic["Igeral"] = self.indicators.loc[self.indicators[f"Tipo/Qualis {self.qualis_year}"] == "Igeral"].reset_index(drop=True)
		
		dic["Periódicos"] = self.indicators.loc[self.indicators[f"Tipo/Qualis {self.qualis_year}"] == "Periódicos"].reset_index(drop=True)
		dic["Periódicos com alunos/egressos"] = dic["Periódicos"]

		if HAS_EVENTS == True:
			dic["Anais"] = self.indicators.loc[self.indicators[f"Tipo/Qualis {self.qualis_year}"] == "Anais"].reset_index(drop=True)
			dic["Anais com alunos/egressos"] = dic["Anais"]

		if self.qualis_year == "CC 2016":
			dic["A1-B1"] = self.indicators.loc[self.indicators[f"Tipo/Qualis {self.qualis_year}"] == "A1-B1"].reset_index(drop=True)
			dic["A1-B1 com alunos/egressos"] = dic["A1-B1"]

			dic["B2-B5"] = self.indicators.loc[self.indicators[f"Tipo/Qualis {self.qualis_year}"] == "B2-B5"].reset_index(drop=True)
			dic["B2-B5 com alunos/egressos"] = dic["B2-B5"]

		elif self.qualis_year ==  "2019":
			dic["A1-A4"] = self.indicators.loc[self.indicators[f"Tipo/Qualis {self.qualis_year}"] == "A1-A4"].reset_index(drop=True)
			dic["A1-A4 com alunos/egressos"] = dic["A1-A4"]

			dic["B1-B4"] = self.indicators.loc[self.indicators[f"Tipo/Qualis {self.qualis_year}"] == "B1-B4"].reset_index(drop=True)
			dic["B1-B4 com alunos/egressos"] = dic["B1-B4"]

		return dic

	def calculate_data(self, key, df=None):
		data_sum = 0	
		data = None
		if key != "Periódicos A1-A4" and key != "Periódicos A1-A4 com alunos/egressos" and key != "Periódicos A1-B1" and key != "Periódicos A1-B1 com alunos/egressos":
			if "com alunos/egressos" in key:
				amount_col = "Quantidade com alunos/egressos"
			else:
				amount_col = "Quantidade"

			df = self.dict[key]
			for pos, i in enumerate(df[amount_col]):
				df.loc[pos, amount_col] = float(str(i).replace(",", "."))
				if key == "Irestrito" or key == "Igeral":
					if df[amount_col][pos] != 0.0 and df[amount_col][pos] != 0 and str(df[amount_col][pos]).lower() != "nan":
						df.loc[pos, amount_col] = round(df[amount_col][pos], 1)
					else:
						df.loc[pos, amount_col] = 0
				else:
					df.loc[pos, amount_col] = int(df[amount_col][pos])
				data_sum += df[amount_col][pos]

			data = pd.DataFrame(columns=["Nome", "Data", "Porcentagem", "Porcentagem Acumulada"])
			data["Nome"] = self.dict[key]["Nome Autor"]
			data["Data"] = df[amount_col]
		else:
			for i in df["Data"]:
				data_sum += i
			data = df

		data = data.sort_values(by='Data', ascending=False).reset_index(drop=True)

		for pos, i in enumerate(data["Data"]):
			if data_sum != 0:
				data.loc[pos, "Porcentagem"] = 100/data_sum * i
			else:
				data.loc[pos, "Porcentagem"] = 0
			if pos == 0:
				data.loc[pos, "Porcentagem Acumulada"] = data["Porcentagem"][pos]
			else:
				data.loc[pos, "Porcentagem Acumulada"] = data["Porcentagem Acumulada"][pos-1]+data["Porcentagem"][pos]

		return data

	def autolabel(self, rects, ax, key, xpos='center'):
	    xpos = xpos.lower()  # normalize the case of the parameter
	    ha = {'center': 'center', 'right': 'left', 'left': 'right'}
	    offset = {'center': 0.5, 'right': 0.57, 'left': 0.43}  # x_txt = x + w*off

	    for rect in rects:
	        height = rect.get_height()
	        if key == "Irestrito" or key == "Igeral":
	        	ax.text(rect.get_x() + rect.get_width()*offset[xpos], 1.01*height,
	                	'{}'.format(height), ha=ha[xpos], va='bottom', fontdict={"fontsize":13})
	        else:
	        	ax.text(rect.get_x() + rect.get_width()*offset[xpos], 1.01*height,
	                	'{}'.format(int(height)), ha=ha[xpos], va='bottom', fontdict={"fontsize":13})

	    return ax

	def build_graph(self):
		try:
			os.mkdir(self.temp_folder) # Creates a temporary folder to hold the graphs images
		except:
			pass

		keys = [] # List with dictionary keys
		for key in self.dict.keys():
			keys.append(key)

		if self.qualis_year == "CC 2016": # If it's the 2016 qualis it uses A1-B1
			keys.append("Periódicos A1-B1")
			keys.append("Periódicos A1-B1 com alunos/egressos")
		elif self.qualis_year == "2019":
			keys.append("Periódicos A1-A4") # If it's the 2019 qualis it uses A1-A4
			keys.append("Periódicos A1-A4 com alunos/egressos")

		for key in keys:
			if key == "Periódicos A1-A4" or key == "Periódicos A1-B1": # Calculates the data for upper strata journals
				data = self.calculate_data(key, self.per_upperstrata)
			elif key == "Periódicos A1-A4 com alunos/egressos" or key == "Periódicos A1-B1 com alunos/egressos": # Calculates the data for upper strata journals with students and egress
				data = self.calculate_data(key, self.per_upperstrata_ae)
			else: # Calculate the data for the other graphs
				data = self.calculate_data(key)


			fig = plt.figure(figsize=(10,6))
			ax = fig.add_subplot(1, 1, 1)

			# =======================================================================
			# DEFINES THE TITLES ALONG WITH THE DOC_PPG AND THE TOTAL_PPG 

			total_ppg = 0
			for i in data["Data"]:
				total_ppg += i
			doc_ppg = total_ppg/ND
			if ".0" in str(total_ppg): # Converts total_ppg to int
				total_ppg = int(total_ppg)
			if ".0" in str(doc_ppg): # Converts doc_ppg to int
				doc_ppg = int(doc_ppg)
			
			# Set the title for each dict key
			titles = {"Periódicos": "Artigos em Periódicos", 
					  "Periódicos com alunos/egressos": "Artigos em Periódicos com Alunos/Egressos",
					  "Anais": "Artigos em Anais de Eventos",
					  "Anais com alunos/egressos": "Artigos em Anais de Eventos com Alunos/Egressos",
					  "A1-A4": "Artigos em Periódicos e em Anais de Eventos A1-A4",
					  "A1-A4 com alunos/egressos": "Artigos em Periódicos e em Anais de Eventos A1-A4 com Alunos/Egressos",
					  "A1-B1": "Artigos em Periódicos e em Anais de Eventos A1-B1",
					  "A1-B1 com alunos/egressos": "Artigos em Periódicos e em Anais de Eventos A1-B1 com Alunos/Egressos",
					  "B1-B4": "Artigos em Periódicos e em Anais de Eventos B1-B4",
					  "B1-B4 com alunos/egressos": "Artigos em Periódicos e em Anais de Eventos B1-B4 com Alunos/Egressos",
					  "B2-B5": "Artigos em Periódicos e em Anais de Eventos B2-B5",
					  "B2-B5 com alunos/egressos": "Artigos em Periódicos e em Anais de Eventos B2-B5 com Alunos/Egressos", 
					  "Periódicos A1-A4": "Artigos em Periódicos A1-A4",
					  "Periódicos A1-A4 com alunos/egressos": "Artigos em Periódicos A1-A4 com Alunos/Egressos",
					  "Periódicos A1-B1": "Artigos em Periódicos A1-B1",
					  "Periódicos A1-B1 com alunos/egressos": "Artigos em Periódicos A1-B1 com Alunos/Egressos"
					  }
			try:
				title = titles[key]
			except:
				title = key

			plt.text(x=0.5, y=0.94, s=title, fontsize=18, ha="center", transform=fig.transFigure)
			plt.text(x=0.5, y=0.88, s= f"(PPGtotal = {round(total_ppg, 1)}, PPGdoc = {round(doc_ppg, 1)})", fontsize=15, ha="center", transform=fig.transFigure)
			plt.subplots_adjust(top=0.8, wspace=0.3)

			# =======================================================================
			# CUSTOMIZE GRAPH:

			matplotlib.rc('xtick', labelsize=15) 
			matplotlib.rc('ytick', labelsize=15) 

			rects = ax.bar(data["Nome"], data["Data"], color="C0", zorder=3) # Creates the bar graph
			ax.set_ylim([0, Y_LIMITS[key]]) # Set the "y" limits
			ax.tick_params(axis="y", colors="C0") # Set "y" ticks color
			ax.axes.yaxis.set_ticklabels([]) # Remove "y" tick labels

			try:
				ticks_loc = list(ax.get_xticks())
				ax.xaxis.set_major_locator(mticker.FixedLocator(ticks_loc))
				ax.set_xticklabels(data["Nome"], size=15, rotation=75) # Customize "x" tick labels
			except:
				ax.set_xticklabels(data["Nome"], size=15, rotation=75) # Customize "x" tick labels
				ticks_loc = list(ax.get_xticks())
				ax.xaxis.set_major_locator(mticker.FixedLocator(ticks_loc))


			ax2 = ax.twinx() # Add another graph to the bar one
			ax2.plot(data["Nome"], data["Porcentagem Acumulada"], color="C1", marker="o", ms=5) # Creates the line graph
			ax2.set_yticks([0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]) # Set the "y" ticks
			ax2.yaxis.set_major_formatter(PercentFormatter())
			ax2.tick_params(axis="y", colors="C1") # Set "y" ticks color 
			ax2.yaxis.grid(color="C0") # Set the grid color
			ax2.set_ylim([0, 100]) # Y limits

			# Remove spines
			ax.spines["top"].set_visible(False) 
			ax.spines["right"].set_visible(False)
			ax.spines["left"].set_visible(False)

			ax2.spines["top"].set_visible(False) 
			ax2.spines["right"].set_visible(False)
			ax2.spines["left"].set_visible(False)

			fig.tight_layout()
			ax = self.autolabel(rects, ax, key) # Adds the label for the bars
			ax.tick_params(
			    axis='y',
			    which='both',
			    right=False,
			    left=False) 

			# =======================================================================

			key = key.replace("/", "-")
			plt.savefig(f'{self.temp_folder}/{key}.png') # Saves the graph to the temporary folder
			plt.close('all')
			self.images.append(f'{self.temp_folder}/{key}.png') # List with graphs paths

	def add_graphs(self, ws): # Adds the graphs to the excel sheet
		positions = ["A1", "D1", "A7", "D7", "A13", "D13", "A20", "D20", "A26", "D26", "A32", "D32"]
		for pos, image in enumerate(self.images):
			img = PIL.Image.open(image)
			basewidth = 600
			wpercent = (basewidth/float(img.size[0]))
			hsize = int((float(img.size[1])*float(wpercent)))
			img = img.resize((basewidth,hsize), PIL.Image.ANTIALIAS)
			img.save(image) 

			img = Image(image)
			ws.add_image(img, positions[pos])

		return ws

class Graphs_Proceedings_Journals():
	def __init__(self, df, key):
		super(Graphs_Proceedings_Journals, self).__init__()
		self.df = df
		self.key = key
		self.build_graph()

	def calculate_data(self):
		data_sum = 0	
		for pos, i in enumerate(self.df["Quantidade"]):
			data_sum += int(i)

		data = pd.DataFrame(columns=["Nome", "Data", "Porcentagem", "Porcentagem Acumulada"])
		if self.key == "Anais de Eventos Utilizados para Publicação":
			data["Nome"] = self.df["Sigla"]
		else:
			data["Nome"] = self.df["Nome de Publicação"]

		data["Data"] = self.df["Quantidade"]
		data = data.sort_values(by='Data', ascending=False).reset_index(drop=True)

		for pos, i in enumerate(data["Data"]):
			data.loc[pos, "Porcentagem"] = 100/data_sum * i
			if pos == 0:
				data.loc[pos, "Porcentagem Acumulada"] = data["Porcentagem"][pos]
			else:
				data.loc[pos, "Porcentagem Acumulada"] = data["Porcentagem Acumulada"][pos-1]+data["Porcentagem"][pos]

		return data

	def autolabel(self, rects, ax, key, xpos='center'):
	    xpos = xpos.lower()  # normalize the case of the parameter
	    ha = {'center': 'center', 'right': 'left', 'left': 'right'}
	    offset = {'center': 0.5, 'right': 0.57, 'left': 0.43}  # x_txt = x + w*off

	    for rect in rects:
	        height = rect.get_height()
	        if key == "Irestrito" or key == "Igeral":
	        	ax.text(rect.get_x() + rect.get_width()*offset[xpos], 1.01*height,
	                	'{}'.format(height), ha=ha[xpos], va='bottom', fontdict={"fontsize":13})
	        else:
	        	ax.text(rect.get_x() + rect.get_width()*offset[xpos], 1.01*height,
	                	'{}'.format(int(height)), ha=ha[xpos], va='bottom', fontdict={"fontsize":13})

	    return ax

	def build_graph(self):
		try:
			os.mkdir("temp") # Creates a temporary folder to hold the graphs images
		except:
			pass

		if self.key == "Anais de Eventos Utilizados para Publicação":
			y_limits_pj = Y_LIMITS_PROCEEDINGS # y_limits_pj = y_limits proceedings and journals
		else:
			y_limits_pj = Y_LIMITS_JOURNALS
		

		data = self.calculate_data()
		names = []
		for pos, name in enumerate(data["Nome"]):
			if len(name) > 30:
				if name[:30] not in names:
					data.loc[pos, "Nome"] = f"{name[:30]}..."
					names.append(name[:30])
				else:
					data.loc[pos, "Nome"] = f"{name[:40]}..."
					names.append(name[:40])

		matplotlib.rc('xtick', labelsize=15) 
		matplotlib.rc('ytick', labelsize=15) 

		if self.key == "Anais de Eventos Utilizados para Publicação":
			fig = plt.figure(figsize=(25,10))
		else:
			fig = plt.figure(figsize=(20,10))
		ax = fig.add_subplot(1, 1, 1)


		# =======================================================================
		# DEFINES THE TITLES ALONG WITH THE DOC_PPG AND THE TOTAL_PPG 

		total_ppg = 0
		for i in data["Data"]:
			total_ppg += i
		doc_ppg = total_ppg/ND
		if ".0" in str(total_ppg):
			total_ppg = int(total_ppg)
		if ".0" in str(doc_ppg):
			doc_ppg = int(doc_ppg)

		plt.text(x=0.5, y=0.94, s=self.key, fontsize=18, ha="center", transform=fig.transFigure)
		plt.text(x=0.5, y=0.88, s= f"(PPGtotal = {round(total_ppg, 1)}, PPGdoc = {round(doc_ppg, 1)})", fontsize=15, ha="center", transform=fig.transFigure)
		plt.subplots_adjust(top=0.8, wspace=0.3)

		# =======================================================================

		rects = ax.bar(data["Nome"], data["Data"], color="C0", zorder=3) # Creates the bar graph
		ax.set_ylim([0, y_limits_pj]) # Set the "y" limits
		ax.tick_params(axis="y", colors="C0") # Set "y" ticks color

		ticks_loc = list(ax.get_xticks())
		ax.xaxis.set_major_locator(mticker.FixedLocator(ticks_loc))
		if self.key == "Anais de Eventos Utilizados para Publicação":
			ax.set_xticklabels(data["Nome"], size=14, rotation=90) # Customize "x" tick labels
		else:
			ax.set_xticklabels(data["Nome"], size=12, rotation=90) # Customize "x" tick labels
		ax.axes.yaxis.set_ticklabels([]) # Remove "y" tick labels

		ax2 = ax.twinx() # Add another graph to the bar one
		ax2.plot(data["Nome"], data["Porcentagem Acumulada"], color="C1", marker="o", ms=5) # Creates the line graph
		ax2.set_yticks([0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]) # Set the "y" ticks
		ax2.yaxis.set_major_formatter(PercentFormatter())
		ax2.tick_params(axis="y", colors="C1") # Set "y" ticks color 
		ax2.yaxis.grid(color="C0") # Set the grid color
		ax2.set_ylim([0, 100])  # Y limits

		# Remove spines
		ax.spines["top"].set_visible(False) 
		ax.spines["right"].set_visible(False)
		ax.spines["left"].set_visible(False)

		ax2.spines["top"].set_visible(False) 
		ax2.spines["right"].set_visible(False)
		ax2.spines["left"].set_visible(False)

		fig.tight_layout()
		ax = self.autolabel(rects, ax, self.key)
		ax.tick_params(
		    axis='y',
		    which='both',
		    right=False,
		    left=False) 

		# =======================================================================


		self.key = self.key.replace("/", "-")
		plt.savefig(f'temp/{self.key}.png') # Saves the graph to the temporary folder
		plt.close('all')
		self.image = f'temp/{self.key}.png' # Graph path

	def add_graphs(self, ws): # Adds the graphs to the excel sheet
		linha = ws.max_row + 2
		position = f"A{linha}"
		img = PIL.Image.open(self.image)
		basewidth = 1300
		wpercent = (basewidth/float(img.size[0]))
		hsize = int((float(img.size[1])*float(wpercent)))
		img = img.resize((basewidth,hsize), PIL.Image.ANTIALIAS)
		img.save(self.image) 

		img = Image(self.image)
		ws.add_image(img, position)

		return ws
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
import matplotlib
import pandas as pd
from openpyxl.drawing.image import Image
import PIL
import openpyxl
import os
from valores import ND

# tabela = {"Tipo/Qualis": tipo_qualis, "Quantidade": [], "Porcentagem": [], "Quantidade com alunos/egressos":[], "Porcentagem alunos/egressos":[]}
class Graficos():
	def __init__(self, indicadores, per_a1_a4, per_a1_a4_ae, lista_autores):
		super(Graficos, self).__init__()
		self.indicadores = indicadores
		self.per_a1_a4 = pd.DataFrame(columns=["Nome", "Dado", "Porcentagem", "Porcentagem Acumulada"])
		self.per_a1_a4["Dado"] = per_a1_a4
		self.per_a1_a4["Nome"] = lista_autores
		self.per_a1_a4_ae = pd.DataFrame(columns=["Nome", "Dado", "Porcentagem", "Porcentagem Acumulada"])
		self.per_a1_a4_ae["Dado"] = per_a1_a4_ae
		self.per_a1_a4_ae["Nome"] = lista_autores

		self.dict = self.fill_dict()
		self.images = []
		self.build_graph()
		#Pegar nome na parte que adiciona as informações de cada autor


	def fill_dict(self):
		self.indicadores["Quantidade com alunos/egressos"] = self.indicadores["Quantidade com alunos/egressos"].astype("int", errors="ignore", copy=False)
		dic = {}
		dic["Irestrito"] = self.indicadores.loc[self.indicadores["Tipo/Qualis"] == "Irestrito"].reset_index(drop=True)
		dic["Igeral"] = self.indicadores.loc[self.indicadores["Tipo/Qualis"] == "Igeral"].reset_index(drop=True)
		
		dic["Periódicos"] = self.indicadores.loc[self.indicadores["Tipo/Qualis"] == "Periódicos"].reset_index(drop=True)
		dic["Periódicos com alunos/egressos"] = dic["Periódicos"]

		dic["Anais"] = self.indicadores.loc[self.indicadores["Tipo/Qualis"] == "Anais"].reset_index(drop=True)
		dic["Anais com alunos/egressos"] = dic["Anais"]

		dic["A1-A4"] = self.indicadores.loc[self.indicadores["Tipo/Qualis"] == "A1-A4"].reset_index(drop=True)
		dic["A1-A4 com alunos/egressos"] = dic["A1-A4"]

		dic["B1-B4"] = self.indicadores.loc[self.indicadores["Tipo/Qualis"] == "B1-B4"].reset_index(drop=True)
		dic["B1-B4 com alunos/egressos"] = dic["B1-B4"]

		return dic

	def calculate_data(self, key, df=None):
		soma_dados = 0	
		dados = None
		if key != "Periódicos A1-A4" and key != "Periódicos A1-A4 com alunos/egressos":
			if "com alunos/egressos" in key:
				col_quantidade = "Quantidade com alunos/egressos"
			else:
				col_quantidade = "Quantidade"

			df = self.dict[key]
			for pos, i in enumerate(df[col_quantidade]):
				df[col_quantidade][pos] = float(str(i).replace(",", "."))
				if key == "Irestrito" or key == "Igeral":
					if df[col_quantidade][pos] != 0.0 and df[col_quantidade][pos] != 0 and str(df[col_quantidade][pos]).lower() != "nan":
						df[col_quantidade][pos] = round(df[col_quantidade][pos], 1)
					else:
						df[col_quantidade][pos] = 0
				else:
					df[col_quantidade][pos] = int(df[col_quantidade][pos])
				soma_dados += df[col_quantidade][pos]

			dados = pd.DataFrame(columns=["Nome", "Dado", "Porcentagem", "Porcentagem Acumulada"])
			dados["Nome"] = self.dict[key]["Nome Autor"]
			dados["Dado"] = df[col_quantidade]
		else:
			for i in df["Dado"]:
				soma_dados += i
			dados = df

		dados = dados.sort_values(by='Dado', ascending=False).reset_index(drop=True)

		for pos, i in enumerate(dados["Dado"]):
			if soma_dados != 0:
				dados["Porcentagem"][pos] = 100/soma_dados * i
			else:
				dados["Porcentagem"][pos] = 0
			if pos == 0:
				dados["Porcentagem Acumulada"][pos] = dados["Porcentagem"][pos]
			else:
				dados["Porcentagem Acumulada"][pos] = dados["Porcentagem Acumulada"][pos-1]+dados["Porcentagem"][pos]

		return dados

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
			os.mkdir("temp")
		except:
			pass
		# y_limits = [16, 16, 25, 25, 30, 30, 18, 18, 18, 18, 14, 14]
		y_limits = [30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30]
		keys = []
		for key in self.dict.keys():
			keys.append(key)
		keys.append("Periódicos A1-A4")
		keys.append("Periódicos A1-A4 com alunos/egressos")

		for pos, key in enumerate(keys):
			if key == "Periódicos A1-A4":
				dados = self.calculate_data(key, self.per_a1_a4)
			elif key == "Periódicos A1-A4 com alunos/egressos":
				dados = self.calculate_data(key, self.per_a1_a4_ae)
			else:
				dados = self.calculate_data(key)
			matplotlib.rc('xtick', labelsize=15) 
			matplotlib.rc('ytick', labelsize=15) 

			fig = plt.figure(figsize=(10,6))
			ax = fig.add_subplot(1, 1, 1)

			ppg_total = 0
			for i in dados["Dado"]:
				ppg_total += i
			ppg_doc = ppg_total/ND
			if ".0" in str(ppg_total):
				ppg_total = int(ppg_total)
			if ".0" in str(ppg_doc):
				ppg_doc = int(ppg_doc)
			

			titles = {"Periódicos": "Artigos em Periódicos", 
					  "Periódicos com alunos/egressos": "Artigos em Periódicos com Alunos/Egressos",
					  "Anais": "Artigos em Anais de Eventos",
					  "Anais com alunos/egressos": "Artigos em Anais de Eventos com Alunos/Egressos",
					  "A1-A4": "Artigos em Periódicos e em Anais de Eventos A1-A4",
					  "A1-A4 com alunos/egressos": "Artigos em Periódicos e em Anais de Eventos A1-A4 com Alunos/Egressos",
					  "B1-B4": "Artigos em Periódicos e em Anais de Eventos B1-B4",
					  "B1-B4 com alunos/egressos": "Artigos em Periódicos e em Anais de Eventos B1-B4 com Alunos/Egressos", 
					  "Periódicos A1-A4": "Artigos em Periódicos A1-A4",
					  "Periódicos A1-A4 com alunos/egressos": "Artigos em Periódicos A1-A4 com Alunos/Egressos"
					  }
			try:
				title = titles[key]
			except:
				title = key

			plt.text(x=0.5, y=0.94, s=title, fontsize=18, ha="center", transform=fig.transFigure)
			plt.text(x=0.5, y=0.88, s= f"(PPGtotal = {round(ppg_total, 1)}, PPGdoc = {round(ppg_doc, 1)})", fontsize=15, ha="center", transform=fig.transFigure)
			plt.subplots_adjust(top=0.8, wspace=0.3)

			rects = ax.bar(dados["Nome"], dados["Dado"], color="C0", zorder=3)
			ax.set_ylim([0, y_limits[pos]])
			ax.tick_params(axis="y", colors="C0")
			ax.set_xticklabels(dados["Nome"], size=15, rotation=75)
			ax.axes.yaxis.set_ticklabels([])

			ax2 = ax.twinx()
			ax2.plot(dados["Nome"], dados["Porcentagem Acumulada"], color="C1", marker="o", ms=5)
			ax2.set_yticks([0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
			ax2.yaxis.set_major_formatter(PercentFormatter())
			ax2.tick_params(axis="y", colors="C1")
			ax2.set_ylim([0, 100])

			ax.spines["top"].set_visible(False) 
			ax.spines["right"].set_visible(False)
			ax.spines["left"].set_visible(False)

			ax2.spines["top"].set_visible(False) 
			ax2.spines["right"].set_visible(False)
			ax2.spines["left"].set_visible(False)

			fig.tight_layout()
			ax2.yaxis.grid(color="C0")
			ax = self.autolabel(rects, ax, key)
			ax.tick_params(
			    axis='y',
			    which='both',
			    right=False,
			    left=False) 

			key = key.replace("/", "-")
			self.images.append(f'temp/{key}.png')
			plt.savefig(f'temp/{key}.png')

	def add_graphs(self, ws):
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

class Graficos_Anais_Periodicos():
	def __init__(self, df, key):
		super(Graficos_Anais_Periodicos, self).__init__()
		self.df = df
		self.key = key
		self.build_graph()

	def calculate_data(self):
		soma_dados = 0	
		for pos, i in enumerate(self.df["Quantidade"]):
			soma_dados += int(i)

		dados = pd.DataFrame(columns=["Nome", "Dado", "Porcentagem", "Porcentagem Acumulada"])
		if self.key == "Anais de Eventos Utilizados para Publicação":
			dados["Nome"] = self.df["Sigla"]
		else:
			dados["Nome"] = self.df["Nome de Publicação"]

		dados["Dado"] = self.df["Quantidade"]
		dados = dados.sort_values(by='Dado', ascending=False).reset_index(drop=True)

		for pos, i in enumerate(dados["Dado"]):
			dados["Porcentagem"][pos] = 100/soma_dados * i
			if pos == 0:
				dados["Porcentagem Acumulada"][pos] = dados["Porcentagem"][pos]
			else:
				dados["Porcentagem Acumulada"][pos] = dados["Porcentagem Acumulada"][pos-1]+dados["Porcentagem"][pos]

		return dados

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
			os.mkdir("temp")
		except:
			pass

		if self.key == "Anais de Eventos Utilizados para Publicação":
			y_limits = 30
		else:
			# y_limits = 10
			y_limits = 30
		
		dados = self.calculate_data()
		for pos, nome in enumerate(dados["Nome"]):
			if len(nome) > 30:
				dados["Nome"][pos] = f"{nome[:30]}..."

		matplotlib.rc('xtick', labelsize=15) 
		matplotlib.rc('ytick', labelsize=15) 

		if self.key == "Anais de Eventos Utilizados para Publicação":
			fig = plt.figure(figsize=(25,10))
		else:
			fig = plt.figure(figsize=(20,10))
		ax = fig.add_subplot(1, 1, 1)

		ppg_total = 0
		for i in dados["Dado"]:
			ppg_total += i
		ppg_doc = ppg_total/ND
		if ".0" in str(ppg_total):
			ppg_total = int(ppg_total)
		if ".0" in str(ppg_doc):
			ppg_doc = int(ppg_doc)

		# title = key + f" (PPGtotal = {round(ppg_total, 1)}, PPGdoc = {round(ppg_doc, 1)})"
		plt.text(x=0.5, y=0.94, s=self.key, fontsize=18, ha="center", transform=fig.transFigure)
		plt.text(x=0.5, y=0.88, s= f"(PPGtotal = {round(ppg_total, 1)}, PPGdoc = {round(ppg_doc, 1)})", fontsize=15, ha="center", transform=fig.transFigure)
		plt.subplots_adjust(top=0.8, wspace=0.3)
		# ax.set_title(title, size=18, pad=25)


		rects = ax.bar(dados["Nome"], dados["Dado"], color="C0", zorder=3)
		ax.set_ylim([0, y_limits])
		ax.tick_params(axis="y", colors="C0")
		if self.key == "Anais de Eventos Utilizados para Publicação":
			ax.set_xticklabels(dados["Nome"], size=14, rotation=90)
		else:
			ax.set_xticklabels(dados["Nome"], size=12, rotation=90)
		ax.axes.yaxis.set_ticklabels([])

		ax2 = ax.twinx()
		ax2.plot(dados["Nome"], dados["Porcentagem Acumulada"], color="C1", marker="o", ms=5)
		ax2.set_yticks([0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
		ax2.yaxis.set_major_formatter(PercentFormatter())
		ax2.tick_params(axis="y", colors="C1")
		ax2.set_ylim([0, 100])

		ax.spines["top"].set_visible(False) 
		ax.spines["right"].set_visible(False)
		ax.spines["left"].set_visible(False)

		ax2.spines["top"].set_visible(False) 
		ax2.spines["right"].set_visible(False)
		ax2.spines["left"].set_visible(False)

		fig.tight_layout()
		ax2.yaxis.grid(color="C0")
		ax = self.autolabel(rects, ax, self.key)
		ax.tick_params(
		    axis='y',
		    which='both',
		    right=False,
		    left=False) 

		self.key = self.key.replace("/", "-")
		self.image = f'temp/{self.key}.png'
		plt.savefig(f'temp/{self.key}.png')

	def add_graphs(self, ws):
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
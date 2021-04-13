import requests
import zipfile
import os
import pandas as pd
import re

# Read the file with the encoding utf-8 and if that doesn't work try with iso-8859-1
try:
	professors = pd.read_csv("UNIVALI - PPGC - Professores.csv", sep=";", encoding='utf-8') 
except:
	professors = pd.read_csv("UNIVALI - PPGC - Professores.csv", sep=";", encoding='iso-8859-1') 

professors = pd.read_csv("Relatório Lattes - Docentes 2017-2020.csv", sep=";", encoding='iso-8859-1') 

for file in os.listdir('Currículos'): # Clear the folder that holds the resumes
	os.remove(f"Currículos/{file}")

for pos, professor in enumerate(professors["Nome"]): # Iterates through the professors
	link = professors["Lattes"][pos] # Get the link to the professor's lattes page 
	if "lattes" in str(link):
		lattes_id = re.findall(r'[0-9]+', link)[0] # Get the professor's id

		# Request the resume:
		r = requests.get(f"http://sapi.udesc.br:8080/SapiWebService/?tokenAcesso=edd6b4922c1d1252a1646f259336cc5b&acao=downloadCurriculo&codigoLattes={lattes_id}")

		with open(f'{professor}.zip', 'wb') as f: # Download it as a zip file
			f.write(r.content)

		with zipfile.ZipFile(f"{professor}.zip", 'r') as zip_ref:
			os.mkdir("temp")
			zip_ref.extractall("temp") # Extract all the content in the zip file to a temporary folder

		os.chdir("temp") # Go to the temporary folder
		os.rename(os.listdir()[0], f'{professor}.xml') # Change the name of the xml file

		os.chdir("..") # Get out of the temporary folder
		os.rename(f"temp/{professor}.xml", f"Currículos/{professor}.xml") # Put the xml file into the folder "Currículos"

		os.remove(f"{professor}.zip") # Remove the zip file
		os.rmdir("temp") # Remove the temporary folder


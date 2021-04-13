import requests
import zipfile
import os
import pandas as pd
import re

# Read the file with the encoding utf-8 and if that doesn't work try with iso-8859-1
try:
	egress = pd.read_csv("Egressos.csv", sep=";", encoding='utf-8') 
except:
	egress = pd.read_csv("Egressos.csv", sep=";", encoding='iso-8859-1') 

for file in os.listdir('../Curriculos'): # Clear the folder that holds the resumes
	os.remove(f"../Curriculos/{file}")

for pos, student in enumerate(egress["Aluno"]): # Iterates through the egress
	link = egress["Lattes"][pos] # Get the link to the student's lattes page 
	if "lattes" in str(link):
		lattes_id = re.findall(r'[0-9]+', link)[0] # Get the student's id

		# Request the resume:
		r = requests.get(f"http://sapi.udesc.br:8080/SapiWebService/?tokenAcesso=edd6b4922c1d1252a1646f259336cc5b&acao=downloadCurriculo&codigoLattes={lattes_id}")

		with open(f'{student}.zip', 'wb') as f: # Download it as a zip file
			f.write(r.content)

		with zipfile.ZipFile(f"{student}.zip", 'r') as zip_ref:
			os.mkdir("temp")
			zip_ref.extractall("temp") # Extract all the content in the zip file to a temporary folder

		os.chdir("temp") # Go to the temporary folder
		os.rename(os.listdir()[0], f'{student}.xml') # Change the name of the xml file

		os.chdir("..") # Get out of the temporary folder
		os.rename(f"temp/{student}.xml", f"../Curriculos/{student}.xml") # Put the xml file into the folder "Currículos"

		os.remove(f"{student}.zip") # Remove the zip file
		os.rmdir("temp") # Remove the temporary folder


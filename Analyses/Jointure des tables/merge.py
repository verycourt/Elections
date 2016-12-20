# Merge table impots 

import pandas as pd  
import re
import os
# Merge Sheets Impots : impots_locaux_2000-2015.xls
# Taxe Habitation 

sheet_0 = pd.read_excel("impots_locaux_2000-2015.xls",sheetname=0,skiprows=3,skip_footer =2)
sheet_0 = sheet_0.iloc[:,1:] 

# Créer une norme pour les variables Tx_Hab_an 
sheet_0 = sheet_0.rename(columns={'Unnamed: 1': 'code', 'Unnamed: 2': 'départements',2001:'Tx_Hab_an01',
									2002: "Tx_Hab_an02", 2003:"Tx_Hab_an03" , 2004:"Tx_Hab_an04",
                                  2005:"Tx_Hab_an05", 2006:"Tx_Hab_an06", 2007 : "Tx_Hab_an07",                            
                                  2008:"Tx_Hab_an08", 2009:"Tx_Hab_an09", 
                                  2010:'Tx_Hab_an10'})

# Foncier Bâti
sheet_1 = pd.read_excel("impots_locaux_2000-2015.xls",sheetname=1,skiprows=3,skip_footer =4)
sheet_1 = sheet_1.iloc[:,1:] 


# Créer une norme pour les variables Tx_FonBat_an 
sheet_1 = sheet_1.rename(columns={'Unnamed: 1': 'code', 'Unnamed: 2': 'départements',2001:'Tx_FonBat_an01',
									2002: "Tx_FonBat_an02", 2003:"Tx_FonBat_an03" , 2004:"Tx_FonBat_an04",
                                  2005:"Tx_FonBat_an05", 2006:"Tx_FonBat_an06", 2007 : "Tx_FonBat_an07",                            
                                  2008:"Tx_FonBat_an08", 2009:"Tx_FonBat_an09", 
                                  '2010 (2)\n(taux votés)':"Tx_FonBat_an10_vote",
                                  '2010 (2)\n(taux de référence)' : "Tx_FonBat_an10_ref",                      
       							'2011 (2)' : "Tx_FonBat_an11",
                                  2012:"Tx_FonBat_an12", 2013 : "Tx_FonBat_an13",
                                  2014 : "Tx_FonBat_an14",  2015 : "Tx_FonBat_an15"})



# Foncier non Bâti 
sheet_2 = pd.read_excel("impots_locaux_2000-2015.xls",sheetname=2,skiprows=3,skip_footer=3)
sheet_2 = sheet_2.iloc[:,1:]

# Créer une norme pour les variables Tx_FonNonBat_an 
sheet_2 = sheet_2.rename(columns={'Unnamed: 1': 'code', 'Unnamed: 2': 'départements',2001:'Tx_FonNonBat_an01',
									2002: "Tx_FonNonBat_an02", 2003:"Tx_FonNonBat_an03" , 2004:"Tx_FonNonBat_an04",
                                  2005:"Tx_FonNonBat_an05", 2006:"Tx_FonNonBat_an06", 2007 : "Tx_FonNonBat_an07",                            
                                  2008:"Tx_FonNonBat_an08", 2009:"Tx_FonNonBat_an09", 
                                  2010:'Tx_FonNonBat_an10'})


# Taxe Professionnelle 

sheet_3 = pd.read_excel("impots_locaux_2000-2015.xls",sheetname=3,skiprows=3)
sheet_3 = sheet_3.iloc[:,1:]

# Créer une norme pour les variables Tx_Pro_an 
sheet_3 = sheet_3.rename(columns={'Unnamed: 1': 'code', 'Unnamed: 2': 'départements',2001:'Tx_Pro_an01',
									2002: "Tx_Pro_an02", 2003:"Tx_Pro_an03" , 2004:"Tx_Pro_an04",
                                  2005:"Tx_Pro_an05", 2006:"Tx_Pro_an06", 2007 : "Tx_Pro_an07",                            
                                  2008:"Tx_Pro_an08", 2009:"Tx_Pro_an09" })



base_impots_an0 = pd.merge(sheet_0,sheet_1,on=["code","départements"])
base_impots_an1 = pd.merge(sheet_2,sheet_3,on=["code","départements"])

base_impots = pd.merge(base_impots_an0,base_impots_an1,on=["code","départements"])

# Passage des libellés des départements en minuscule 
base_impots["départements"] = base_impots["départements"].apply(lambda x : x.lower())
# On s'assure du bon format des codes départementaux 
base_impots["code"] = base_impots["code"].apply(lambda x : str(x))

# Merge Caf 


# Dénombrement des foyers bénéficiaires d'un droit payable aux allocations familiales : AFCafdepuis1993.csv
"""
Code Insee des départements avec comme exception les codes suivants :
	
	17M Caisse nationale maritime (chargée du versement des prestations familiales et sociales auprès
	    des marins qui relèvent du régime des gens de mer (Enim).

				
   2ème colonne - DEPLIB -
	Libellé du département de la Caf. Le territoire de compétence des Caisses d'allocations famililes (Caf)
	correspond au département à l'exception de deux cas :					
			-  Pyrénées-Atlantiques (2 Caf Pays Basque et Seignanx et Béarn et de la Soule),
			-  Landes (le canton de Saint Martin de Seignanx est géré par la Caf du Pays Basque et Seignanx)

	La donnée évoque le nombre de foyer aux quelles ont a versé une prestation
"""


# On skip les deux dernières lignes car elles concernent st bart et st martin 

af_caf = pd.read_csv("AFCafdepuis1993.csv",sep=";",encoding="ISO-8859-1",skipfooter=3,engine="python" )


# Dénombrement des foyers allocataires percevant l'allocation de logement familiale (ALF) : ALFCafdepuis1993.csv

alf_caf = pd.read_csv("ALFCafdepuis1993.csv",sep=";",encoding="ISO-8859-1",skipfooter=3,engine="python" )

alf_caf = alf_caf.rename(columns={'dep': 'dep_'})

# Pour chacune des tables de la caf on veut : 
# Supprimer la ligne Caisse national maritime car on ne sait pas à quel département elle est liée 
# merge les deux caisses du 64  => pyrenees atlantiques

def clean_caf(data,pattern):

	data = data.drop( data[data["dep_"] == "17M"].index )

	data.iloc[65] = data.iloc[65]+ data.iloc[66]
	data.iloc[65]["dep_"] = "64"
	data.iloc[65]["reg"] = "72"
	data.loc[65]["deplib"] = "pyrenees atlantiques"
	data = data.drop(66).reset_index(drop=True)


	# On conserve les AF à fin décembre 
	    
	# On ajoute à la liste les colonnes de départements,region...
	# On supprime le libellé de département car on va effectuer la jointure sur la table impôt qui le contient 

	liste_columns_to_keep = ['dep_', 'reg']

	for i in data.columns.tolist():
		find_patern = re.compile("déc-\d+|déc\d+").search(i)

		try :
			liste_columns_to_keep.append(find_patern.group())
		except AttributeError:
			pass


	data = data.loc[:,liste_columns_to_keep]

	# Normaliser les noms de colonnes
	for name in liste_columns_to_keep :

		find_patern = re.compile("déc-\d+|déc\d+").search(name)
		try:
			name_columns = find_patern.group()
			data = data.rename(columns={name_columns : name_columns.replace("déc",pattern).replace("-","")})

		except AttributeError:
			pass


	return data

 
alf_caf = clean_caf(alf_caf,"alf")
af_caf  = clean_caf(af_caf,"af")

# Avant de pouvoir joindre les deux tables on doit opérer une modification sur af_caf
# les numéros de 1-9 ne sont pas à 2 digits 

for i in range(af_caf.shape[0]):

	if len(af_caf.loc[i,"dep_"]) == 1 :
		af_caf.loc[i,"dep_"] = "0"+ af_caf.loc[i,"dep_"]

# On crée une table qui regroupe toutes les données sur la caf 

base_caf = pd.merge(alf_caf,af_caf ,on=["dep_"],suffixes=('', '_y'))

# Comme la clé de jointure est "dep_", on a deux fois l'information reg, on nettoie cela 
del base_caf["reg_y"]


# Jointure entre la base de caf et la base impots 

# Pour merge base_caf et base_impot on doit avoir une clé commune
base_caf = base_caf.rename(columns={"dep_" : "code"})


# On export les deux tables intermédiaires

#base_caf.to_csv(os.getcwd()+"/base_caf.csv")
#base_impots.to_csv(os.getcwd()+"/base_impots.csv")

base_caf_dgi = pd.merge(base_caf,base_impots ,on=["code"],suffixes=('', ''))

base_caf_dgi.to_csv(os.getcwd()+"/base_caf_dgi.csv")
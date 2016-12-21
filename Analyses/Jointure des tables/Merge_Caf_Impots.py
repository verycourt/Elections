# Merge table impots 

import pandas as pd  
import re
import os
import numpy as np 
# Merge Sheets Impots : impots_locaux_2000-2015.xls
# Taxe Habitation 

sheet_0 = pd.read_excel("impots_locaux_2000-2015.xls",sheetname=0,skiprows=3,skip_footer =2)
sheet_0 = sheet_0.iloc[:,1:] 

# Créer une norme pour les variables TxHab_an 
sheet_0 = sheet_0.rename(columns={'Unnamed: 1': 'code', 'Unnamed: 2': 'département',2001:'TxHab_an01',
									2002: "TxHab_an02", 2003:"TxHab_an03" , 2004:"TxHab_an04",
                                  2005:"TxHab_an05", 2006:"TxHab_an06", 2007 : "TxHab_an07",                            
                                  2008:"TxHab_an08", 2009:"TxHab_an09", 
                                  2010:'TxHab_an10'})



# Foncier Bâti
sheet_1 = pd.read_excel("impots_locaux_2000-2015.xls",sheetname=1,skiprows=3,skip_footer =4)
sheet_1 = sheet_1.iloc[:,1:] 


# Créer une norme pour les variables TxFonBat_an 
sheet_1 = sheet_1.rename(columns={'Unnamed: 1': 'code', 'Unnamed: 2': 'département',2001:'TxFonBat_an01',
									2002: "TxFonBat_an02", 2003:"TxFonBat_an03" , 2004:"TxFonBat_an04",
                                  2005:"TxFonBat_an05", 2006:"TxFonBat_an06", 2007 : "TxFonBat_an07",                            
                                  2008:"TxFonBat_an08", 2009:"TxFonBat_an09", 
                                  '2010 (2)\n(taux votés)':"TxFonBat_an10_vote",
                                  '2010 (2)\n(taux de référence)' : "TxFonBat_an10_ref",                      
       							'2011 (2)' : "TxFonBat_an11",
                                  2012:"TxFonBat_an12", 2013 : "TxFonBat_an13",
                                  2014 : "TxFonBat_an14",  2015 : "TxFonBat_an15"})



# Foncier non Bâti 
sheet_2 = pd.read_excel("impots_locaux_2000-2015.xls",sheetname=2,skiprows=3,skip_footer=3)
sheet_2 = sheet_2.iloc[:,1:]

# Créer une norme pour les variables TxFonNonBat_an 
sheet_2 = sheet_2.rename(columns={'Unnamed: 1': 'code', 'Unnamed: 2': 'département',2001:'TxFonNonBat_an01',
									2002: "TxFonNonBat_an02", 2003:"TxFonNonBat_an03" , 2004:"TxFonNonBat_an04",
                                  2005:"TxFonNonBat_an05", 2006:"TxFonNonBat_an06", 2007 : "TxFonNonBat_an07",                            
                                  2008:"TxFonNonBat_an08", 2009:"TxFonNonBat_an09", 
                                  2010:'TxFonNonBat_an10'})


# Taxe Professionnelle 

sheet_3 = pd.read_excel("impots_locaux_2000-2015.xls",sheetname=3,skiprows=3)
sheet_3 = sheet_3.iloc[:,1:]

# Créer une norme pour les variables TxPro_an 
sheet_3 = sheet_3.rename(columns={'Unnamed: 1': 'code', 'Unnamed: 2': 'département',2001:'TxPro_an01',
									2002: "TxPro_an02", 2003:"TxPro_an03" , 2004:"TxPro_an04",
                                  2005:"TxPro_an05", 2006:"TxPro_an06", 2007 : "TxPro_an07",                            
                                  2008:"TxPro_an08", 2009:"TxPro_an09" })



base_impots_an0 = pd.merge(sheet_0,sheet_1,on=["code","département"])
base_impots_an1 = pd.merge(sheet_2,sheet_3,on=["code","département"])

base_impots = pd.merge(base_impots_an0,base_impots_an1,on=["code","département"])

# Passage des libellés des départements en minuscule 
base_impots["département"] = base_impots["département"].apply(lambda x : x.lower())
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

# Foyers allocataires percevant l'aide personnalisée au logement (APL) par Caf
# Attention la table d'APL n'a d'informations sur les DOM-TOM
apl_caf = pd.read_csv("APLCafdepuis1993.csv",sep=";",encoding="ISO-8859-1",engine="python" )
apl_caf = apl_caf.rename(columns={'dep': 'dep_'}) 

# Pour chacune des tables de la caf on veut : 
# Supprimer la ligne Caisse national maritime car on ne sait pas à quel département elle est liée 
# merge les deux caisses du 64  => pyrenees atlantiques

def clean_caf(data,pattern,adj_index):

	data = data.drop( data[data["dep_"] == "17M"].index )

	data.iloc[65] = data.iloc[65]+ data.iloc[66-adj_index]
	data.iloc[65]["dep_"] = "64"
	data.iloc[65]["reg"] = "72"
	data.loc[65]["deplib"] = "pyrenees atlantiques"
	data = data.drop(66-adj_index).reset_index(drop=True)


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

 
alf_caf = clean_caf(alf_caf,"alf",0)
af_caf  = clean_caf(af_caf,"af",0)
apl_caf = clean_caf(apl_caf,"apl",2)

# Avant de pouvoir joindre les deux tables on doit opérer une modification sur af_caf
# les numéros de 1-9 ne sont pas à 2 digits 

for i in range(af_caf.shape[0]):

	if len(af_caf.loc[i,"dep_"]) == 1 :
		af_caf.loc[i,"dep_"] = "0"+ af_caf.loc[i,"dep_"]

# On crée une table qui regroupe toutes les données sur la caf 

# 1ère étape : on merge les deux tables qui ont le même périmètre de département
base_caf = pd.merge(alf_caf,af_caf ,on=["dep_"],suffixes=('', '_y'))


# 2ème étape : on merge par un left join la table apl car elle ne possède pas les DOM-TOM 
base_caf = pd.merge(base_caf,apl_caf,how='left',on=["dep_"],suffixes=('', '_y'))

# Comme la clé de jointure est "dep_", on a deux fois l'information reg, on nettoie cela 
del base_caf["reg_y"]


# Jointure entre la base de caf et la base impots 

# Pour merge base_caf et base_impot on doit avoir une clé commune
base_caf = base_caf.rename(columns={"dep_" : "code"})


# On export les deux tables intermédiaires

base_caf.to_csv(os.getcwd()+"/base_caf.csv")
base_impots.to_csv(os.getcwd()+"/base_impots.csv")

base_caf_dgi = pd.merge(base_caf,base_impots ,on=["code"],suffixes=('', ''))

#base_caf_dgi.to_csv(os.getcwd()+"/base_caf_dgi.csv")




# On veut une nouvelle structure sur notre table avec une variable année

# PAS OPTIMMM !!!!
 
name_columns = {"code","reg","département","année","af","alf","apl","TxPro","TxFonNonBat","TxFonBat","TxHab"}
base_caf_dgi_2 = pd.DataFrame(columns=name_columns)

list_year = ["93","94","95","96","97","98","99","00","01","02","03","04","05","06","07","08",
			"09","10","11","12","13","14","15"]

for i in range(base_caf_dgi.shape[0]) :

	code = base_caf_dgi.loc[i,"code"]
	reg = base_caf_dgi.loc[i,"reg"]
	departement = base_caf_dgi.loc[i,"département"]

	for j in list_year:
		
		if int(j) < 50 :
			annee = "20" + j
		else :
			annee = "19" + j 

		var_af = np.nan
		var_alf = np.nan
		var_apl = np.nan
		var_TxPro = np.nan
		var_TxHab = np.nan
		var_TxFonBat = np.nan
		var_TxFonNonBat = np.nan

		for name in base_caf_dgi.columns.tolist() : 
			
			if name not in ["code","reg","département"] :

				year = re.compile("\d+").search(name).group()

				if year == j :

					var = re.compile("[A-Za-z]+").search(name).group()

					if var == "af":
						var_af = base_caf_dgi.loc[i,name]

					elif var == "alf":
						var_alf = base_caf_dgi.loc[i,name]

					elif var == "apl":
						var_apl = base_caf_dgi.loc[i,name]

					elif var == "TxPro":
						var_TxPro = base_caf_dgi.loc[i,name]

					elif var == "TxFonNonBat" : 
						var_TxFonNonBat = base_caf_dgi.loc[i,name]

					elif var == "TxFonBat" : 
						var_TxFonBat = base_caf_dgi.loc[i,name]
					elif var == "TxHab" :
						var_TxHab = base_caf_dgi.loc[i,name]
					else :
						pass

		dict_add = {"code":code,"reg":reg,"département":departement,"année":annee,"af":var_af,
				"alf":var_alf,"apl":var_apl,"TxPro":var_TxPro,
				"TxFonNonBat":var_TxFonNonBat,"TxFonBat":var_TxFonBat,"TxHab":var_TxHab}

		base_caf_dgi_2 = base_caf_dgi_2.append(dict_add,ignore_index=True )
		

# Organisation des colonnes pour l'extraction 

new_list_columns = ['code','département','reg','année','alf',
 'af',
 'TxHab',
 'apl',
 'TxFonNonBat',
 'TxFonBat',
 'TxPro']

base_caf_dgi_2 = base_caf_dgi_2[new_list_columns]

base_caf_dgi_2.to_csv(os.getcwd()+"/base_caf_dgi.csv",encoding="ISO-8859-1")



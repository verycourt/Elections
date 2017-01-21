Paramètres autorisés pour le script de scrapping :

Deux options
	1. Ne passer aucun argument en paramètre : 
Dans ce cas le script va tourner pour chaque couple (argument1, argument2) définis ci-dessous.

	2. Spécifier un seul ou les deux arguments parmi :
	Argument 1 (les termes de recherche) :
	- candidats_1 (Fillon, Mélanchon, Macron, Le Pen, Valls)
	- partis_1 (LR, PS, FN, EELV)
	- divers_gauche (France Insoumise, Lutte Ouvriere, NPA, PCF)
	
	Argument 2 (la période) :
	- 1d (un jour)
	- 3d (trois jours)

Exemple en ligne de commande :
python script_scrap_gtrends.py "candidats_majeurs" "3d"

Un retour console indique le succès ou l'échec du scrapping.
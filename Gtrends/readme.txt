Param�tres autoris�s pour le script de scrapping :

Deux options
	1. Ne passer aucun argument en param�tre : 
Dans ce cas le script va tourner pour chaque couple (argument1, argument2) d�finis ci-dessous.

	2. Sp�cifier un seul ou les deux arguments parmi :
	Argument 1 (les termes de recherche) :
	- candidats_1 (Fillon, M�lanchon, Macron, Le Pen, Valls)
	- partis_1 (LR, PS, FN, EELV)
	- divers_gauche (France Insoumise, Lutte Ouvriere, NPA, PCF)
	
	Argument 2 (la p�riode) :
	- 1d (un jour)
	- 3d (trois jours)

Exemple en ligne de commande :
python script_scrap_gtrends.py				=> toutes les recherches sont ex�cut�es
python script_scrap_gtrends.py "" "1d"			=> tous les arg1, avec la p�riode 1d


Un retour console indique le succ�s ou l'�chec du scrapping.
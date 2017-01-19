Paramètres autorisés pour le script de scrapping :

1. Argument 1 (les termes de recherche) :
	- candidats_majeurs (Fillon, Jadot, Macron, Le Pen, Valls) => par défaut
	- partis_majeurs (LR, PS, FN, EELV)
	- divers_gauche (France Insoumise, Lutte Ouvriere, NPA, PCF)

2. Argument 2 (la période) :
	- 1h
	- 4h
	- 1d
	- 3d => Par défaut
	- 7d
	- 1m
	- 3m

Exemple en ligne de commande :
python script_scrap_gtrends.py "candidats_majeurs" "3d"

Un retour console indique le succès ou l'échec du scrapping.
Le script de scrapping enregistre les donn�es de Google Trends sous format json dans le dossier /var/www/html/gtrends/data

Choix pour les param�tres :
	1. Ne passer aucun argument en param�tre : 
	Dans ce cas le script va par d�faut prendre les param�tres "candidats_A" et "7d"

	2. Sp�cifier les deux arguments :
	Argument 1 (les termes de recherche) :
		- candidats_A (Fillon, M�lanchon, Macron, Le Pen, Hamon)
	
	Argument 2 (la p�riode) :
		- 1h (une heure)
		- 4h (quatre heures)
		- 1d (un jour)
		- 7d (une semaine)
		- 1m (un mois)

NB: on peut faire un choix multiple sur un argument en ins�rant des virgules.

Exemple en ligne de commande :

python script_scrap_gtrends.py				=> "candidats_A" et "7d"
python script_scrap_gtrends.py "candidats_A" "1d,7d"	=> "candidats_A" pour les p�riodes "1d" et "7d"

Un retour console indique le succ�s ou l'�chec du scrapping.
Crontab sauvegarde le log dans le dossier Gtrends/log.
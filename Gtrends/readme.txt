Le script de scrapping enregistre les données de Google Trends sous format json dans le dossier /var/www/html/gtrends/data

Choix pour les paramètres :
	1. Ne passer aucun argument en paramètre : 
	Dans ce cas le script va par défaut prendre les paramètres "candidats_A" et "7d"

	2. Spécifier les deux arguments :
	Argument 1 (les termes de recherche) :
		- candidats_A (Fillon, Mélanchon, Macron, Le Pen, Hamon)
	
	Argument 2 (la période) :
		- 1h (une heure)
		- 4h (quatre heures)
		- 1d (un jour)
		- 7d (une semaine)
		- 1m (un mois)

NB: on peut faire un choix multiple sur un argument en insérant des virgules.

Exemple en ligne de commande :

python script_scrap_gtrends.py				=> "candidats_A" et "7d"
python script_scrap_gtrends.py "candidats_A" "1d,7d"	=> "candidats_A" pour les périodes "1d" et "7d"

Un retour console indique le succès ou l'échec du scrapping.
Crontab sauvegarde le log dans le dossier Gtrends/log.
# Projet Le Point 
## Récupération des tweets dans le passé
* Le code récupéré de https://github.com/Jefferson-Henrique/GetOldTweets-python nous permet de récupérer les tweets sur une fenêtre temporelle sans utiliser l'API twitter et donc en contournant la limite à 7 jours de tweet. Cependant une limite a été atteinte en récupérant ~20K lignes, une issue a été ouverte à ce sujet sur le github du créateur.
* Pour la récupération _live_ de tweets nous utiliseront https://github.com/anthonymonori/text-mining qui insère les extractions dans une base MongoDB

## Exemples d'utilisation

_python Exporter.py --querysearch "primaire droite" --since 2016-05-15_
Les tweets recoltés sont exportés sous forme structurée (.csv)


## Récupération live de tweets
* L'infra mise en place sur AWS nous permet de récupérer les tweets en streaming en utiliant  RabbitMQ
* Le script a été transformé en service pour permettre une exécution en tâche de fond
* TODO : écrire le script .sh qui sera appelé par Crontab et finaliser traitement_JSON.py pour permettre l'import dans mongo
1) Le Script .sh arrête le service tweet river
2) Le script .sh renomme le fichier all_tweet.txt => temp_all_tweet.txt
4) Le script .sh relance le service tweet_river
3) Le script .sh appelle traitement_json.py
4) Le script traitement_json.py effectue les opérations suivantes :
a) Nettoyer les données et les transformer en JSON
b) Importer les données dans MongoDB avec une bonne gestion d'erreur
5) Le script .sh supprime temp_all_tweet.txt


## Analyse Google Trends
Une API non officielle permet de récupérer certaines données de Google Trends, format JSON et DataFrame pandas pour les volumes de recherche, avec la possibilité d'exporter en format .csv si besoin.
Le code de l'API est copié dans le fichier trendsAPI.py pour l'adapter à nos besoins.

Documentation de l'API à cette adresse : https://github.com/GeneralMills/pytrends

Problème ouvert : limite de 5 termes de recherche à la fois. Comment faire pour merger plusieurs tables de résultats pour contourner cette limite ? 

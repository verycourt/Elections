# Projet Le Point 
## Récupération des tweets dans le passé
* Le code récupéré de https://github.com/Jefferson-Henrique/GetOldTweets-python nous permet de récupérer les tweets sur une fenêtre temporelle sans utiliser l'API twitter et donc en contournant la limite à 7 jours de tweet. Cependant une limite a été atteinte en récupérant ~20K lignes, une issue a été ouverte à ce sujet sur le github du créateur.
* Pour la récupération _live_ de tweets nous utiliseront https://github.com/anthonymonori/text-mining qui insère les extractions dans une base MongoDB

## Exemples d'utilisation

_python Exporter.py --querysearch "primaire droite" --since 2016-05-15_
Les tweets recoltés sont exportés sous forme structurée (.csv)


## Récupération live de tweets
* L'infra mise en place sur AWS nous permet de récupérer les tweets en streaming en utiliant  RabbitMQ

## Analyse Google Trends
Une API non officielle permet de récupérer certaines données de Google Trends, format JSON et DataFrame pandas pour les volumes de recherche, avec la possibilité d'exporter en format .csv si besoin.
Le code de l'API est copié dans le fichier trendsAPI.py pour l'adapter à nos besoins.

Documentation de l'API à cette adresse : https://github.com/GeneralMills/pytrends

Problème ouvert : limite de 5 termes de recherche à la fois. Comment faire pour merger plusieurs tables de résultats pour contourner cette limite ? 

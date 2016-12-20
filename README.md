# Projet Le Point 
## Récupération des tweets dans le passé
* Le code récupéré de https://github.com/Jefferson-Henrique/GetOldTweets-python nous permet de récupérer les tweets sur une fenêtre temporelle sans utiliser l'API twitter et donc en contournant la limite à 7 jours de tweet. Cependant une limite a été atteinte en récupérant ~20K lignes, une issue a été ouverte à ce sujet sur le github du créateur.
* Pour la récupération _live_ de tweets nous utiliseront https://github.com/anthonymonori/text-mining qui insère les extractions dans une base MongoDB

## Exemples d'utilisation

_python Exporter.py --querysearch "primaire droite" --since 2016-05-15_
Les tweets recoltés sont exportés sous forme structurée (.csv)


## Récupération live de tweets
* L'infra mise en place sur AWS nous permet de récupérer les tweets en streaming en utiliant  RabbitMQ


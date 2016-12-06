# Branche Dev 
## Première feature : récupération des tweets
* Le code récupéré de https://github.com/Jefferson-Henrique/GetOldTweets-python nous permet de récupérer les tweets sur une fenêtre temporelle sans utiliser l'API twitter et donc en contournant la limite à 7 jours de tweet. Cependant une limite a été atteinte en récupérant ~20K lignes, une issue a été ouverte à ce sujet sur le github du créateur.
* Pour la récupération _live_ de tweets nous utiliseront https://github.com/anthonymonori/text-mining qui insère les extractions dans une base MongoDB
* Pour contourner les limites de l'API twitter, nous utilisons RabbitMQ sur le Teralab de l'école qui lisse la récupération des tweets et réinserons les tweets exportés de RabbitMQ au format JSON dans MongoDB
## Exemples d'utilisation

_python Exporter.py --querysearch "primaire droite" --since 2016-05-15_
Les tweets recoltés sont exportés sous forme structurée (.csv)

## Deuxième Feature : Data Visualisations à partir des tweets

* Dans MongoDB nous effectuons le NLP
* Nous traçons les graphs en exploitant les données récupérée via l'API Node.js de MongoDB

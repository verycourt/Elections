# Méthodologie


1. Première étape : Collecte de données
Pour l'instant, nous sommes capables de collecter seulement la transcription 
sous forme de texte des débats n°3 et n°4 de la primaire de gauche
(19/01 et 25/01). 

La méthode consiste à extraire du web le document texte utilisé par
le site pluzz (France 2) pour produire les sous-titres des deux débats.

2. Deuxième étape : Traitement du texte

Une fois le texte récupéré, on identifie chaque candidat par un pattern
du type "- M. Valls" qui indique le début de la prise de parole du candidat.
Une fois les prises de paroles identifiées, on calcule l'occurence de chaque
mot dans le discours de chacun des candidats.

3. Troisième étape : Représentation

Une fois la liste des mots et de leurs occurences produite, il ne reste plus
qu'à produire une visualisation. 
Pour cela, on peut utiliser une visualition classique dite "Word Cloud" qui 
représente les mots sous la forme de nuage, et attribue une taille plus ou moins
grande à chaque mot selon son nombre d'occurrences.
On peut également utiliser un "Word Cloud" personnalisé pour introduire un 
dégradé de couleurs sur les mots selon le nombre d'occurrences des mots. 

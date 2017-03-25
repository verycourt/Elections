<!DOCTYPE html>
<html>
	
	<head>
		<title>Réseaux sociaux</title>

		<?php include "/var/www/html/site_head.html";?>
		<style><?php include "/var/www/html/header_style.css";?></style>
		<!-- si besoin, rajouter une feuille de style css via une balise link ici -->
	</head>

	<body>	
		<header><?php include "/var/www/html/site_header.html";?></header>
		<div style="margin-left:10%">
		<div>
			<canvas id="radar" width="700" height="450"></canvas>
		</div>

		<script src="radar.js" type="text/javascript"></script>
		<p>* Les likes des vidéos YouTube sont une moyenne sur les 10 dernières vidéos publiées sur la chaîne des candidats.</p>
		<p>** Les mentions sur Facebook représentent le nombre d'utilisateurs qui ont interagi avec la page officielle d'un des candidat. Les interactions comprennent notamment les likes, les commentaires ou partages d'une publication de la page du candidat.</p>
		<p><strong>Sources :</strong> Facebook, Twitter, Youtube. Données actualisées tous les jours. </p>
		</div>
	</body>
</html>

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
		<p>Les 2 indicateurs YouTube prennent en compte les 10 dernières vidéos publiées sur les chaînes officielles de chaque candidat.</p>
		<p><strong>Sources :</strong> Facebook, Twitter, Youtube. Données actualisées tous les jours. </p>
		</div>
	</body>
</html>

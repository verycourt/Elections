<!DOCTYPE html>
<html>
	
	<head>
		<title>Parrainages par candidat</title>

		<?php include "/var/www/html/site_head.html";?>
		<style><?php include "/var/www/html/header_style.css";?></style>
		<!-- si besoin, rajouter une feuille de style css via une balise link ici -->
	</head>

	<body>	
		<header><?php include "/var/www/html/site_header.html";?></header>

		<!-- rajouter le body souhaite ici -->

		<div class="bar">
			<canvas id="chartParrainages" width="550" height="300"></canvas>
		</div>
		<script src="parrainages.js" type="text/javascript"></script>
		<p> Le niveau de dégradé indique la date d'obtention des parrainages. Plus il est foncé plus il est récent. </p>
		<p> Source des données : conseil constitutionnel. </p>
	</body>
</html>